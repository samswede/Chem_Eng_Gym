
from pyomo.environ import *
from pyomo.dae import *
from Chem_Eng_Gym.utils.performance import Timer

class WaterTank:
    def __init__(self, m, name, Cv=0.1, A=1.0, feed=None):
        self.m = m
        self.name = name
        self.Cv = Cv
        self.A = A
        self.feed = feed

        self._build_model()

    def _build_model(self):
        self._define_variables()
        self._define_inlet_flowrate()
        self._define_outlet_flowrate()
        self._define_differential_equation()
        self._define_initial_condition()

    def _define_variables(self):
        m = self.m
        m.add_component(self.name + '_V', Var(m.t, within=NonNegativeReals))
        m.add_component(self.name + '_h', Var(m.t, within=NonNegativeReals))
        m.add_component(self.name + '_F_out', Var(m.t, within=NonNegativeReals))
        m.add_component(self.name + '_F_in', Var(m.t, initialize=0.0))

        self.V = getattr(m, self.name + '_V')
        self.h = getattr(m, self.name + '_h')
        self.F_out = getattr(m, self.name + '_F_out')  # Store F_out as an attribute
        self.F_in = getattr(m, self.name + '_F_in')

    def _define_inlet_flowrate(self):
        m = self.m
        if self.feed is None:
            self.F_in[0].fix(0.0)
        else:
            def _F_in_rule(m, i):
                return self.F_in[i] == self.feed[i]
            m.add_component(self.name + '_F_in_con', Constraint(m.t, rule=_F_in_rule))

    def _define_outlet_flowrate(self):
        m = self.m
        def _F_out_rule(m, i):
            return self.F_out[i] == self.Cv*sqrt(self.h[i] + 1e-8)  # Adding a small positive number inside sqrt
        m.add_component(self.name + '_F_out_con', Constraint(m.t, rule=_F_out_rule))

    def _define_differential_equation(self):
        m = self.m
        m.add_component(self.name + '_dVdt', DerivativeVar(self.V, wrt=m.t))
        self.dVdt = getattr(m, self.name + '_dVdt')

        def _differential_eqn(m, i):
            return self.dVdt[i] == self.F_in[i] - self.F_out[i]
        m.add_component(self.name + '_differential_eqn', Constraint(m.t, rule=_differential_eqn))

    def _define_initial_condition(self):
        self.V[0].fix(0.0)


class System:
    def __init__(self, t_end=10):
        self.t_end = t_end
        self.m = self._build_model()
        self.tanks = []

    def _build_model(self):
        m = ConcreteModel()

        # Time
        m.t = ContinuousSet(bounds=(0, self.t_end))

        return m

    def add_tank(self, name, Cv=0.1, A=1.0, feed=None):
        tank = WaterTank(self.m, name, Cv, A, feed)
        self.tanks.append(tank)
        return tank

    def solve(self, print_results= False):
        # Choose a solver
        solver = SolverFactory('ipopt')

        # Solve the model
        results = solver.solve(self.m, tee= print_results)

        # Check if solver was successful
        if (results.solver.status == SolverStatus.ok) and (results.solver.termination_condition == TerminationCondition.optimal):
            print('Successful solve')
        else:
            print('Unsuccessful solve: ' + str(results.solver))

# import time

# class Timer:
#     def __init__(self, name):
#         self.name = name

#     def __enter__(self):
#         self.start = time.perf_counter()

#     def __exit__(self, *args):
#         self.end = time.perf_counter()
#         print(f"{self.name} took {self.end - self.start} seconds")

# Create a system
with Timer("System creation"):
    system = System()

# Add the first tank
with Timer("Adding first tank"):
    tank1 = system.add_tank('tank1')

# Add the second tank, fed by the first
with Timer("Adding second tank"):
    tank2 = system.add_tank('tank2', feed=tank1.F_out)

# Solve the system
with Timer("Solving the system"):
    system.solve()
