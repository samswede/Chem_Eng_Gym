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

    def test_input_validation_in_bounds(self):
        valid_inputs = {'param1': 3.0, 
                        'param2': 2.0, 
                        'param3': 3.0, 
                        'param4': 4.0
                       }
        # This should not raise an exception
        self.unit._input_validation(valid_inputs)

    def test_input_validation_out_of_bounds(self):
        out_of_bounds_inputs = {'param1': 6.0}  # 6.0 is outside the bounds (0, 5) for param1
        with self.assertRaises(ValueError) as context:
            self.unit._input_validation(out_of_bounds_inputs)
        self.assertTrue('is out of bounds' in str(context.exception))

    def test_input_validation_unrecognized_param(self):
        unrecognized_param_inputs = {'param5': 1.0}  # 'param5' is not a recognized parameter
        with self.assertRaises(ValueError) as context:
            self.unit._input_validation(unrecognized_param_inputs)
        self.assertTrue('is not recognized' in str(context.exception))

    def test_capex(self):
        self.assertEqual(self.unit.capex, self.unit.param1 * self.unit.param2 **2)
        self.assertTrue(isinstance(self.unit.capex, float))

    def test_opex(self):
        self.assertEqual(self.unit.opex, self.unit.param1 * 365)
        self.assertTrue(isinstance(self.unit.opex, float))

# Run the tests
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)