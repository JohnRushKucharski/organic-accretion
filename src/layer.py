'''
Computes accretion in a single cohert.

Morris and Bowden (1986) presents a model for computing coherts of sediment,
where each cohert is the sediment deposited during a particular simulation year. 
This follows that model, with a less rigid timestep - e.g. a cohert is sediment
from a particular computational timestep. 

Some notes about the what is being processed.
    1. construction of bottom layer with a fixed composition, initial deposition and biomass at surface
    2. each year a new layer is added
        a. through normal deposition
        b. with er

'''

# from typing import Tuple
# from dataclasses import dataclass, field

# import numpy as np

# from src.constants import CONSTANTS

# def biomass_weight(biomass_at_surface: float, top_elevation: float, bottom_elevation: float, distribution_parameter: float) -> float:
#     '''
#     Computes dry weight of live below ground biomass between top and bottom elevation, given a (constant) mass [in g/cm2] at the surface. 

#     Arguments: 
#         biomass_at_surface [float]: constant concentration of mass at surface [in g/cm2].
#         top_elevation [float]: relative to the surface [in cm].
#         bottom_elevaton [float]: relative to the surface [in cm].
#         distribution_parameter [float]: k1 parameter for exponential decay as function of depth [in 1/cm].
#     '''
#     return biomass_at_surface * (pow(np.e, -distribution_parameter*bottom_elevation) - pow(np.e, -distribution_parameter*top_elevation)) / -distribution_parameter

# @dataclass
# class Layer:
#     '''
#     Keeps track of cohert of sediment on a plot of marsh with a fixed surface area.
#     '''
#     #region fields
#     #region required inputs
#     timestep: int
#     '''Timestep that defines cohert.''' 
#     surface_area: float
#     '''Surface area for volumetric layer [in cm].'''
#     constants: CONSTANTS

#     deposition: float
#     '''Initial deposition at surface, from leaf litter and exogenous sources [in cm].'''
#     # excess_deposition: float
#     # '''Excess deposition from event driven mortality of plants [in g].''' 
#     biomass_at_surface: float
#     '''Ro in Morris & Bowden, assumed constant over the surface area [in g/cm2].'''
#     #endregion
#     #region computed fields
#     top: float = 0.0
#     '''Depth from surface [in cm].'''
#     bottom: float = field(init=False)
#     '''Depth from surface (initialized as initial_deposition) [in cm].'''

#     biomass: float = field(init=False)
#     '''Length of biomass in layer [in cm].'''
#     refractory: float = field(init=False)
#     '''Length of refractory organic content in layer [in cm].'''
#     labile: float = field(init=False)
#     '''Length of labile organice content in layer [in cm].'''
    
#     inorganic: float = field(init=False)
#     '''Length of inorganic content in layer [in cm].'''
#     #endregion
#     #endregion

#     def __post_init__(self) -> None:
#         self.bottom = self.deposition
#         self.biomass = self.constants.grams_to_cm_organic(biomass_weight(self.biomass_at_surface, self.top, self.bottom, self.constants.biomass_distribution_parameter_k1))
#         self.refractory = self.refractory_deposition(self.deposition)
#         self.labile = self.labile_deposition(self.deposition)
#         self.inorganic = self.inorganic_deposition(self.deposition)

#     # def depth(self, deposition: float) -> float:
#     #     '''
#     #     Computes depth of layer from natural and excess (event driven mortality) deposition [in cm].
#     #     '''
#     #     # natural depostion + inorganic excess converted to cm + organic excess converted to cm
#     #     # organic_excess = self.constants.grams_to_cm_organic(grams=self.excess_deposition * (1 - self.constants.portion_ash), surface_area=self.surface_area)
#     #     # inorganic_excess =  self.constants.grams_to_cm_inorganic(grams=self.excess_deposition * self.constants.portion_ash, surface_area=self.surface_area)
#     #     return deposition #+ organic_excess + inorganic_excess

#     # def biomass_weight(self, biomass_at_surface: float, upper: float, lower: float):
#     #     '''
#     #     Computes dry weight of below ground live organic material from depth a to b [in g].

