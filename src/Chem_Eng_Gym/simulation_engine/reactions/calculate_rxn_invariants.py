# Solving for rxn invariants

# Given following reactions, calculate the rxn invariants:
# R1:   2A <-> B
# R2:   B + C <-> 2D
# R3:   A + C -> 2E

# FORMULA

import numpy as np
from scipy.linalg import null_space
'''
TO DO:
    - REMOVE round(value, 3) from method get_reaction_invariants() because it will fuck things up later.
        - Will require fixing test as well

    - Convert reactions dict into a reaction network for perception by the agent
        - and vice versa. Should be interchangeable.
'''

class ReactionInvariants:
    def __init__(self, reactions_dict):
        self.reactions_dict = reactions_dict
        self.stoichiometric_matrix_equilibrium_rxns = self._build_stoichiometric_matrix()
        self.null_space_stoichiometric_matrix = self._calculate_null_space()

    def _build_stoichiometric_matrix(self):
        stoichiometric_matrix = []
        for rxn_key, rxn_details in self.reactions_dict.items():
            if rxn_details['is_type_equilibrium']:
                rxn_vector = [rxn_details['stoichiometry'].get(species, 0) for species in ['A', 'B', 'C', 'D', 'E']]
                stoichiometric_matrix.append(rxn_vector)
        return np.array(stoichiometric_matrix)

    def _calculate_null_space(self):
        return null_space(self.stoichiometric_matrix_equilibrium_rxns)

    def print_reaction_invariants(self):
        print(f"Null space of A: \n {self.null_space_stoichiometric_matrix}")

    def verify_reaction_invariants(self):
        verification_result = self.stoichiometric_matrix_equilibrium_rxns @ self.null_space_stoichiometric_matrix
        print("Verification (should be close to zero):")
        print(verification_result)

    def return_reaction_invariants(self):
        return self.null_space_stoichiometric_matrix

    def get_reaction_invariants(self):
        reaction_invariants = {}
        species = ['A', 'B', 'C', 'D', 'E']
        
        # Iterate through each column of the null_space_stoichiometric_matrix
        for idx, invariant_vector in enumerate(self.null_space_stoichiometric_matrix.T):
            invariant_dict = {}
            for species_idx, value in enumerate(invariant_vector):
                invariant_dict[f'M_{species[species_idx]}'] = round(value, 32)
            reaction_invariants[f'M_{idx + 1}'] = invariant_dict

        return reaction_invariants


# Usage
reactions_dict = {
    'rxn_1': {'is_type_equilibrium': True, 'catalyst': None, 'phase': 'vapour', 'stoichiometry': {'A': -2, 'B': 1}},
    'rxn_2': {'is_type_equilibrium': True, 'catalyst': None, 'phase': 'vapour', 'stoichiometry': {'B': -1, 'C': -1, 'D': 2}},
    'rxn_3': {'is_type_equilibrium': False, 'catalyst': None, 'phase': 'vapour', 'stoichiometry': {'A': -1, 'C': -1, 'E': 2}},
}

ri = ReactionInvariants(reactions_dict)
ri.print_reaction_invariants()
ri.verify_reaction_invariants()

reaction_invariants = ri.get_reaction_invariants()
print("Reaction Invariants:")
print(reaction_invariants)

reaction_invariants = {'M_1' : {'M_A': -0.186, 'M_B': -0.371, 'M_C': 0.874, 'M_D': 0.251, 'M_E': 0},
                       'M_2' : {'M_A': 0.371, 'M_B': 0.743, 'M_C': 0.251, 'M_D': 0.497, 'M_E': 0},
                       'M_3' : {'M_A': 0.0, 'M_B': 0.0, 'M_C': 0.0, 'M_D': 0.0, 'M_E': 1.0}}

# reactions_dict = {'rxn_1' : {'type_equilibrium': True, 'catalyst': None, 'phase': 'vapour',
#                              'stoichiometry' : {'A': -2, 'B': 1}},
#                   'rxn_2' : {'type_equilibrium': True, 'catalyst': None, 'phase': 'vapour',
#                              'stoichiometry' : {'B': -1, 'C': -1, 'D': 2}},
#                   'rxn_3' : {'type_equilibrium': False, 'catalyst': None, 'phase': 'vapour',
#                              'stoichiometry' : {'A': 1, 'C': 1, 'E': 2}},}

# rxn_vector_1 = np.array([-2, 1, 0, 0, 0])
# rxn_vector_2 = np.array([0, -1, -1, 2, 0])
# rxn_vector_3 = np.array([-1, 0, -1, 0, 2])

# stoichiometric_matrix_equilibrium_rxns = np.array([rxn_vector_1,
#                                   rxn_vector_2])
                                  

# # Find the null space
# null_space_stoichiometric_matrix = null_space(stoichiometric_matrix_equilibrium_rxns)

# # Print the result
# print(f"Null space of A: \n {null_space_stoichiometric_matrix}")

# # Verify the result by multiplying A by the null space vectors
# print("Verification (should be close to zero):")
# print(stoichiometric_matrix_equilibrium_rxns @ null_space_stoichiometric_matrix)

