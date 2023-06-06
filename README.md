# organic-accretion
Computes accretion on salt marshes in dynamic simulations
   
            natural                 
            deposition (W)
                |             
                |---------------------------------------
    W * (1 - a) |                           |           |
                | W * a * b                 |           | W * a * (1 - c)
                |--------         W * a * c |           |       +
                |        |                  |           |             
                |        |                  |           |   -----
                |        |                  |           |  |     |
                v        v                  v           v  v     ^
            |         |     |           |          |
            |inorganic| ash |           |refractory| labile | live rootmass  
            |_________|_____|           |__________|
                    |         
                    v
                erosion

a = portion organic
b = portion organic that is (inorganic) ash.
c = portion organic that is refactory

## how to use:

1. Initialization

A lengthy set of constants are required. These are supplied in .toml file. This work is based on Morris & Bowden (1986), a default "morris_constants.toml" file is provided based on constants used in that paper's case study. These constants are invariant in time and space. An intial sediment layer is created in this step. Unlike the subsequent layers, this layer cannot be eroded away in later time steps. 

2. Advancing the model

The simulatation advances once per timestep. Each time the model is advanced a new layer is added, and existing layers are updated. This involves several sub processes, which are computed in the following order: 

A. Accretion or erosion - if erosion occurs a new layer with 0 depth is added, live and inert organic and inorganic sediment if removed from the previous layers. 

B. Below ground biomass - updating biomass is a sequential 3 step process...

FIRST: Biomass in eroded sediment (at the top) is removed, and/or biomass below the maximum root depth (root_depth constant) is converted to labile sediment. If sediment is eroded then a new, Ro[t] is computed based on the biomass at the eroded depth. If accretion occurs then R[t] = R[t-1]. This occurs without any new parameterization,aside from the deposition parameter that drives the erosion and accretion process.

SECOND: 1 of 2 optional parameters may be provided, either (1) mortality - converts a fixed portion of the biomass to mostly labile sediment, or (2) Ro - an updated Ro (biomass at the surface) value. This for instance may be used to update the biomass in each timestep to account for growth of the plants. If the parameter, Ro[t] is less than the previous value, Ro[t-1] then the difference, Ro[t-1] - Ro[t] is converted to (mostly) labile sediment.

THIRD: IF neither of the optional parameters described above are provided, THEN normal turnover (k2 constant) of the living below ground biomass, based on Ro[t] (biomass at surface) value is computed, converting some of the biomass into labile sediment. If one of the optional parameters described in the previous step are provided then this step is skipped.
 

