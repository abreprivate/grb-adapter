import itertools

from ortools.linear_solver import pywraplp


class GRB:
    MINIMIZE = 1
    MAXIMIZE = -1
    CONTINUOUS = 'C'
    BINARY = 'B'
    INTEGER = 'I'


class TupleDict(dict):
    def prod(self, other):
        terms = []
        for key, variable in self.items():
            if (coefficient := other.get(key)) is not None:
                terms.append(coefficient * variable)
        return sum(terms)


class DecisionVar:
    def __init__(self, num_var):
        self.num_var = num_var

    def __add__(self, other): return self.num_var.__add__(other)
    def __sub__(self, other): return self.num_var.__sub__(other)
    def __mul__(self, other): return self.num_var.__mul__(other)
    def __radd__(self, other): return self.num_var.__radd__(other)
    def __rmul__(self, other): return self.num_var.__rmul__(other)

    def __getattr__(self, attr_name):
        if attr_name == 'X':
            return self.num_var.solution_value()
        return getattr(self.num_var, attr_name)


class Model:
    def __init__(self, name=""):
        self.name = name
        self.solver = pywraplp.Solver.CreateSolver("SCIP")

        self.var_constructor_lookup = {GRB.CONTINUOUS: self.solver.NumVar,
                                       GRB.INTEGER: self.solver.IntVar}

    def addVars(self, *indices, lb=0.0, ub=float('inf'), vtype=GRB.CONTINUOUS, name=""):
        solver = self.solver

        if len(indices) == 1:
            my_index = indices[0]
        else:
            my_index = itertools.product(*indices)

        if vtype == GRB.BINARY:
            return TupleDict({element: DecisionVar(solver.BoolVar(name=f"{name}[{element}]"))
                              for element in my_index})

        try:
            constructor = self.var_constructor_lookup[vtype]
        except KeyError:
            raise Exception("vtype not supported")

        return TupleDict({element: DecisionVar(constructor(lb, ub, name=f"{name}[{element}]"))
                          for element in my_index})

    def addConstr(self, constraint, name):
        self.solver.Add(constraint, name=name)

    def addConstrs(self, generator, name=""):
        # TODO: How to inspect the generator frame?
        for constr in generator:
            self.solver.Add(constr, name=name)

    def setObjective(self, expr, sense=GRB.MINIMIZE):
        if sense == GRB.MINIMIZE:
            self.solver.Minimize(expr)
        elif sense == GRB.MAXIMIZE:
            self.solver.Maximize(expr)
        else:
            raise Exception("Objective sense must be +1 or -1.")

    def optimize(self, callback=None):
        self.solver.Solve()

    def __getattr__(self, attr_name):
        if attr_name == 'ObjVal':
            return self.solver.Objective().Value()
        raise AttributeError(self, attr_name)


def quicksum(to_sum):
    return sum(to_sum)
