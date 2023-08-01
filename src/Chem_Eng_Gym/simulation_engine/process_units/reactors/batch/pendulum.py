from pyomo.environ import *
from pyomo.dae import *
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go

m = ConcreteModel()

# Constants
g = 9.81  # Acceleration due to gravity
L = 1     # Length of the pendulum

# Set
m.t = ContinuousSet(bounds=(0, 100))  # Time

# Variables
m.x = Var(m.t, initialize= 0.1)  # Angle
m.v = Var(m.t)  # Angular velocity

# Derivatives
m.dxdt = DerivativeVar(m.x, wrt=m.t)
m.dvdt = DerivativeVar(m.v, wrt=m.t)

# Differential equations
m.ode1 = Constraint(m.t, rule=lambda m, t: m.dxdt[t] == m.v[t])
m.ode2 = Constraint(m.t, rule=lambda m, t: m.dvdt[t] == -g/L*sin(m.x[t]))

# Discretize model using finite difference method
discretizer = TransformationFactory('dae.finite_difference')
discretizer.apply_to(m, nfe=50, scheme='FORWARD')

# Solve the model
solver = SolverFactory('ipopt')
solver.solve(m, tee=True)

def extract_results(model):
    data = {'t': [], 'x': [], 'v': []}
    for t in model.t:
        data['t'].append(t)
        data['x'].append(value(model.x[t]))
        data['v'].append(value(model.v[t]))

    return pd.DataFrame(data)

def plot_results_plotly(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['t'], y=df['x'], mode='lines', name='Angle'))
    fig.add_trace(go.Scatter(x=df['t'], y=df['v'], mode='lines', name='Angular velocity'))
    fig.update_layout(title='Pendulum Motion over time', xaxis_title='Time')
    fig.show()

def plot_results_seaborn(df):
    f, axes = plt.subplots(nrows=2, figsize=(7, 7))
    sns.lineplot(x=df['t'], y=df['x'], ax=axes[0]).set_title('Angle over time')
    sns.lineplot(x=df['t'], y=df['v'], ax=axes[1]).set_title('Angular velocity over time')
    plt.tight_layout()
    plt.show()

# Usage:
df = extract_results(m)
plot_results_seaborn(df)
plot_results_plotly(df)
