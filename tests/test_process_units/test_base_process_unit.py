import unittest
from src.simulation_engine.process_units.base_process_unit import ConcreteProcessUnit

class TestConcreteProcessUnit(unittest.TestCase):
    def setUp(self):
        design_params = {"param1": 1.0, "param2": 2.0}
        self.unit = ConcreteProcessUnit("test_unit", design_params)

    def test_initial_params(self):
        self.assertEqual(self.unit.id, "test_unit")
        self.assertEqual(self.unit.param1, 1.0)
        self.assertEqual(self.unit.param2, 2.0)
