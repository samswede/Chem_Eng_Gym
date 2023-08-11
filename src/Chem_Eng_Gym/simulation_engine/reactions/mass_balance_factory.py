'''
TO DO:
    - may be best to remove the self. variables within the init. (what is the official name of a self variable?)
'''

from pyomo.environ import *
# ConcreteModel, Var, Param, Constraint, Reals, NonNegativeReals, ContinuousSet
from pyomo.dae import *
# DerivativeVar

class MassBalanceFactory:
    """
    A class to create mass balance equations for a given set of reactions.

    Attributes:
        reactions_dict (dict): Dictionary containing reaction information.
        feed_rate (float): Feed rate of the system.
        feed_composition (object): Pyomo object containing feed composition.
    """

    def __init__(self, reactions_dict, feed_rate, feed_composition):
        self.reactions_dict = reactions_dict
        self.feed_rate = feed_rate
        self.feed_composition = feed_composition

    def create_mass_balance(self, model, t, component):
        """Create mass balance equation for a given component."""
        dMdt = getattr(model, 'dMdt_' + component)[t]
        Fin_xi = self.feed_rate * getattr(self.feed_composition, 'x_' + component)[t]
        reactions = sum(model.r[rxn, t] * coeff['stoichiometry'].get(component, 0) for rxn, coeff in self.reactions_dict.items())
        return dMdt == Fin_xi + reactions


def define_components(model, components):
    """Define components and their time derivatives."""
    for component in components:
        M = Var(model.t, domain=NonNegativeReals)
        dMdt = DerivativeVar(M, wrt=model.t)
        setattr(model, 'M_' + component, M)
        setattr(model, 'dMdt_' + component, dMdt)


def main():
    # Define reaction information
    reactions_dict = {
        'rxn_1': {'is_type_equilibrium': True, 'catalyst': None, 'phase': 'vapour', 'stoichiometry': {'A': -2, 'B': 1}},
        'rxn_2': {'is_type_equilibrium': True, 'catalyst': None, 'phase': 'vapour', 'stoichiometry': {'B': -1, 'C': -1, 'D': 2}},
        'rxn_3': {'is_type_equilibrium': False, 'catalyst': None, 'phase': 'vapour', 'stoichiometry': {'A': -1, 'C': -1, 'E': 2}},
    }

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

    # Create mass balance factory
    mass_balance_factory = MassBalanceFactory(reactions_dict, model.F_in, model)

    # Define mass balance equations
    for component in components:
        def mass_balance_rule(model, t, component=component):
            return mass_balance_factory.create_mass_balance(model, t, component)
        setattr(model, 'mass_balance_' + component, Constraint(model.t, rule=mass_balance_rule))

    # Print the full Pyomo model
    model.pprint()


if __name__ == "__main__":
    main()
