
# Create Base Class
class CustomFunction:
    def evaluate(self, x):
        pass

# Create Concrete Classes
class LinearFunction(CustomFunction):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def evaluate(self, x):
        return self.a * x + self.b

class QuadraticFunction(CustomFunction):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def evaluate(self, x):
        return self.a * x**2 + self.b * x + self.c

# Create Factory Class
class FunctionFactory:
    @staticmethod
    def create_function(function_type, *args):
        if function_type == 'linear':
            return LinearFunction(*args)
        elif function_type == 'quadratic':
            return QuadraticFunction(*args)
        else:
            raise ValueError('Invalid function type')

# Use this factory in pyomo model
from pyomo.environ import *

model = ConcreteModel()
model.x = Var()

function_type = 'linear' # or 'quadratic'
function_args = (2, 3) # or (1, 2, 3) for a quadratic function
custom_function = FunctionFactory.create_function(function_type, *function_args)

def custom_constraint_rule(model):
    return custom_function.evaluate(model.x) <= 10

model.custom_constraint = Constraint(rule=custom_constraint_rule)
