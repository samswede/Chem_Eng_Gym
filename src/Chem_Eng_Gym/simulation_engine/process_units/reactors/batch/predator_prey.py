import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

from pyomo.environ import Var, Constraint, Objective, value
from pyomo.environ import *
from pyomo.dae import *

def setup_model():
    m = ConcreteModel()

    m.t = ContinuousSet(bounds=(0, 50))  # time period

    # Variables
    m.x = Var(m.t, domain=NonNegativeReals)  # Prey population
    m.y = Var(m.t, domain=NonNegativeReals)  # Predator population

    # Derivatives
    m.dxdt = DerivativeVar(m.x, wrt=m.t)
    m.dydt = DerivativeVar(m.y, wrt=m.t)

    # Parameters
    alpha, beta, delta, gamma = 0.1, 0.02, 0.3, 0.01

    # Initial conditions
    m.ic1 = Constraint(expr=m.x[0] == 400)
    m.ic2 = Constraint(expr=m.y[0] == 100)

    # Lotka-Volterra equations
    m.ode1 = Constraint(m.t, rule=lambda m, t: m.dxdt[t] == alpha*m.x[t] - beta*m.x[t]*m.y[t])
    m.ode2 = Constraint(m.t, rule=lambda m, t: m.dydt[t] == delta*beta*m.x[t]*m.y[t] - gamma*m.y[t])

    return m

def solve_model(m):
    discretizer = TransformationFactory('dae.finite_difference')
    discretizer.apply_to(m, nfe=500)  # discretize model using finite difference method

    solver = SolverFactory('ipopt')
    solver.solve(m, tee=True)  # solve the model

    return m

def extract_results(model):
    data = {'t': [], 'x': [], 'y': [], 'dxdt': [], 'dydt': []}
    for t in model.t:
        data['t'].append(t)
        data['x'].append(value(model.x[t]))
        data['y'].append(value(model.y[t]))
        data['dxdt'].append(value(model.dxdt[t]))
        data['dydt'].append(value(model.dydt[t]))

    return pd.DataFrame(data)


def extract_results_from_model(model):
    # Extract time data
    data = {'t': [t for t in model.t]}

    # Extract variable data into a dictionary
    for v in model.component_objects(Var, active=True):
        var_name = str(v)
        data[var_name] = [value(v[t]) for t in model.t]

    # Include the objective function value, if there is one
    for o in model.component_objects(Objective, active=True):
        obj_name = str(o)
        if o.is_indexed():
            data[obj_name] = [value(o[t]) if t in o else float('nan') for t in model.t]
        else:
            data[obj_name] = value(o)

    # Convert dictionary to DataFrame
    df = pd.DataFrame(data)
    
    # Return DataFrame
    return df





def plot_results_plotly(df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df['t'], y=df['x'], mode='lines', name='Prey'))
    fig.add_trace(go.Scatter(x=df['t'], y=df['y'], mode='lines', name='Predator'))

    fig.update_layout(title='Population over time', xaxis_title='Time', yaxis_title='Population')

    fig.show()

def plot_results_seaborn(df):
    variables = df.columns[1:]  # Skip the 't' column
    n_vars = len(variables)
    n_rows = (n_vars + 1) // 2  # Number of rows, rounded up

    fig, axes = plt.subplots(n_rows, 2, figsize=(14, n_rows*5))  # Create a subplot grid
    axes = axes.flatten()  # Flatten the 2D array of axes to easily iterate over it

    # Generate a line plot for each variable
    for i, var in enumerate(variables):
        sns.lineplot(x=df['t'], y=df[var], ax=axes[i]).set_title(f'{var} over time')

    # Remove empty subplots
    if n_vars % 2:
        fig.delaxes(axes[-1])

    plt.tight_layout()
    plt.show()


# Usage:
m = setup_model()
m = solve_model(m)

df = extract_results_from_model(m)
plot_results_seaborn(df)

