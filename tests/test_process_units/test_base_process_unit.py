import unittest
from Chem_Eng_Gym.simulation_engine.process_units.base_process_unit import ConcreteProcessUnit

class TestConcreteProcessUnit(unittest.TestCase):
    def setUp(self):
        design_params = {'param1': 1.0, 
                         'param2': 2.0, 
                         'param3': 3.0, 
                         'param4': 4.0
                        }
        self.unit = ConcreteProcessUnit("test_unit", design_params)

    def test_initial_params(self):
        self.assertEqual(self.unit.node_id, "test_unit")
        self.assertEqual(self.unit.param1, 1.0)
        self.assertEqual(self.unit.param2, 2.0)

    # def test_input_validation(self):
    #     self.

    def test_consistent_bounds(self):
        design_params = {'param1': 1.0, 
                         'param2': 2.0, 
                         'param3': 3.0, 
                         'param4': 4.0
                        }
        self.assertEqual(set(self.unit.param_bounds.keys()), set(design_params.keys()))

    def test_modify_params(self):
        new_params = {'param1': 3.0, 'param2': 4.0}
        self.unit.modify_params(new_params)
        self.assertEqual(self.unit.param1, 3.0)
        self.assertEqual(self.unit.param2, 4.0)

    def test_capex(self):
        self.assertEqual(self.unit.capex, self.unit.param1 * self.unit.param2 **2)

    def test_opex(self):
        self.assertEqual(self.unit.opex, self.unit.param1 * 365)