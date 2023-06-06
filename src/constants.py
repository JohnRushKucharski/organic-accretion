'''
Constants for accretion model.

These values are assigned from a .toml file. 
Defaults to values in morris_constants.toml, which reflects Morris & Bowden (1986).
'''
import tomllib
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass, field

MORRIS_CONSTANTS = str(Path(__file__).parent.joinpath('morris_constants.toml'))
'''String path to toml file containing constants used in Morris & Bowden (1986).'''

@dataclass(frozen=True)
class CONSTANTS:
    '''Contains constants used in simulation.'''
    file_path: str = MORRIS_CONSTANTS
    '''Path to .toml file containing constants data, set to moriss_constants.toml by default.'''
    
    init_top: float = field(init=False)
    '''Top elevation of initial cohert or layer, not a paraemeter of Morris & Bowden [in cm].'''
    init_bottom: float = field(init=False)
    '''Bottom elevation of initial cohert or layer, not a parameter of Morris & Bowden [in cm].'''

    # INORGANIC
    inorganic_density: float = field(init=False)
    '''Bulk density of inorganic material [in g/cm3]. Note: not a property of Morris and Bowden.'''
    # k3 portion ash (in Biomass parameters)
    # k4: initial inorganic deposition used to compute portion organic but not saved

    #ORGANIC MATERIAL
    organic_density: float = field(init=False)
    '''Bulk density of organic material [in g/cm3].'''
    portion_organic: float = field(init=False)
    '''Quotient of Wa(0) * (1 - k3) / (Wa(0) * (1 - k3) + Wa(0) * k3 + k4 ) [dmls].'''

    portion_refractory: float = field(init=False)
    '''f_c: Fraction of organic material that is refactory [in g/g].'''

    #BIOMASS PARAMETERS
    max_root_depth: float = field(init=False)
    '''Db(0): Maximum depth of new live biomass [in cm]'''
    biomass_distribution_parameter_k1: float = field(init=False)
    '''k1: a distribution parameter for below ground biomass [in 1/cm].'''
    init_biomass_at_surface: float = field(init=False)
    '''Ro: below ground live biomass at surface [in g/cm].'''
    portion_ash: float = field(init=False)
    '''k3: inorganic content of live plants [in g/g].'''
    natural_underground_mortality: float = field(init=False)
    '''k2: natural turnover rate for below ground biomass per year [1/yr].'''

    def __post_init__(self) -> None:
        with open(self.file_path, mode = 'rb') as file:
            data = tomllib.load(file)
            object.__setattr__(self, 'init_top', data['initial_conditions']['Du'])
            object.__setattr__(self, 'init_bottom', data['initial_conditions']['Db'])
            object.__setattr__(self, 'inorganic_density', data['bi'])
            object.__setattr__(self, 'oganic_density', data['bo'])    
            object.__setattr__(self, 'portion_organic', self.compute_portion_organic(data))

            object.__setattr__(self, 'portion_refractory', data['fc'])

            object.__setattr__(self, 'max_root_depth', data['biomass']['root_depth'])
            object.__setattr__(self, 'biomass_distribution_parameter_k1', data['biomass']['k1'])
            object.__setattr__(self, 'init_biomass_at_surface', data['biomass']['Ro'])
            object.__setattr__(self, 'portion_ash', data['biomass']['k3'])
            object.__setattr__(self, 'natural_underground_mortality', data['biomass']['k2'])

    def compute_portion_organic(self, data: Dict[str, Any]) -> float:
        '''
        Computes constant portion organic in natural deposition,
        based on initial organic deposition, inorganic deposition, 
        and portion of organic deposition that is ash.
        '''
        organic_weight = data['initial_conditions']['Wa'] * (1 - data['biomass']['k3'])
        inorganic_weight = data['initial_conditions']['k4'] + data['initial_conditions']['Wa'] - organic_weight
        return organic_weight / (organic_weight + inorganic_weight)

    def grams_to_cm3_organic(self, grams: float = 1) -> float:
        '''
        Converts weight [in g] to volume [in cm3], 
        based on assumed bulk density of organic material [in g/cm3].
        '''
        return grams * (1 / self.organic_density)

    def grams_to_cm3_inorganic(self, grams: float = 1) -> float:
        '''
        Converts weight [in g] to volume [in cm3], 
        based on assumed bulk density of inorganic material [in g/cm3].
        '''
        return grams * (1 / self.inorganic_density)

    def grams_to_cm_organic(self, grams: float = 1, surface_area: float = 1) -> float:
        '''
        Converts weight [in g] to lenght [in cm], 
        based on assumed bulk density of organic material [in g/cm3],
        and provided surface area [in cm2].
        '''
        return grams * self.grams_to_cm3_organic() * (1 / surface_area)

    def grams_to_cm_inorganic(self, grams: float = 1, surface_area: float = 1) -> float:
        '''
        Converts weight [in g] to lenght [in cm], 
        based on assumed bulk density of inorganic material [in g/cm3],
        and provided surface area [in cm2].
        '''
        return grams * self.grams_to_cm3_inorganic() * (1 / surface_area)
