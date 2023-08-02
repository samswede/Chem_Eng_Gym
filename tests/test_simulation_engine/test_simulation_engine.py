import unittest
import os
from Chem_Eng_Gym.simulation_engine import FlowSheet


class TestFlowSheet(unittest.TestCase):

    def setUp(self):
        # This method will be called before each test
        self.flow_sheet = FlowSheet()

    def test_add_tank(self):
        # Test the add_tank method
        tank = self.flow_sheet.add_tank('tank1')
        self.assertEqual(tank.name, 'tank1')
        self.assertEqual(len(self.flow_sheet.tanks), 1)

    def test_solve(self):
        # Test the solve method
        # First add a tank
        self.flow_sheet.add_tank('tank1')
        self.flow_sheet.solve()
        # You can add some assertion here to check the solve results

    # def test_save_graph(self):
    #     # Test the save_graph method
    #     self.flow_sheet.add_tank('tank1')
    #     self.flow_sheet.add_tank('tank2', feed=self.flow_sheet.tanks[0])
    #     self.flow_sheet.save_graph('test_graph.json')
    #     # Check if the file exists
    #     self.assertTrue(os.path.exists('test_graph.json'))
    #     # You can add some assertion here to check the content of the json file

    # def tearDown(self):
    #     # This method will be called after each test
    #     # Remove the json file if exists
    #     if os.path.exists('test_graph.json'):
    #         os.remove('test_graph.json')

# Run the tests
if __name__ == '__main__':
    unittest.main()
