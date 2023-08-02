import datetime
import os
import pandas as pd
from pyomo.environ import Var, Objective, value

import networkx as nx
from networkx.readwrite import json_graph
import json

# class Simulator:
#     def __init__(self):
#         self.data_handler = DataHandler()

#     def simulate(self, simulation_name):
#         # Placeholder for simulation logic
#         output, parameters, notes, plot = "...", "...", "...", "..."
        
#         # Save simulation results
#         self.data_handler.save_simulation_files(simulation_name, output, parameters, notes, plot)


class SimulationFileManager:
    def __init__(self, base_dir='/Users/samuelandersson/Dev/github_projects/Chem_Eng_Gym/src/Chem_Eng_Gym/data/simulations'):
        self.base_dir = base_dir

    def extract_results_from_model(self, pyomo_model):
        # Extract time data
        data = {'t': [t for t in pyomo_model.t]}

        # Extract variable data into a dictionary
        for v in pyomo_model.component_objects(Var, active=True):
            var_name = str(v)
            data[var_name] = [value(v[t]) for t in pyomo_model.t]

        # Include the objective function value, if there is one
        for o in pyomo_model.component_objects(Objective, active=True):
            obj_name = str(o)
            if o.is_indexed():
                data[obj_name] = [value(o[t]) if t in o else float('nan') for t in pyomo_model.t]
            else:
                data[obj_name] = value(o)

        # Convert dictionary to DataFrame
        df = pd.DataFrame(data)
        
        # Return DataFrame
        return df

    def get_directory_structure(self, simulation_name):
        now = datetime.now()
        year = now.strftime('%Y')
        month = now.strftime('%m_%B')
        day = now.strftime('%d')
        time = now.strftime('%H%M')

        return os.path.join(self.base_dir, year, month, day, f'{simulation_name}_{time}')

    def save_simulation_files(self, simulation_name, output, parameters, notes, plot):
        """
        Saves simulation files in a structured directory.

        This function takes the name of the simulation, output data, parameters, 
        notes, and a plot, then writes these into appropriately named files. The 
        files are saved in a directory structure organized by the current date and 
        time, down to the minute. The directory structure is as follows:

        Simulations/YYYY/MM_Month/DD/simulation_name_HHMM/

        Args:
            simulation_name (str): The name of the simulation.
            output (str): The output data of the simulation in string format. 
                Typically this would be the contents of 'output.csv'.
            parameters (str): The parameters used in the simulation in string 
                format. Typically this would be the contents of 'parameters.json'.
            notes (str): Any additional notes or metadata in string format. 
                Typically this would be the contents of 'notes.txt'.
            plot (bytes): A byte string representing a plot image. Typically this 
                would be the contents of 'plot.png'.

        Returns:
            None
        """
        dir_structure = self.get_directory_structure(simulation_name)

        if not os.path.exists(dir_structure):
            os.makedirs(dir_structure)

        # Placeholder functions to create files
        output_file_path = os.path.join(dir_structure, 'output.csv')
        with open(output_file_path, 'w') as f:
            f.write(output)

        parameters_file_path = os.path.join(dir_structure, 'parameters.json')
        with open(parameters_file_path, 'w') as f:
            f.write(parameters)

        notes_file_path = os.path.join(dir_structure, 'notes.txt')
        with open(notes_file_path, 'w') as f:
            f.write(notes)

        plot_file_path = os.path.join(dir_structure, 'plot.png')
        with open(plot_file_path, 'wb') as f:
            f.write(plot)

    # Add a load function here to load data if necessary
    # def load_simulation_files(self, dir_structure):
    #     ...

    def save_flowsheet_graph(self, filename, networkx_graph):
        data = json_graph.node_link_data(networkx_graph)
        with open(filename, 'w') as f:
            json.dump(data, f)

