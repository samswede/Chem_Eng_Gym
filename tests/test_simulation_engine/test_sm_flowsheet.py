import unittest
import os
from Chem_Eng_Gym.simulation_engine.sm_flowsheet import SMFlowSheet


class TestEOFlowSheet(unittest.TestCase):

    def setUp(self):
        # This method will be called before each test
        self.flow_sheet = SMFlowSheet()

    def test_add_tank(self):
        # Test the add_tank method
        tank = self.flow_sheet.add_tank('tank1')
        self.assertEqual(tank.name, 'tank1')
        self.assertEqual(len(self.flow_sheet.tanks), 1)

# Run the tests
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)