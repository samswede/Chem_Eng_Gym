# Create mass balance equations for the following reaction:
# R1:   2A <-> B
# R2:   B + C <-> 2D
# R3:   A + C -> 2E

class ReactionInvariantMassBalanceFactory(MassBalanceFactory):
    def __init__(self, reactions_dict, feed_rate, feed_composition, reaction_invariants):
        super().__init__(reactions_dict, feed_rate, feed_composition)
        self.reaction_invariants = reaction_invariants

    def create_reaction_invariant_mass_balance(self, model, t, invariant_name):
        coefficients = self.reaction_invariants[invariant_name]
        dMdt_invariant = DerivativeVar(sum(coefficients[comp] * getattr(model, 'M_' + comp)[t] for comp in coefficients), wrt=model.t)
        Fin_xi_invariant = sum(coefficients[comp] * self.feed_rate * getattr(self.feed_composition, 'x_' + comp)[t] for comp in coefficients)
        reactions_invariant = sum(model.r[rxn, t] * sum(coeff['stoichiometry'].get(comp, 0) * coefficients[comp] for comp in coefficients) for rxn, coeff in self.reactions_dict.items())
        return dMdt_invariant == Fin_xi_invariant + reactions_invariant

    def create_all_reaction_invariant_mass_balances(self, model, t):
        for invariant_name in self.reaction_invariants.keys():
            invariant_constraint = self.create_reaction_invariant_mass_balance(model, t, invariant_name)
            setattr(model, 'reaction_invariant_mass_balance_' + invariant_name, Constraint(model.t, rule=lambda model, t: invariant_constraint))

# ...
def main():

    # Define reaction information
    reaction_invariants = {'M_1': {'A': -0.186, 'B': -0.371, 'C': 0.874, 'D': 0.251, 'E': 0},
                       'M_2': {'A': 0.371, 'B': 0.743, 'C': 0.251, 'D': 0.497, 'E': 0},
                       'M_3': {'A': 0.0, 'B': 0.0, 'C': 0.0, 'D': 0.0, 'E': 1.0}}

    # Create Pyomo model
    model = ConcreteModel()

    # Time bounds
    t_f = 4  # hours
    model.t = ContinuousSet(bounds=(0, t_f))

    # Create feed composition
    model.F_in = Param(initialize=10)  # mol / hr


    mass_balance_factory = ReactionInvariantMassBalanceFactory(reactions_dict, model.F_in, model, reaction_invariants)
    mass_balance_factory.create_all_reaction_invariant_mass_balances(model, t)

    # Print the full Pyomo model
    model.pprint()
