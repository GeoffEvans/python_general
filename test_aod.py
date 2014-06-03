from aod import *
from ray import Ray
from numpy import pi, arange, allclose

r = Ray([0,0,0],[0,0,1],800e-9,1)
aod = Aod([0,0,1], [1,0,0], 1, 1, 1, 1)

#ray down optic axis should have that dir
#ray off optic axis should not have that dir

#ray moving along aod axis should end up on axis

#ray refracting in should be closer to normal
#ray refracting out should be further from normal

#sound vector should match sound direction for normal being z
#sound vector should be down [1,0,-1] for normal being [1,0,1] and direction of [1,0,0]

#verify calc_refractive_indices_vector and calc_refractive_indices_ray are the same for a ray 


    
    