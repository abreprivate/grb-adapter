#!/usr/bin/env python3.11

# Copyright 2023, Gurobi Optimization, LLC

# Solve the classic diet model.  This file implements
# a function that formulates and solves the model,
# but it contains no model data.  The data is
# passed in by the calling program.  Run example 'diet2.py',
# 'diet3.py', or 'diet4.py' to invoke this function.

import grb_adapter as gp
from grb_adapter import GRB
#import gurobipy as gp
#from gurobipy import GRB


def solve_diet_problem(categories, minNutrition, maxNutrition, foods, cost, nutritionValues):
    # Model
    m = gp.Model("diet")

    # Create decision variables for the foods to buy
    buy = m.addVars(foods, name="buy")

    # The objective is to minimize the costs
    m.setObjective(buy.prod(cost), GRB.MINIMIZE)

    # Nutrition constraints
    m.addConstrs(
        (
            gp.quicksum(nutritionValues[f, c] * buy[f] for f in foods)
            >= minNutrition[c]
            for c in categories
        ),
        "_",
    )

    m.addConstrs(
        (
            gp.quicksum(nutritionValues[f, c] * buy[f] for f in foods)
            <= maxNutrition[c]
            for c in categories
        ),
        "_",
    )

    m.optimize()

    return {food: var.X for food, var in buy.items()}
