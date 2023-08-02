from pyomo.environ import *
from pyomo.dae import *
from Chem_Eng_Gym.utils.performance import Timer
from Chem_Eng_Gym.simulation_engine.sm_flowsheet import SMFlowSheet
from Chem_Eng_Gym.simulation_engine.eo_flowsheet import EOFlowSheet

from Chem_Eng_Gym.visualisation.visualiser import Visualiser

visualiser = Visualiser()

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
with Timer("Solving the EO flow_sheet"):
    flow_sheet.solve()

with Timer("Plot Flowsheet"):
    visualiser.plot_flowsheet(flow_sheet)

# %%
