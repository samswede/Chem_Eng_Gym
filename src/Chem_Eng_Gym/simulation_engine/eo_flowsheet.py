# Equation Oriented Flowsheet Paradigm
from pyomo.environ import *
from pyomo.dae import *
from Chem_Eng_Gym.simulation_engine.process_units.equation_oriented.tanks.water_tank import WaterTank

import networkx as nx

class EOFlowSheet:
    def __init__(self, t_end=10):
        self.t_end = t_end
        self.m = self._build_model()
        self.tanks = []
        self.graph = nx.DiGraph()

    def _build_model(self):
        m = ConcreteModel()
        m.t = ContinuousSet(bounds=(0, self.t_end))
        return m

    # abstract this to 'add_process_unit' later
    def add_tank(self, process_unit_identifier, Cv=0.1, A=1.0, feed=None):
        """AI is creating summary for add_tank

        Args:
            name ([type]): [description]
            Cv (float, optional): [description]. Defaults to 0.1.
            A (float, optional): [description]. Defaults to 1.0.
            feed ([type], optional): [description]. Defaults to None.

        Returns:
            [type]: [description]
        """
        tank = WaterTank(self.m, process_unit_identifier, Cv, A, feed)
        self.tanks.append(tank)

        # Add tank node to graph
        self.graph.add_node(process_unit_identifier, Cv=Cv, A=A)

        # Add edge to graph if tank is fed by another tank
        if feed is not None:
            self.graph.add_edge(feed.name, process_unit_identifier)

        return tank

    def solve(self, print_results=False):
        """AI is creating summary for solve

        Args:
            print_results (bool, optional): [description]. Defaults to False.
        """
        solver = SolverFactory('ipopt')
        results = solver.solve(self.m, tee=print_results)
        if (results.solver.status == SolverStatus.ok) and (results.solver.termination_condition == TerminationCondition.optimal):
            print('Successful solve')
        else:
            print('Unsuccessful solve: ' + str(results.solver))