#     #     Notes:
#     #         [1] Follows equation 4 in Morris and Bowden.
#     #     '''
#     #     if lower < upper:
#     #         raise AttributeError('The lower depth must be greater than the upper depth.')
#     #     if self.bottom < lower:
#     #         raise AttributeError('The specified lower depth, exceeds the layer depth.')
#     #     return biomass_at_surface * \
#     #         (pow(np.e, -self.constants.biomass_distribution_parameter_k1*lower) - \
#     #          pow(np.e, -self.constants.biomass_distribution_parameter_k1*upper)) \
#     #             / -self.constants.biomass_distribution_parameter_k1*self.surface_area

#     # def weight_of_biomass(self, biomass_at_surface: float, depth: float) -> float:
#     #     '''
#     #     Computes the initial dry weight of below ground organic material in layer [in g].

#     #     Notes:
#     #         [1] Follows equation 4 in Morris & Bowden, 
#     #             where -exp(-k1Du) evaluates to 1 since Du = 0, 
#     #             equation is multiplied by surface area to return g/layer instead of g/cm2.
#     #         [2] Is modified by erosion, desication.
#     #     '''
#     #     # If bottom > roots can grow integrate to max root depth, o/w integrate to bottom of layer.
#     #     root_depth_in_layer = min(depth, self.constants.max_root_depth)
#     #     return biomass_at_surface * (pow(np.e, -self.constants.biomass_distribution_parameter_k1*root_depth_in_layer) - 1) / - self.constants.biomass_distribution_parameter_k1 * self.surface_area

#     # def biomass_depth(self, biomass_at_surface: float, upper: float, lower: float) -> float:
#     #     '''
#     #     Computes the size of the live below ground biomass in layer as a length [in cm].
#     #     '''

#     #     return self.constants.grams_to_cm_organic(self.biomass_weight(biomass_at_surface, upper, lower), surface_area=self.surface_area)

#     def refractory_deposition(self, deposition: float) -> float:
#         '''
#         Computes the initial depth or length of refractory material [in cm].
        
#         Notes:
#             [1] Generally follows equation 7 in Morris and Bowden, except a length is computed.
#             [2] Is modified by erosion, desication of biomass (equation 6 in Morris and Bowden).
#         '''
#         # natural depositon + portion of excess that is refractory all organic - except ash.
#         #excess_deposition = self.constants.grams_to_cm_organic(self.excess_deposition * (1 - self.constants.portion_ash) * self.constants.portion_refractory, self.surface_area)
#         return deposition * self.constants.portion_organic * self.constants.portion_refractory

#     def labile_deposition(self, deposition: float) -> float:
#         '''
#         Computes the depth or length of labile material [in cm].

#         Notes:
#             [1] Genarally follows equation 1 in Morris & Boweden, except a length is computed.
#             [2] Is modified by erosion, desication of biomass, decomposition.
#         '''
#         return deposition * self.constants.portion_organic * (1 - self.constants.portion_refractory)

#     def inorganic_deposition(self, deposition: float) -> float:
#         '''
#         Computes the depth or length of the initial inorganic content. Given a deposition of mixed inorganic and organic materials. [in cm].
#         '''
#         return deposition * self.constants.portion_organic * self.constants.portion_ash + deposition * (1 - self.constants.portion_organic)

#     # cases
#     # 1: just turnover between stocks
#     # 2: 1 + root growth
#     # 3: 1 + 2 + erosion

#     def turnover(self):
#         # no ash?
#         biomass_turnover: float = self.constants.natural_underground_mortality*self.biomass
#         self.refractory += self.constants.portion_refractory*biomass_turnover
#         labile_turnover: float = 
#         self.labile += (1 - self.constants.portion_refractory)*biomass_turnover


#     # def erosion(self, erosion: float) -> None:
#     #     '''
#     #     Removes eroded sediment [in cm], from buckets in layer.
#     #     '''
#     #     if erosion < 0: raise AttributeError('Only positive values for erosion (amount eroded) are acceptable.')
        
#     # def update_layer(self,
#     #                  top: float,                            # [in cm]
#     #                  erosion: float = 0,                    # [in cm]
#     #                  excess_organic_deposition: float = 0,  # [in g]
#     #                  biomass_at_surface: None|float = None, # [in g/cm2]  
#     #                  biomass_mortality: float = 0           # [dmls]
#     #                  ) -> float:                            # [in cm]
#     #     '''
#     #     Updates the layer.

