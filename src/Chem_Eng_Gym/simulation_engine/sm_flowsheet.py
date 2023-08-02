# Sequential Modular Flowsheet Paradigm
from pyomo.environ import *
from pyomo.dae import *
from Chem_Eng_Gym.simulation_engine.process_units.sequential_modular. import WaterTank

import networkx as nx

class SMFlowSheet:
    def __init__(self, t_end=10):
        self.t_end = t_end
        self.m = self._build_model()
        self.tanks = []
        self.graph = nx.DiGraph()

    def _build_model(self):
        m = ConcreteModel()
        m.t = ContinuousSet(bounds=(0, self.t_end))
        return m
    