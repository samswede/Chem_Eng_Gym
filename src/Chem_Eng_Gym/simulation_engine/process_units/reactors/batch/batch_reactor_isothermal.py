from Chem_Eng_Gym.simulation_engine.process_units.base_process_unit import ProcessUnit
from pyomo.environ import *
from pyomo.dae import *

from typing import Dict, Tuple, List, Any

class BatchReactorIsothermal(ProcessUnit):
    def __init__(self, node_id, design_params):

        # Specify the variable data
        self.variable_data = {
                                'var1': {'type': 'algebraic', 'init': 1.0, 'domain': NonNegativeReals, 'bounds': (0.0, 5.0)}, 
                                'var2': {'type': 'algebraic', 'init': 2.0, 'domain': NonNegativeReals, 'bounds': (0.0, 5.0)},
                                'var3': {'type': 'differential', 'initial_condition': 0.0, 'init': 1.0, 'domain': NonNegativeReals, 'bounds': (0.0, 5.0)},
                                'var4': {'type': 'differential', 'initial_condition': 0.0, 'init': 2.0, 'domain': NonNegativeReals, 'bounds': (0.0, 5.0)}
                            }

        self.constraint_data =    {
                                'constraint1': {'expr': self.constraint_1_expr, 'assumptions': ['assumption 1', 'assumption 2']}, 
                                'constraint2': {'expr': self.constraint_2_expr, 'assumptions': ['assumption 1', 'assumption 3']}
                                }
        
        self.model = None
        self.time = None

        super().__init__(node_id, design_params)

    def constraint_1_expr(self):
        return  self.model.var1 >= 0
    
    def constraint_2_expr(self):
        return  self.model.var2 >= 0

    # def constraint_1_expr(self):
    #     return  self.model.var1[0] >= 0

    # def constraint_2_expr(self):
    #     return  self.model.var2[0] >= 0


    def _input_validation(self, inputs):
        super()._input_validation(inputs)

    def _output_validation(self, outputs):
        pass  # Add your own implementation for output validation

    def modify_params(self, new_params):
        super().modify_params(new_params)

    @property
    def params(self):
        return {"param1": self.param1, "param2": self.param2}

    @property
    def capex(self):
        return self.param1 * self.param2 ** 2

    @property
    def opex(self):
        return self.param1 * 365.0

    def build_model(self) -> None:
        self.model = ConcreteModel()
        self.add_time_set()

        # Add variables to the model
        self.add_all_variables_to_model(self.variable_data)
        # self.add_differential_variables_to_model()
        # self.add_differential_equations_to_model()
        # # ... add constraints, objective function, etc...

        # Add constraints to the model
        self.add_all_constraints_to_model(self.constraint_data)

    def add_time_set(self) -> None:
        self.time = ContinuousSet(initialize=[0,1]) # you can adjust this for your needs
        self.model.time = self.time

    def add_variable_to_model(self, variable: str, var_data: Dict[str, Any]) -> None:
        setattr(self.model, variable, Var(initialize=var_data['init'], within=var_data['domain'], bounds=var_data['bounds']))

    def add_differential_variable_to_model(self, variable: str, var_data: Dict[str, Any]) -> None:
        var = Var(self.model.time, initialize=var_data['init'], within=var_data['domain'], bounds=var_data['bounds'])
        setattr(self.model, variable, var)
        dvar = DerivativeVar(var, wrt=self.model.time)
        setattr(self.model, f'd{variable}_dt', dvar)

    def add_all_variables_to_model(self, variable_data: Dict[str, Dict[str, Any]]) -> None:
        for variable, var_data in variable_data.items():
            if var_data.get('type') == 'differential':
                self.add_differential_variable_to_model(variable, var_data)
            else:
                self.add_variable_to_model(variable, var_data)

    def add_constraint_to_model(self, constraint_name: str, expr: Any) -> None:
        setattr(self.model, constraint_name, Constraint(expr=expr))

    def add_all_constraints_to_model(self, constraint_data: Dict[str, Dict[str, Any]]) -> None:
        for constraint_name, constraint_data in constraint_data.items():
            expr = constraint_data['expr']()  # Call the expression function stored in the data
            self.add_constraint_to_model(constraint_name, expr)

    def run(self, time):

        # Outputs the final concentration
        return
