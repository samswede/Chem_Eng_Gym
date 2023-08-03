from pyomo.environ import *
from pyomo.dae import *

class WaterTank:
    def __init__(self, m, name, params, feed=None):
        self.m = m
        self.name = name
        self.Cv = params['Cv']
        self.A = params['A']
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
