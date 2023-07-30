import pandas as pd
import seaborn as sns
import plotly.graph_objects as go

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
    m.ic1 = Constraint(expr=m.x[0] == 40)
    m.ic2 = Constraint(expr=m.y[0] == 9)

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

def plot_results_plotly(df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df['t'], y=df['x'], mode='lines', name='Prey'))
    fig.add_trace(go.Scatter(x=df['t'], y=df['y'], mode='lines', name='Predator'))

    fig.update_layout(title='Population over time', xaxis_title='Time', yaxis_title='Population')

    fig.show()

def plot_results_seaborn(df):
    f, axes = plt.subplots(nrows=2, figsize=(7, 7))

    sns.lineplot(x=df['t'], y=df['x'], ax=axes[0]).set_title('Prey over time')
    sns.lineplot(x=df['t'], y=df['y'], ax=axes[1]).set_title('Predator over time')

    plt.tight_layout()
    plt.show()

# Usage:
m = setup_model()
m = solve_model(m)

df = extract_results(m)
plot_results_seaborn(df)
plot_results_plotly(df)
