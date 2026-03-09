"""Computation engine for Visual Angular Impact (VAI)."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence


@dataclass(frozen=True)
class Turbine:
    """Turbine geometry projected in DEM CRS."""

    x: float
    y: float
    hub_h: float
    rot_d: float
    hbase: float


@dataclass(frozen=True)
class DemGrid:
    """In-memory DEM representation with georeferencing information."""

    data: Sequence[Sequence[float]]
    geotransform: tuple[float, float, float, float, float, float]
    nodata: float | None

    @property
    def nrows(self) -> int:
        return len(self.data)

    @property
    def ncols(self) -> int:
        return len(self.data[0]) if self.nrows else 0

    @property
    def pixel_size_x(self) -> float:
        return abs(self.geotransform[1])

    @property
    def pixel_size_y(self) -> float:
        return abs(self.geotransform[5])

    @property
    def sample_step(self) -> float:
        return min(self.pixel_size_x, self.pixel_size_y)

    def world_to_pixel(self, x: float, y: float) -> tuple[int, int]:
        gt = self.geotransform
        col = int(math.floor((x - gt[0]) / gt[1]))
        row = int(math.floor((y - gt[3]) / gt[5]))
        return row, col

    def pixel_center(self, row: int, col: int) -> tuple[float, float]:
        gt = self.geotransform
        x = gt[0] + (col + 0.5) * gt[1]
        y = gt[3] + (row + 0.5) * gt[5]
        return x, y

    def value_at(self, x: float, y: float) -> float | None:
        row, col = self.world_to_pixel(x, y)
        if row < 0 or col < 0 or row >= self.nrows or col >= self.ncols:
            return None
        value = float(self.data[row][col])
        if self.nodata is not None and math.isclose(value, self.nodata):
            return None
        if math.isnan(value):
            return None
        return value


def build_spatial_index(turbines: Sequence[Turbine], cell_size: float) -> dict[tuple[int, int], list[int]]:
    """Build a lightweight grid index for non-QGIS contexts/tests."""
    index: dict[tuple[int, int], list[int]] = {}
    if cell_size <= 0:
        return index
    for idx, turbine in enumerate(turbines):
        key = (int(math.floor(turbine.x / cell_size)), int(math.floor(turbine.y / cell_size)))
        index.setdefault(key, []).append(idx)
    return index


def sample_dem_value(dem: DemGrid, x: float, y: float) -> float | None:
    """Sample DEM value with NoData/out-of-bounds handling."""
    return dem.value_at(x, y)


def los_horizon_angle(dem: DemGrid, px: float, py: float, tx: float, ty: float, hp: float) -> float:
    """Compute local horizon angle (radians) along LOS from observer P to turbine T."""
    dx = tx - px
    dy = ty - py
    di = math.hypot(dx, dy)
    if di <= 0.0:
        return -math.inf

    step = max(0.1, dem.sample_step)
    n_steps = int(di / step)
    if n_steps <= 1:
        return -math.inf

    alpha_hor = -math.inf
    for step_idx in range(1, n_steps):
        frac = step_idx / n_steps
        sx = px + dx * frac
        sy = py + dy * frac
        hs = sample_dem_value(dem, sx, sy)
        if hs is None:
            continue
        ds = di * frac
        if ds <= 0.0:
            continue
        alpha = math.atan((hs - hp) / ds)
        if alpha > alpha_hor:
            alpha_hor = alpha
    return alpha_hor


def compute_point_vai(
    px: float,
    py: float,
    hp: float,
    candidate_turbines: Sequence[Turbine],
    dem: DemGrid,
    radius_m: float,
) -> float:
    """Compute VAI at one observer location as Σ(Aapp_vis_i * delta_theta_i), degree²."""
    vai = 0.0

    for turbine in candidate_turbines:
        dx = turbine.x - px
        dy = turbine.y - py
        di = math.hypot(dx, dy)
        if di <= 0.0 or di > radius_m:
            continue

        htop = turbine.hbase + turbine.hub_h + turbine.rot_d / 2.0
        hbot = turbine.hbase + turbine.hub_h - turbine.rot_d / 2.0

        alpha_hor = los_horizon_angle(dem, px, py, turbine.x, turbine.y, hp)
        hcut = hp + math.tan(alpha_hor) * di if alpha_hor != -math.inf else -math.inf

        hvis = max(0.0, htop - max(hbot, hcut))
        if hvis <= 0.0:
            continue

        hvisbase = max(hbot, hcut)
        aapp_vis_rad = max(0.0, math.atan((htop - hp) / di) - math.atan((hvisbase - hp) / di))
        if aapp_vis_rad <= 0.0:
            continue

        aapp_vis_deg = math.degrees(aapp_vis_rad)
        delta_theta_deg = math.degrees(2.0 * math.atan((turbine.rot_d / 2.0) / di))
        vai += aapp_vis_deg * delta_theta_deg

    return float(vai)
