import math

from calculator import DemGrid, Turbine, compute_cell_metrics, union_circular_intervals


def test_union_circular_intervals_wraparound():
    total = union_circular_intervals([(350.0, 10.0), (5.0, 25.0), (100.0, 120.0)])
    assert math.isclose(total, 55.0, rel_tol=1e-9)


def test_los_blocks_visibility_on_ridge():
    dem_data = [
        [100.0, 100.0, 120.0, 100.0, 100.0],
        [100.0, 100.0, 120.0, 100.0, 100.0],
        [100.0, 100.0, 120.0, 100.0, 100.0],
        [100.0, 100.0, 120.0, 100.0, 100.0],
        [100.0, 100.0, 120.0, 100.0, 100.0],
    ]
    dem = DemGrid(dem_data, (0.0, 10.0, 0.0, 50.0, 0.0, -10.0), None)
    p_x, p_y = dem.pixel_center(2, 0)
    hp = dem.value_at(p_x, p_y)
    t_x, t_y = dem.pixel_center(2, 4)
    turbine = Turbine(t_x, t_y, hub_h=10.0, rot_d=20.0, hbase=100.0)

    metrics = compute_cell_metrics(p_x, p_y, hp, [turbine], dem, radius_m=1000.0)
    assert metrics["astor"] == 0
    assert math.isclose(metrics["aapp_sum"], 0.0)


def test_astor_tiny_setup():
    dem_data = [[100.0 for _ in range(5)] for _ in range(5)]
    dem = DemGrid(dem_data, (0.0, 10.0, 0.0, 50.0, 0.0, -10.0), None)
    p_x, p_y = dem.pixel_center(2, 2)
    hp = dem.value_at(p_x, p_y)
    t1_x, t1_y = dem.pixel_center(2, 4)
    t2_x, t2_y = dem.pixel_center(0, 2)
    turbines = [
        Turbine(t1_x, t1_y, hub_h=80.0, rot_d=40.0, hbase=100.0),
        Turbine(t2_x, t2_y, hub_h=80.0, rot_d=40.0, hbase=100.0),
    ]

    metrics = compute_cell_metrics(p_x, p_y, hp, turbines, dem, radius_m=1000.0)
    assert metrics["astor"] == 2
    assert metrics["hocc"] > 0
    assert metrics["aapp_sum"] > 0
