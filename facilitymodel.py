#import gurobipy as gp
#from gurobipy import GRB
import grb_adapter as gp
from grb_adapter import GRB


def solve_facility_problem(demand, capacity, fixedCosts, transCosts):
    plants = range(len(capacity))
    warehouses = range(len(demand))

    m = gp.Model("facility")

    open = m.addVars(plants, vtype=GRB.BINARY, name="open")
    transport = m.addVars(warehouses, plants, name="trans")

    for p in plants:
        m.addConstr(sum(transport[w, p] for w in warehouses) <= capacity[p] * open[p], "Capacity[%d]" % p)

    for w in warehouses:
        m.addConstr(sum(transport[w, p] for p in plants) == demand[w], "Demand[%d]" % w)

    total_fixed_costs = sum(open[p]*fixedCosts[p] for p in plants)
    total_transportation_costs = sum(transport[w, p] * transCosts[w][p]
                                     for w in warehouses
                                     for p in plants)

    m.setObjective(total_fixed_costs + total_transportation_costs)

    m.optimize()

    open_solution = {key: var.X for key, var in open.items()}
    transport_solution = {key: var.X for key, var in transport.items()}
    return open_solution, transport_solution, m.ObjVal
