import unittest
from Chem_Eng_Gym.simulation_engine.reactions.calculate_rxn_invariants import ReactionInvariants

import numpy as np
from scipy.linalg import null_space

class TestReactionInvariants(unittest.TestCase):
    def setUp(self):
        self.reactions_dict = {
            'rxn_1': {'is_type_equilibrium': True, 'catalyst': None, 'phase': 'vapour', 'stoichiometry': {'A': -2, 'B': 1}},
            'rxn_2': {'is_type_equilibrium': True, 'catalyst': None, 'phase': 'vapour', 'stoichiometry': {'B': -1, 'C': -1, 'D': 2}},
            'rxn_3': {'is_type_equilibrium': False, 'catalyst': None, 'phase': 'vapour', 'stoichiometry': {'A': -1, 'C': -1, 'E': 2}},
        }
        self.reaction_invariants = ReactionInvariants(self.reactions_dict)

    def test_build_stoichiometric_matrix(self):
        expected_stoichiometric_matrix = np.array([[-2, 1, 0, 0, 0],
                                                   [0, -1, -1, 2, 0]])
        np.testing.assert_array_equal(self.reaction_invariants.stoichiometric_matrix_equilibrium_rxns, expected_stoichiometric_matrix)

    def test_null_space_calculation(self):
        expected_stoichiometric_matrix = np.array([[-2, 1, 0, 0, 0],
                                                   [0, -1, -1, 2, 0]])
        expected_null_space = null_space(expected_stoichiometric_matrix)

        np.testing.assert_array_almost_equal(self.reaction_invariants.null_space_stoichiometric_matrix, expected_null_space)

    def test_get_reaction_invariants(self):
        expected_reaction_invariants = {'M_1': {'M_A': -0.186, 'M_B': -0.371, 'M_C': 0.874, 'M_D': 0.251, 'M_E': 0},
                                        'M_2': {'M_A': 0.371, 'M_B': 0.743, 'M_C': 0.251, 'M_D': 0.497, 'M_E': 0},
                                        'M_3': {'M_A': 0.0, 'M_B': 0.0, 'M_C': 0.0, 'M_D': 0.0, 'M_E': 1.0},}
        reaction_invariants = self.reaction_invariants.get_reaction_invariants()
        
        # Assert that each invariant vector is as expected
        for key in expected_reaction_invariants:
            for inner_key in expected_reaction_invariants[key]:
                self.assertAlmostEqual(reaction_invariants[key][inner_key], expected_reaction_invariants[key][inner_key], places=3)

# Run the tests
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
