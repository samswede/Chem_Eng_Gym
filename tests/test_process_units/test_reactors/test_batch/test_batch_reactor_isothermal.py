import unittest
from Chem_Eng_Gym.simulation_engine.process_units.reactors.batch.batch_reactor_isothermal import BatchReactorIsothermal

from pyomo.environ import *
from pyomo.dae import *

class TestBatchReactorIsothermal(unittest.TestCase):
    def setUp(self):
        self.design_params = {'initial_concentration': 1.0, 
                              'rate_constant': 2.0
                             }
        self.node_id = "test_reactor"
        self.reactor = BatchReactorIsothermal(self.node_id, self.design_params)

        self.reactor.build_model()
        self.solver = SolverFactory('ipopt')

    def test_initialization(self):
        self.assertEqual(self.reactor.node_id, self.node_id)
        self.assertEqual(self.reactor.initial_concentration, self.design_params['initial_concentration'])
        self.assertEqual(self.reactor.rate_constant, self.design_params['rate_constant'])

    def test_model_creation(self):
        self.assertIsNotNone(self.reactor.model)

    def test_add_time_set(self):
        self.assertIn('time', self.reactor.model.component_map())
        self.assertEqual(self.reactor.model.time.value, {0, 1})  # check the values of the time set

    # def test_model_variables(self):
    #     # Assuming these are the variables you expect to be in your model
    #     expected_variables = ['var1', 'var2']

    #     # Get all variable names in the model
    #     model_variables = [var.name for var in self.reactor.model.component_objects(Var, active=True)]

    #     for var_name in expected_variables:
    #         self.assertIn(var_name, model_variables, f'Variable {var_name} not found in model.')

    # def test_model_differential_variables(self):
    #     self.assertIn('dvar1_dt', self.reactor.model.component_map())

    def test_model_variables(self):
        # Assuming these are the variables you expect to be in your model
        expected_variables = [var for var, data in self.reactor.variable_data.items() if data['type'] == 'ordinary']

        # Get all variable names in the model
        model_variables = [var.name for var in self.reactor.model.component_objects(Var, active=True) if var.name.endswith('_dt') == False]

        for var_name in expected_variables:
            self.assertIn(var_name, model_variables, f'Variable {var_name} not found in model.')

    def test_model_differential_variables(self):
        expected_differential_variables = [var for var, data in self.reactor.variable_data.items() if data['type'] == 'differential']

        # Get all differential variable names in the model
        model_variables = [var.name for var in self.reactor.model.component_objects((DerivativeVar), active=True) if var.name.endswith('_dt')]

        for var_name in expected_differential_variables:
            self.assertIn(f'd{var_name}_dt', model_variables, f'Differential variable {var_name}_dt not found in model.')
    
    def test_count_model_differential_variables(self):
        # Compute expected number of differential variables
        expected_num_diff_vars = sum(1 for var, data in self.reactor.variable_data.items() if data['type'] == 'differential')

        # Count all differential variables in the model
        actual_num_diff_vars = sum(1 for var in self.reactor.model.component_objects(DerivativeVar, active=True))

        # Assert that expected and actual numbers match
        self.assertEqual(expected_num_diff_vars, actual_num_diff_vars, f'The number of differential variables in the model is incorrect.')

    def test_count_model_algebraic_variables(self):
        # Compute expected number of algebraic variables
        expected_num_alg_vars = sum(1 for var, data in self.reactor.variable_data.items() if data['type'] == 'algebraic')

        # Count all variables in the model that are not DerivativeVars
        actual_num_alg_vars = sum(1 for var in self.reactor.model.component_objects(Var, active=True) 
                                if not any(isinstance(v, DerivativeVar) for v in var.values()))

        # Assert that expected and actual numbers match
        self.assertEqual(expected_num_alg_vars, actual_num_alg_vars, f'The number of algebraic variables in the model is incorrect.')


    def test_model_variable_types(self):
        expected_differential_variables = [var for var, data in self.reactor.variable_data.items() if data['type'] == 'differential']
        for var_name in expected_differential_variables:
            self.assertTrue(isinstance(getattr(self.reactor.model, f'd{var_name}_dt'), DerivativeVar), f'Variable {var_name} is not of type DerivativeVar.')

        expected_algebraic_variables = [var for var, data in self.reactor.variable_data.items() if data['type'] == 'algebraic']
        for var_name in expected_algebraic_variables:
            self.assertTrue(isinstance(getattr(self.reactor.model, var_name), Var), f'Variable {var_name} is not of type Var.')


    def test_model_constraints(self):
        # Check that constraint1 exists in the model
        self.assertTrue(hasattr(self.reactor.model, 'constraint1'))
        
        # Check that constraint1 is indeed a Constraint
        self.assertIsInstance(self.reactor.model.constraint1, pyomo.core.base.constraint.SimpleConstraint)
        
        # # Check the lower and upper bounds of the constraint1
        # self.assertEqual(self.reactor.model.constraint1.lower(), 0.0)
        # self.assertEqual(self.reactor.model.constraint1.upper(), None)

    # def test_model_differential_equations(self):
    #     self.assertIn('dCa_eq', self.reactor.model.component_map())

    # def test_model_solve(self):
    #     results = self.solver.solve(self.reactor.model, tee=False)
    #     self.assertEqual(results.solver.status, SolverStatus.ok)

    # def test_model_constraints(self):
    #     list_constraints = ['rate_eq']
    #     for constraint in list_constraints:
    #         self.assertIn(constraint, self.reactor.model.component_map(Constraint))

    # def test_model_equation(self):
    #     self.reactor.model.k.fix(1.0)  # fix the rate constant to simplify the problem
    #     self.reactor.model.C[0].fix(1.0)  # fix initial concentration

    #     # Solve the model
    #     results = self.solver.solve(self.reactor.model, tee=False)
    #     self.assertEqual(results.solver.status, SolverStatus.ok)

    #     # Assuming the solution should approach zero as time goes to infinity (simple first order reaction)
    #     # We check the final concentration
    #     final_time = max(self.reactor.model.t)
    #     self.assertAlmostEqual(self.reactor.model.C[final_time].value, 0.0, places=2)
