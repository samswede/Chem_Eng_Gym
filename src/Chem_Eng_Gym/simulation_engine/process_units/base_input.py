from pydantic import BaseModel, Field, NonNegativeFloat, NonNegativeInt, conset
from typing import Dict, Any, Set

class ConcreteExample():
    def __init__(self):
        self.node_id = "T01"

        # include units, and definition within params.
        #self.type_params = Dict(str: Dict(str: Any))
        self.params = {  
                    'param':    {'value': float, 'units': str, 'domain': str, 'bounds': set,
                                'definition': str},
                    'A':        {'value': 1.0, 'units': 'm^2', 'domain': str, 'bounds': set,
                                'definition': 'area of vessel base'}, 
                    'alpha':    {'value': 10.0, 'units': 'kg s^-1 m^-0.5', 'domain': str, 'bounds': set,
                                'definition': 'outlet rate flowrate coefficient'}, 
                    'rho':      {'value': 1000.0, 'units': 'kg m^-3', 'domain': str, 'bounds': set,
                                'definition': 'mass density of water'}
                }
        
        self.feed = {
                'temperature': 300.0,
                'pressure': 1.0,
                'total_mass': 100.0, 'total_moles': 50.0, 
                'total_mass_enthalpy': 100.0, 'total_molar_enthalpy': 100.0,

                'vapour_phase': {   'component_A': {'mass_flowrate': 100.0, 'mass_fraction': 1.0, 
                                                    'molar_flowrate': 50.0, 'molar_fraction': 1.0,
                                                    'mass_enthalpy': 100, 'molar_enthalpy': 100}
                                },
                'liquid_phase': {   'component_A': {'mass_flowrate': 100.0, 'mass_fraction': 1.0, 
                                                    'molar_flowrate': 50.0, 'molar_fraction': 1.0,
                                                    'mass_enthalpy': 100, 'molar_enthalpy': 100},
                                    'component_B': {'mass_flowrate': 100.0, 'mass_fraction': 1.0, 
                                                    'molar_flowrate': 50.0, 'molar_fraction': 1.0,
                                                    'mass_enthalpy': 100, 'molar_enthalpy': 100}
                                },
                'solid_phase': {
                                },
            }
        

        # Specify the variable data
        self.variable_data = {
                                'var1': {'type': 'algebraic', 'init': 1.0, 'domain': NonNegativeReals, 'bounds': (0.0, 5.0), 
                                            'definition': ''}, 
                                'var2': {'type': 'algebraic', 'init': 2.0, 'domain': NonNegativeReals, 'bounds': (0.0, 5.0), 
                                            'definition': ''},
                                'var3': {'type': 'differential', 'initial_condition': 0.0, 'init': 1.0, 'domain': NonNegativeReals, 'bounds': (0.0, 5.0), 
                                            'definition': ''},
                                'var4': {'type': 'differential', 'initial_condition': 0.0, 'init': 2.0, 'domain': NonNegativeReals, 'bounds': (0.0, 5.0), 
                                            'definition': ''}
                            }

        # self.constraint_data =    {
        #                         'constraint1': {'expr': self.constraint_1_expr, 
        #                                         'assumptions': ['assumption 1', 'assumption 2']}, 
        #                         'constraint2': {'expr': self.constraint_2_expr, 
        #                                         'assumptions': ['assumption 1', 'assumption 3']}
            #                         }

class Param(BaseModel):
    value: float = Field(...)
    units: str = Field(...)
    domain: str = Field(...)
    bounds: Set[float] = Field(...)
    definition: str = Field(...)

class ComponentData(BaseModel):
    mass_flowrate: float = Field(...)
    mass_fraction: float = Field(...)
    molar_flowrate: float = Field(...)
    molar_fraction: float = Field(...)
    mass_enthalpy: float = Field(...)
    molar_enthalpy: float = Field(...)

class Phase(BaseModel):
    str: ComponentData

class Feed(BaseModel):
    temperature: float = Field(...)
    pressure: float = Field(...)
    total_mass: float = Field(...)
    total_moles: float = Field(...)
    total_mass_enthalpy: float = Field(...)
    total_molar_enthalpy: float = Field(...)
    vapour_phase: Phase = Field(default_factory=dict)
    liquid_phase: Dict[str, ComponentData] = Field(default_factory=dict)
    solid_phase: Dict[str, ComponentData] = Field(default_factory=dict)

class VariableData(BaseModel):
    type: str = Field(...)
    init: float = Field(...)
    domain: str = Field(...)
    bounds: Set[float] = Field(...)
    definition: str = Field(...)
    initial_condition: float = Field(None)

class TankModel(BaseModel):
    node_id: str = Field(...)
    params: Dict[str, Param] = Field(...)
    feed: Feed
    variable_data: Dict[str, VariableData] = Field(...)
    tank: Any

# Now you can instantiate the model and it will automatically validate the input:
model = TankModel(
    node_id="T01",
    params={
        'param': {'value': 1.0, 'units': 'm^2', 'domain': 'domain', 'bounds': {0.0, 5.0},
                  'definition': 'definition'},
        'A': {'value': 1.0, 'units': 'm^2', 'domain': 'domain', 'bounds': {0.0, 5.0},
              'definition': 'area of vessel base'},
        'alpha': {'value': 10.0, 'units': 'kg s^-1 m^-0.5', 'domain': 'domain', 'bounds': {0.0, 5.0},
                  'definition': 'outlet rate flowrate coefficient'},
        'rho': {'value': 1000.0, 'units': 'kg m^-3', 'domain': 'domain', 'bounds': {0.0, 5.0},
                'definition': 'mass density of water'}
    },
    feed=Feed(
        temperature=300.0,
        pressure=1.0,
        total_mass=100.0,
        total_moles=50.0,
        total_mass_enthalpy=100.0,
        total_molar_enthalpy=100.0,
        vapour_phase=Phase(component_C=ComponentData(
            mass_flowrate=100.0,
            mass_fraction=1.0,
            molar_flowrate=50.0,
            molar_fraction=1.0,
            mass_enthalpy=100,
            molar_enthalpy=100
        )),
        liquid_phase={
            'component_A': ComponentData(
                mass_flowrate=100.0,
                mass_fraction=1.0,
                molar_flowrate=50.0,
                molar_fraction=1.0,
                mass_enthalpy=100,
                molar_enthalpy=100
            ),
            'component_B': ComponentData(
                mass_flowrate=100.0,
                mass_fraction=1.0,
                molar_flowrate=50.0,
                molar_fraction=1.0,
                mass_enthalpy=100,
                molar_enthalpy=100
            )
        }
    ),
    variable_data={
        'var1': {'type': 'algebraic', 'init': 1.0, 'domain': 'NonNegativeReals', 'bounds': {0.0, 5.0},
                 'definition': ''},
        'var2': {'type': 'algebraic', 'init': 2.0, 'domain': 'NonNegativeReals', 'bounds': {0.0, 5.0},
                 'definition': ''},
        'var3': {'type': 'differential', 'initial_condition': 0.0, 'init': 1.0, 'domain': 'NonNegativeReals',
                 'bounds': {0.0, 5.0}, 'definition': ''},
        'var4': {'type': 'differential', 'initial_condition': 0.0, 'init': 2.0, 'domain': 'NonNegativeReals',
                 'bounds': {0.0, 5.0}, 'definition': ''}
    },
    tank=None
)
