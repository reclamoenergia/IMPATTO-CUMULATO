import math

from calculator import DemGrid, Turbine, compute_point_vai


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

    vai = compute_point_vai(p_x, p_y, hp, [turbine], dem, radius_m=1000.0)
    assert math.isclose(vai, 0.0)


def test_vai_tiny_setup_matches_sum_of_products():
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

    vai = compute_point_vai(p_x, p_y, hp, turbines, dem, radius_m=1000.0)

    di = 20.0
    aapp_vis = math.degrees(math.atan((200.0 - 100.0) / di) - math.atan((160.0 - 100.0) / di))
    delta_theta = math.degrees(2.0 * math.atan((40.0 / 2.0) / di))
    expected_vai = 2.0 * (aapp_vis * delta_theta)

    assert math.isclose(vai, expected_vai, rel_tol=1e-9)


def test_invisible_turbine_returns_zero_vai():
    dem_data = [
        [100.0, 100.0, 135.0, 100.0, 100.0],
        [100.0, 100.0, 135.0, 100.0, 100.0],
        [100.0, 100.0, 135.0, 100.0, 100.0],
        [100.0, 100.0, 135.0, 100.0, 100.0],
        [100.0, 100.0, 135.0, 100.0, 100.0],
    ]
    dem = DemGrid(dem_data, (0.0, 10.0, 0.0, 50.0, 0.0, -10.0), None)
    p_x, p_y = dem.pixel_center(2, 0)
    hp = dem.value_at(p_x, p_y)
    t_x, t_y = dem.pixel_center(2, 4)
    turbine = Turbine(t_x, t_y, hub_h=10.0, rot_d=10.0, hbase=100.0)

    vai = compute_point_vai(p_x, p_y, hp, [turbine], dem, radius_m=1000.0)
    assert math.isclose(vai, 0.0)
