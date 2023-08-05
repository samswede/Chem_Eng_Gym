import os
import unittest
from Chem_Eng_Gym.simulation_engine.process_units.sequential_modular.tanks.buffer_tank import BufferTank

from pyomo.environ import *
from pyomo.dae import *

#from types import Dict, Any

class TestBufferTank(unittest.TestCase):
    def setUp(self):

        self.node_id = "T01"

        # include units, and definition within params.
        #self.type_params = Dict(str: Dict(str: Any))
        self.params = {  
                    'param':    {'value': float, 'units': str, 'domain': str, 'bounds': set,
                                'definition': str},
                    'A':        {'value': 1.0, 'units': 'm^2', 'domain': str, 'bounds': set,
                                'definition': 'area of vessel base'}, 
                    'alpha':    {'value': 10.0, 'units': 'kg s^-1 m^-0.5', 'domain': str, 'bounds': set,
                                'definition': 'outlet rate flowrate coefficient'}, 
                    'rho':      {'value': 1000.0, 'units': 'kg m^-3', 'domain': str, 'bounds': set,
                                'definition': 'mass density of water'}
                }
        
        self.feed = {
                'temperature': 300.0,
                'pressure': 1.0,
                'total_mass': 100.0, 'total_moles': 50.0, 
                'total_mass_enthalpy': 100.0, 'total_molar_enthalpy': 100.0,

                'vapour_phase': {   'component_A': {'mass_flowrate': 100.0, 'mass_fraction': 1.0, 
                                                    'molar_flowrate': 50.0, 'molar_fraction': 1.0,
                                                    'mass_enthalpy': 100, 'molar_enthalpy': 100}
                                },
                'liquid_phase': {   'component_A': {'mass_flowrate': 100.0, 'mass_fraction': 1.0, 
                                                    'molar_flowrate': 50.0, 'molar_fraction': 1.0,
                                                    'mass_enthalpy': 100, 'molar_enthalpy': 100},
                                    'component_B': {'mass_flowrate': 100.0, 'mass_fraction': 1.0, 
                                                    'molar_flowrate': 50.0, 'molar_fraction': 1.0,
                                                    'mass_enthalpy': 100, 'molar_enthalpy': 100}
                                },
                'solid_phase': {
                                },
            }
        

        # Specify the variable data
        self.variable_data = {
                                'var1': {'type': 'algebraic', 'init': 1.0, 'domain': NonNegativeReals, 'bounds': (0.0, 5.0), 
                                         'definition': ''}, 
                                'var2': {'type': 'algebraic', 'init': 2.0, 'domain': NonNegativeReals, 'bounds': (0.0, 5.0), 
                                         'definition': ''},
                                'var3': {'type': 'differential', 'initial_condition': 0.0, 'init': 1.0, 'domain': NonNegativeReals, 'bounds': (0.0, 5.0), 
                                         'definition': ''},
                                'var4': {'type': 'differential', 'initial_condition': 0.0, 'init': 2.0, 'domain': NonNegativeReals, 'bounds': (0.0, 5.0), 
                                         'definition': ''}
                            }

        # self.constraint_data =    {
        #                         'constraint1': {'expr': self.constraint_1_expr, 
        #                                         'assumptions': ['assumption 1', 'assumption 2']}, 
        #                         'constraint2': {'expr': self.constraint_2_expr, 
        #                                         'assumptions': ['assumption 1', 'assumption 3']}
        #                         }

        self.tank = BufferTank(self.node_id, self.params, self.feed)

    # def test_build_model(self):

    #     # self.tank.build_model()
    #     # self.solver = SolverFactory('ipopt')

    def test_initialization(self):
        self.assertEqual(self.tank.node_id, self.node_id)
        self.assertEqual(self.tank.node_id, self.node_id)



# Run the tests
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

    # # the command you want to run
    # command = "pytest test_buffer_tank.py"
    # # execute the command
    # os.system(command)