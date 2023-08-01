import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

class Visualiser:

    @staticmethod
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

    @staticmethod
    def plot_flowsheet(flow_sheet):
        pos = nx.spring_layout(flow_sheet.graph)
        nx.draw(flow_sheet.graph, pos, with_labels=True, node_color='skyblue', node_size=1500, edge_color='k')
        plt.show()
