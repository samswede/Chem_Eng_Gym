import unittest
from pyomo.environ import *
from pyomo.dae import *
from Chem_Eng_Gym.simulation_engine.reactions.calculate_rxn_invariants import ReactionInvariants
from Chem_Eng_Gym.simulation_engine.reactions.reaction_invariant_factory import ReactionInvariantMassBalanceFactory

class TestReactionInvariantMassBalanceFactory(unittest.TestCase):
    
    def setUp(self):
        # Define reaction information similar to what's used in the main code
        self.reactions_dict = {
            'rxn_1': {'is_type_equilibrium': True, 'catalyst': None, 'phase': 'vapour', 'stoichiometry': {'A': -2, 'B': 1}},
            'rxn_2': {'is_type_equilibrium': True, 'catalyst': None, 'phase': 'vapour', 'stoichiometry': {'B': -1, 'C': -1, 'D': 2}},
            'rxn_3': {'is_type_equilibrium': False, 'catalyst': None, 'phase': 'vapour', 'stoichiometry': {'A': -1, 'C': -1, 'E': 2}},
        }
        ri = ReactionInvariants(self.reactions_dict)
        self.reaction_invariants = ri.get_reaction_invariants()
        self.feed_composition = {'A': 0.1, 'B': 0.2, 'C': 0.3, 'D': 0.2, 'E': 0.2}
        self.model = ConcreteModel()
        self.model.t = ContinuousSet(bounds=(0, 4))  # hours
        self.model.r = Var(self.reactions_dict.keys(), self.model.t, domain=Reals)
        self.model.F_in = Param(initialize=10)  # in kmol per hour
        
        for component, x_i in self.feed_composition.items():
            setattr(self.model, 'x_' + component, Param(self.model.t, initialize=x_i))

        # Define components
        components = self.feed_composition.keys()
        self.define_components(self.model, components)

        self.factory = ReactionInvariantMassBalanceFactory(self.reactions_dict, self.model.F_in, self.model, self.reaction_invariants)

    def define_components(self, model, components):
        """Define components and their time derivatives."""
        for component in components:
            M = Var(model.t, domain=NonNegativeReals)
            dMdt = DerivativeVar(M, wrt=model.t)
            setattr(model, 'M_' + component, M)
            setattr(model, 'dMdt_' + component, dMdt)

    def test_define_reaction_invariant_masses(self):
        self.factory.define_reaction_invariant_masses(self.model)
        # Test if invariant masses and their derivatives are defined in the model
        for invariant_name in self.reaction_invariants.keys():
            self.assertIn(invariant_name, self.model.component_objects(Var))
            self.assertIn('dMdt_' + invariant_name, self.model.component_objects(Var))

    def test_create_reaction_invariant_mass_balance(self):
        self.factory.define_reaction_invariant_masses(self.model)
        for t in self.model.t:
            for invariant_name in self.reaction_invariants.keys():
                constraint_expr = self.factory.create_reaction_invariant_mass_balance(self.model, t, invariant_name)
                # You may add specific checks based on the expected expression for different invariants and time points
                
    def test_create_all_reaction_invariant_mass_balances(self):
        self.factory.create_all_reaction_invariant_mass_balances(self.model)
        # Test if all constraints for invariant masses are created
        for t in self.model.t:
            for invariant_name in self.reaction_invariants.keys():
                self.assertIn('reaction_invariant_mass_balance_' + invariant_name + str(t), self.model.component_objects(Constraint))

    def test_define_invariant_mass_equations(self):
        self.factory.create_all_reaction_invariant_mass_balances(self.model)
        # Test if invariant mass equations are defined
        for invariant_name in self.reaction_invariants.keys():
            self.assertIn('invariant_mass_equation_' + invariant_name, self.model.component_objects(Constraint))


# Run the tests
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
