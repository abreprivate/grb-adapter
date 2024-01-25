from pytest import approx
from facilitymodel import solve_facility_problem


# Warehouse demand in thousands of units
demand = [15, 18, 14, 20]

# Plant capacity in thousands of units
capacity = [20, 22, 17, 19, 18]

# Fixed costs for each plant
fixedCosts = [12000, 15000, 17000, 13000, 16000]

# Transportation costs per thousand units
transCosts = [
    [4000, 2000, 3000, 2500, 4500],
    [2500, 2600, 3400, 3000, 4000],
    [1200, 1800, 2600, 4100, 3000],
    [2200, 2600, 3100, 3700, 3200],
]


def test_facility_problem():
    open, transport, obj_val = solve_facility_problem(demand, capacity, fixedCosts, transCosts)

    assert open[0] == approx(1)
    assert open[1] == approx(1)
    assert open[2] == approx(0)
    assert open[3] == approx(1)
    assert open[4] == approx(1)

    expected_transport = {(2, 0): 14,
                          (3, 0): 6,
                          (0, 1): 14,
                          (3, 1): 8,
                          (0, 3): 1,
                          (1, 3): 18,
                          (3, 4): 6}

    for (w, p), solution in transport.items():
        assert solution == approx(expected_transport.get((w, p), 0))

    assert obj_val == approx(210500)