#     #     Args:
#     #         top [float]: Bottom depth of layer above [in cm].
#     #         erosion [float]: Must be positive (amount of erosion) [in cm].
#     #             0 by default.
#     #         excess_organic_deposition [float]: Deposition of above ground biomass [in g].
#     #             Associated with vegetation mortality not accounted for in deposition input, 0 by default.
#     #         biomass_mortality [float]: Reduces below ground biomass by specified portion [dmls].
#     #             Assumed input is based on destruction of above ground biomass.
#     #         biomass_at_surface [float|None]: Ro in Morris & Bowden [in g/cm2].
#     #             Assumed constant over the surface area.
#     #             If None, the last time periods values are used, i.e. no growth is assumed. 
#     #     Returns:
#     #         None
#     #     Raises:
#     #         AttributeError: if erosion term is negative.
#     #     Notes:
#     #         [1] Excess deposition is in units of weight, this could be refactored if some other units are prefered.
#     #             It is upto the caller of this function to deal with advection and diffusion of plant parts.
#     #         [2] Above ground biomass is not tracked by model, so mortality cannot be converted to depositional units.
#     #         [3] It is assumed that the caller deals with mortality due to erosion, innundation, burial, etc.
#     #     '''
#     #     if erosion < 0:
#     #         raise AttributeError("Erosion must be positive (amount of erosion), a negative value was provided.")
#     #     else:
#     #         # deal with erosion term. assume this happens first.
#     #         if erosion > self.


#     #     if deposition < 0:
#     #         if deposition < (self.bottom - self.top):
#     #             # erode a fraction
#     #             # change Ro to Ro * biomass mortality
#     #             # remove biomass Db - Du, recompute Ro at Db
#     #             pass
#     #         else:
#     #             # 0 everything out
#     #             # retun excess erosion
#     #             pass
#     #     else:
            
#     #         # add to layer buckets
#     #         # add excess depositon
#     #         # update Ro with (1) Ro * biomass_mortality, or (2) new Ro
#     #         # compute biomass
#     #         pass

#     def update_elevations(self, top: float, erosion: float = 0):
#         if top < self.top:
#             raise AttributeError('A layer can only shift downward but the top elev')
#         shift = top - self.top

#     def __erode_sediment_layer(self, erosion: float) -> Tuple[float, float]:
#         '''
#         Modifies self.bottom and returns Tuple in form (self.bottom, excess erosion).
    
#         Arguments:
#             erosion [float]: expected a negative value, positive values generate accretion [in cm].
#                 If the absolute value of erosion exceeds the layer depth (self.bottom - self.top),
#                 then self.bottom = self.top.

#         Returns:
#             Tuple in form (new bottom depth [in cm], remaining/excess erosion [in cm]).

#         Note:
#             self._bottom is mutated directly.
#         '''
#         # Excess erosion case
#         if erosion < 0 and (self.bottom - self.top) < abs(erosion):
#             self.bottom = self.top
#             return self.bottom, erosion + (self.bottom - self.top)
#         self.bottom += erosion
#         return self.bottom, 0.0

#     def __str__(self, verbose: bool = False) -> str:
#         '''
#         Provides a more human readable string representing the layer object values.
#         '''
#         label: str = f'layer at t={self.timestep}(top: {self.top}cm, bottom: {self.bottom}cm'
#         if verbose:
#             return label + f', refractory: {self.refractory}g, labile: {self.labile}g, biomass: {self.biomass}g)'
#         else:
#             return label + ')'

# def factory(timestep: int = 0,
#             deposition: float|None = None,
#             aboveground_mortality: float = 0,
#             biomass_at_surface: float|None = None,
#             constants: CONSTANTS = CONSTANTS()) -> Layer:
#     '''
#     Marshalls inputs into correct values for construction of new layer.
#     '''
#     if timestep == 0:
#         # this makes it impossible to override the initial conditions in the constants file.
#         return Layer(timestep,
#                      initial_deposition=constants.init_layer_depth,
#                      initial_biomass_at_surface=constants.init_biomass_at_surface, constants=constants)
#     # else: timestep is no 0 then nothing should be none.
#     if deposition is None or biomass_at_surface is None or constants is None:
#         raise AttributeError('Only the initial layer can be missing deposition, biomass, or constant values.')
#     if deposition > 0:
#         return Layer(timestep,
#                      initial_deposition=deposition,
#                      initial_biomass_at_surface=biomass_at_surface, constants=constants)
#     # else: in the case erosion is occuring record a layer of zero depth (and erode older coherts).
#     return Layer(timestep, initial_deposition=0, initial_biomass_at_surface=0, constants=constants)
# '''