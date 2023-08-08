from pyomo.environ import *
from pyomo.dae import *

from pydantic import BaseModel

from Chem_Eng_Gym.simulation_engine.process_units.base_process_unit import BaseProcessUnit

class BufferTank:
    def __init__(self, node_id, params, feed):
        self.node_id = node_id
        self.params = params
        self.feed = feed
        pass
