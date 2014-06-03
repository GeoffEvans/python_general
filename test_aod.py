from aod import *
from ray import Ray
from numpy import pi, arange, allclose

def create_ray():
    return Ray([0,0,0],[1,0,0],800e-9,1)
    
def create_many_rays():
    assert True
    
def create_aod():
    #aod = Aod([1,0,0], [], aperture_width, transducer_width, crystal_width, order)