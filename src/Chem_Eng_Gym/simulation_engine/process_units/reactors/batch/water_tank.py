
from pyomo.environ import *
from pyomo.dae import *

class WaterTank:
    def __init__(self, Cv=0.1, A=1.0, t_end=10):
        self.Cv = Cv
        self.A = A
        self.t_end = t_end

        self.model = self._build_model()

    def _build_model(self):
        m = ConcreteModel()

        # Time 
        m.t = ContinuousSet(bounds=(0, self.t_end))

        # Variables
        m.V = Var(m.t, within=NonNegativeReals)  # volume of water in the vessel
        m.h = Var(m.t, within=NonNegativeReals)  # height of water in vessel

        # Inlet flow rate (assume a step at t=5)
        m.F_in = Var(m.t, initialize=0.0)
        m.F_in[0].fix(0.0)

        def _F_in_rule(m, i):
            if i >= 5:
                return m.F_in[i] == 1.0
            else:
                return Constraint.Skip
        m.F_in_con = Constraint(m.t, rule=_F_in_rule)

        # Outlet flow rate
        m.F_out = Var(m.t, within=NonNegativeReals)

        def _F_out_rule(m, i):
            return m.F_out[i] == self.Cv*sqrt(m.h[i] + 1e-8)  # Adding a small positive number inside sqrt
        m.F_out_con = Constraint(m.t, rule=_F_out_rule)

        # Differential equation
        m.dVdt = DerivativeVar(m.V, wrt=m.t)

        def _differential_eqn(m, i):
            return m.dVdt[i] == m.F_in[i] - m.F_out[i]
        m.differential_eqn = Constraint(m.t, rule=_differential_eqn)

        # Initial condition
        m.V[0].fix(0.0)

        return m

    def solve(self):
        # Choose a solver
        solver = SolverFactory('ipopt')

        # Solve the model
        results = solver.solve(self.model, tee=True)

        # Check if solver was successful
        if (results.solver.status == SolverStatus.ok) and (results.solver.termination_condition == TerminationCondition.optimal):
            print('Successful solve')
        else:
            print('Unsuccessful solve: ' + str(results.solver))

# Instantiate and solve the model
tank = WaterTank()
tank.solve()