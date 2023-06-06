'''
'''
from enum import Enum, auto
from typing import List, Dict, Protocol
from dataclasses import dataclass, field

import numpy as np

from src.constants import CONSTANTS, MORRIS_CONSTANTS

class Tag(Enum):
    '''
    '''
    BIOMASS = auto(),
    LABILE = auto(),
    REFRACTORY = auto(),
    ASH = auto(),
    INORGANIC = auto()

class Type(set, Enum):
    '''
    '''
    ORGANIC = {Tag.LABILE, Tag.REFRACTORY}
    INORGANIC = {Tag.ASH, Tag.INORGANIC}

class BiomassUpdateMethod(Enum):
    '''
    '''
    TURNOVER = auto(),
    FRACTION = auto(),
    '''Portion of previous biomass to retain (or increase if > 1) [dmls].'''
    BIOMASS = auto(),
    '''Biomass at surface, assumed constant over layer surface area [in g/cm2].'''

@dataclass(frozen=True)
class BiomassUpdate:
    '''
    '''
    method: BiomassUpdateMethod = BiomassUpdateMethod.TURNOVER
    parameter: None|float = None

    def __post_init__(self):
        if self.parameter is None and self.method != BiomassUpdateMethod.TURNOVER:
            raise AttributeError(f'A parameter value is required for the {self.method.value.lower()} biomass update method but none was provided.')

@dataclass
class Stock(Protocol):
    '''
    Note:
        [1] length requires surface area so is computed at the layers level.
    '''
    weight: float = 0
    length: float = 0

    def erode(self, erosion: float) -> None:
        '''
        Updates weight and length given a specified amount of erosion [in cm].
        '''
    def update(self) -> None:
        '''
        Updates weight and length through decomposition.
        '''

def biomass_weight(Ro: float, Du: float, Db: float, k1: float, sa: float) -> float:
    '''
    Returns dry weight of live below ground biomass between top and bottom elevation over a given areas.
    This can be used to add or substract biomass from a layer. 

    Arguments: 
        Ro [float]: concentration of mass at surface [in g/cm2].
        Du [float]: top elevation [in cm].
        Db [float]: bottom elevation [in cm].
        k1 [float]: distribution parameter for exponential decay as function of depth [in 1/cm].
        sa [float]: surface area [in cm2]

    Returns:
        [float]: biomass [in g]
    '''
    return Ro * (pow(np.e, -k1*Db) - pow(np.e, -k1*Du)) / -k1 * sa

@dataclass
class Layer:
    '''
    '''
    top: float = 0
    bottom: float = 0

    stocks: Dict[Tag, Stock] = field(init=False)

    def __post_init__(self):
        self.stocks = {}

    def erode_layer(self, constants: CONSTANTS, erosion: float = 0, is_bottom_layer: bool = False) -> float:
        '''
        Only deposition occurs on new layers. It should not be possible for an "update".
        '''
        if is_bottom_layer:
            self.erode_bottom_layer(constants, erosion)
            return 0.0
        if (excess_erosion := erosion - (self.bottom - self.top)) < 0:
            self.bottom += excess_erosion
            self.top = self.bottom
            return excess_erosion
        self.top += erosion
        return 0.0

    def erode_bottom_layer(self, constants: CONSTANTS, erosion: float) -> None:
        self.top += erosion
        self.bottom = self.top - (constants.init_top - constants.init_bottom)

@dataclass
class Layers:
    surface_area: float = 1
    constants_file: str = MORRIS_CONSTANTS
    constants: CONSTANTS = field(init=False)
    layers: List[Layer] = field(default_factory=list)

    def __post_init__(self):
        self.constants = CONSTANTS(self.constants_file)
        self.layers.append(Layer(top=self.constants.init_top, bottom=self.constants.init_bottom))

    def update(self, deposition: float = 0.0, ):
        '''
        Marshal updates through bed updates, biomass updates, and conversions.
        '''

    def update_bed(self, deposition: float = 0.0) -> None:
        '''
        '''
        if deposition < 0:
            self.erode_bed(erosion=deposition)
        else:
            pre_deposition_top: float = self.layers[len(self.layers) - 1].top
            self.layers.append(Layer(top=pre_deposition_top+deposition, bottom=pre_deposition_top))

    def erode_bed(self, erosion: float = 0) -> None:
        '''
        Recursively erodes layers held in object as a state variable.

        A top layer is recorded at every timestep,
        erosion causes the addition of a zero depth layer,
        the layers below are then made more shallow by decreasing the top elevation,
        with the execption of the bottom (initial) layer which always has a fixed depth,
        defined by the difference between the initial top and bottom elevation in the constants file.
        '''
        def recursive_erosion(i: int, erosion: float) -> None:
            is_bottom_layer = True if i == 0 else False
            excess_erosion = self.layers[i].erode_layer(self.constants, erosion, is_bottom_layer)
            if excess_erosion < 0:
                # layer i erodes completely, erosion continues on layer i - 1
                recursive_erosion(i=i-1, erosion=excess_erosion)

        # first, erode lower layer(s) to find bottom of new layer
        recursive_erosion(i=len(self.layers) - 1, erosion=erosion)
        # add zero depth layer on top elevation of previous top layer
        pre_erosion_top: float = self.layers[len(self.layers) - 1].top
        self.layers.append(Layer(top=pre_erosion_top, bottom=pre_erosion_top))
    
    def update_biomass(self, erosion: float = 0.0, parameters: BiomassUpdate = BiomassUpdate()):
        '''
        '''
        match parameters.method:
            case BiomassUpdateMethod.BIOMASS:
                pass
            case BiomassUpdateMethod.FRACTION:
                pass
            case BiomassUpdateMethod.TURNOVER:
                pass
            case _:
                raise AttributeError("Unknown biomass update method.")

def factory(surface_area: float, constants_file: str) -> Layers:
    return Layers(surface_area=surface_area, constants_file=constants_file)