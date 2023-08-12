# Create mass balance equations for the following reaction:
# R1:   2A <-> B
# R2:   B + C <-> 2D
# R3:   A + C -> 2E
'''
TO DO:

    - Need to add a test for this class
    - Need to add a test for the ReactionInvariantMassBalanceFactory class
    
    - There is no 'reaction_medium' term in the mass balance.
        - This is because I have not defined it properly yet
        - There are deeper design philosophy issues with the reaction_medium term
            - I need to think about this more
            - One option is to have a reaction_medium term for each reaction
                - This could be defined in the reaction dictionary
                - It could be included within the reaction equation

    - dMdt_{component} should not be added into the model. 
        Only reaction invariants should be differential variables
    
    - Rename constraint declaration names to be less verbose?

    - Clean up the code using TDD.

'''

from Chem_Eng_Gym.simulation_engine.reactions.mass_balance_factory import MassBalanceFactory
from Chem_Eng_Gym.simulation_engine.reactions.calculate_rxn_invariants import ReactionInvariants
from pyomo.environ import *
from pyomo.dae import *


class ReactionInvariantMassBalanceFactory(MassBalanceFactory):
    def __init__(self, reactions_dict, feed_rate, feed_composition, reaction_invariants):
        super().__init__(reactions_dict, feed_rate, feed_composition)
        self.reaction_invariants = reaction_invariants
        self.threshold = 1.0e-6
    # Create a new method to define the reaction invariant mass variables
    def define_reaction_invariant_masses(self, model):  
        for invariant_name in self.reaction_invariants.keys():
            setattr(model, invariant_name, Var(model.t, domain=Reals))
            M_invariant = getattr(model, invariant_name)
            dMdt_invariant = DerivativeVar(M_invariant, wrt=model.t)
            setattr(model, 'dMdt_' + invariant_name, dMdt_invariant)

    def create_reaction_invariant_mass_balance(self, model, t, invariant_name):
        coefficients = self.reaction_invariants[invariant_name]
        dMdt_invariant = getattr(model, 'dMdt_' + invariant_name)[t]  # Change here to match the invariant_name
        Fin_xi_invariant = sum(coefficients[comp] * self.feed_rate * getattr(self.feed_composition, 'x_' + comp[2:])[t] for comp in coefficients)
        
        # Compute the combined coefficients for each reaction
        reaction_combined_coefficients = {}
        for rxn, coeff in self.reactions_dict.items():
            combined_coefficient = sum(coeff['stoichiometry'].get(comp[2:], 0) * coefficients[comp] for comp in coefficients)
            reaction_combined_coefficients[rxn] = combined_coefficient

        # Apply the threshold check and build the expression
        reactions_invariant = 0
        for rxn, combined_coefficient in reaction_combined_coefficients.items():
            if abs(combined_coefficient) > self.threshold:
                reactions_invariant += model.r[rxn, t] * combined_coefficient


        return dMdt_invariant == Fin_xi_invariant + reactions_invariant

    def define_invariant_mass_equations(self, model):
        def invariant_mass_equation_rule(model, t, invariant_name):
            coefficients = self.reaction_invariants[invariant_name]
            return getattr(model, invariant_name)[t] == sum(coefficients[comp] * getattr(model, comp)[t] for comp in coefficients)

        for invariant_name in self.reaction_invariants.keys():
            setattr(model, 'invariant_mass_equation_' + invariant_name, Constraint(model.t, rule=lambda model, t: invariant_mass_equation_rule(model, t, invariant_name)))

    def create_all_reaction_invariant_mass_balances(self, model):
        # Define the invariant masses
        for invariant_name in self.reaction_invariants.keys():
            setattr(model, invariant_name, Var(model.t, domain=Reals))  # Add new variables for invariant masses
            setattr(model, 'dMdt_' + invariant_name, DerivativeVar(getattr(model, invariant_name), wrt=model.t))  # Add time derivatives for invariant masses

        self.define_invariant_mass_equations(model)
        for t in model.t:
            for invariant_name in self.reaction_invariants.keys():
                invariant_constraint = self.create_reaction_invariant_mass_balance(model, t, invariant_name)
                setattr(model, 'reaction_invariant_mass_balance_' + invariant_name + str(t), Constraint(rule=lambda model: invariant_constraint))

def define_components(model, components):
    """Define components and their time derivatives."""
    for component in components:
        M = Var(model.t, domain=NonNegativeReals)
        dMdt = DerivativeVar(M, wrt=model.t)
        setattr(model, 'M_' + component, M)
        setattr(model, 'dMdt_' + component, dMdt)


# ...
def main():

    # Define reaction information
    reactions_dict = {
        'rxn_1': {'is_type_equilibrium': True, 'catalyst': None, 'phase': 'vapour', 'stoichiometry': {'A': -2, 'B': 1}},
        'rxn_2': {'is_type_equilibrium': True, 'catalyst': None, 'phase': 'vapour', 'stoichiometry': {'B': -1, 'C': -1, 'D': 2}},
        'rxn_3': {'is_type_equilibrium': False, 'catalyst': None, 'phase': 'vapour', 'stoichiometry': {'A': -1, 'C': -1, 'E': 2}},
    }

    # Define reaction information
    ri = ReactionInvariants(reactions_dict)
    ri.print_reaction_invariants()
    ri.verify_reaction_invariants()

    reaction_invariants = ri.get_reaction_invariants()
    print(reaction_invariants)
    # reaction_invariants = { 'M_1': {'A': -0.186, 'B': -0.371, 'C': 0.874, 'D': 0.251, 'E': 0},
    #                         'M_2': {'A': 0.371, 'B': 0.743, 'C': 0.251, 'D': 0.497, 'E': 0},
    #                         'M_3': {'A': 0.0, 'B': 0.0, 'C': 0.0, 'D': 0.0, 'E': 1.0}}

    # Define feed composition
    feed_composition = {'A': 0.1, 'B': 0.2, 'C': 0.3, 'D': 0.2, 'E': 0.2}

    # Create Pyomo model
    model = ConcreteModel()

    # Time bounds
    t_f = 4  # hours
    model.t = ContinuousSet(bounds=(0, t_f))

    # Define reaction rates
    model.r = Var(reactions_dict.keys(), model.t, domain=Reals)

    # Define components
    components = feed_composition.keys()
    define_components(model, components)

    # Define feed rate
    model.F_in = Param(initialize=10)  # in kmol per hour

    # Define feed composition
    for component, x_i in feed_composition.items():
        setattr(model, 'x_' + component, Param(model.t, initialize=x_i))

    mass_balance_factory = ReactionInvariantMassBalanceFactory(reactions_dict, model.F_in, model, reaction_invariants)
    mass_balance_factory.create_all_reaction_invariant_mass_balances(model)

    # Print the full Pyomo model
    model.pprint()

if __name__ == "__main__":
    main()
