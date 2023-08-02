from pyomo.environ import *
from pyomo.dae import *
from Chem_Eng_Gym.utils.performance import Timer
from Chem_Eng_Gym.simulation_engine.process_units.tanks.water_tank import WaterTank


import networkx as nx
from networkx.readwrite import json_graph
import json

"""
TO DO:
    - Fix networkx graph.
        - Currently, the outlet stream is dangling
        - Decide if streams should be nodes or edges
            - if edges, determine how to add and replace empty "action nodes"
            - I think action nodes are visually great because they offer the affordance of clicking on them
                they could be colored and shown in a way that begs you to click on them. Like pulsating.
                When you do, it passes that through the agent and you somehow see the recommended options

"""

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
    def add_tank(self, name, Cv=0.1, A=1.0, feed=None):
        """AI is creating summary for add_tank

        Args:
            name ([type]): [description]
            Cv (float, optional): [description]. Defaults to 0.1.
            A (float, optional): [description]. Defaults to 1.0.
            feed ([type], optional): [description]. Defaults to None.

        Returns:
            [type]: [description]
        """
        tank = WaterTank(self.m, name, Cv, A, feed)
        self.tanks.append(tank)

        # Add tank node to graph
        self.graph.add_node(name, Cv=Cv, A=A)

        # Add edge to graph if tank is fed by another tank
        if feed is not None:
            self.graph.add_edge(feed.name, name)

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

    # def save_graph(self, filename):
    #     data = json_graph.node_link_data(self.graph)
    #     with open(filename, 'w') as f:
    #         json.dump(data, f)


# Create a system
with Timer("Flowsheet creation"):
    flow_sheet = EOFlowSheet()

# Add the first tank
with Timer("Adding first tank"):
    tank1 = flow_sheet.add_tank('tank1')

# Add the second tank, fed by the first
with Timer("Adding second tank"):
    tank2 = flow_sheet.add_tank('tank2', feed=tank1.F_out)

# Solve the flow_sheet
with Timer("Solving the flow_sheet"):
    flow_sheet.solve()

#%%
from Chem_Eng_Gym.visualisation.visualiser import Visualiser

visualiser = Visualiser()
visualiser.plot_flowsheet(flow_sheet)

# %%
