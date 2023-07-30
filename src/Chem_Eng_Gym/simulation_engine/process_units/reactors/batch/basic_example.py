import pandas as pd
import seaborn as sns
import plotly.graph_objects as go

from pyomo.environ import *
from pyomo.dae import *

def setup_model():
    m = ConcreteModel()

    m.t = ContinuousSet(bounds=(0, 10))  # time period
    m.x = Var(m.t)  # variable
    m.dxdt = DerivativeVar(m.x, wrt=m.t)  # derivative of the variable

    # Initial condition & differential equation
    m.ic = Constraint(expr=m.x[0] == 1)
    m.ode = Constraint(m.t, rule=lambda m, t: m.dxdt[t] == -m.x[t])

    return m

def solve_model(m):
    discretizer = TransformationFactory('dae.finite_difference')
    discretizer.apply_to(m, nfe=50)  # discretize model using finite difference method

    solver = SolverFactory('ipopt')
    solver.solve(m, tee=True)  # solve the model

    return m

def extract_results(model):
    data = {'t': [], 'x': [], 'dxdt': []}
    for t in model.t:
        data['t'].append(t)
        data['x'].append(value(model.x[t]))
        data['dxdt'].append(value(model.dxdt[t]))

    return pd.DataFrame(data)

def plot_results_plotly(df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df['t'], y=df['x'], mode='lines', name='x'))
    fig.add_trace(go.Scatter(x=df['t'], y=df['dxdt'], mode='lines', name='dx/dt'))

    fig.update_layout(title='Plot of x and dx/dt over time', xaxis_title='Time')

    fig.show()

def plot_results_seaborn(df):
    f, axes = plt.subplots(nrows=2, figsize=(7, 7))

    sns.lineplot(x=df['t'], y=df['x'], ax=axes[0]).set_title('x over time')
    sns.lineplot(x=df['t'], y=df['dxdt'], ax=axes[1]).set_title('dx/dt over time')

    plt.tight_layout()
    plt.show()

# Usage:
m = setup_model()
m = solve_model(m)

df = extract_results(m)
plot_results_seaborn(df)
plot_results_plotly(df)
