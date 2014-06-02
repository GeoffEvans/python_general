from aod import *
from numpy import pi, arange, allclose

def test_ord_less_than_ext():
    angles = arange(0,pi/2,pi/10)
    refractive_indices = calc_refractive_indices_ray(angles)
    
    ord_less_than_ext = refractive_indices[1] < refractive_indices[0]
    assert ord_less_than_ext.all()
