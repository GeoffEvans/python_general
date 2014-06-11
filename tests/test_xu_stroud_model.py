from aod import Aod
from ray import Ray
from acoustics import Acoustics
from xu_stroud_model import diffract_acousto_optically,diffract_by_wavevector_triangle,get_aod_efficiency
from vector_utils import normalise
import pytest
from numpy import allclose, all
from random import random
from scipy import less_equal, greater_equal

acoustics = Acoustics(40e6, 2)
aod = Aod([0,0,1], [1,0,0], 1e-3, 1e-3, 1e-3, 1)

def test_efficiency_range():
    
    def eff_fun():
        v = normalise([random(),random(),10])
        ray_in = Ray([0,0,0],v,800e-9,1)
        ray_out = Ray([0,0,0],v,800e-9,1)
        return get_aod_efficiency(aod, random(), ray_in, ray_out, acoustics)
        
    effs = [ eff_fun() for _ in range(100) ]
    assert all(less_equal(effs,1)) and all(greater_equal(effs,0))  

def test_order_sym():
    r1 = Ray([0,0,0],[-17./145,0,144./145],800e-9,1)
    r2 = Ray([0,0,0],[ 17./145,0,144./145],800e-9,1)
    
    diffract_acousto_optically(aod, r1, acoustics)
    aod.order = -1;
    diffract_acousto_optically(aod, r2, acoustics)
    aod.order = 1;
    
    opposite_xcomps = allclose(r1.wavevector_unit[0], -r2.wavevector_unit[0])
    assert allclose(r1.energy, r2.energy) and opposite_xcomps  
        
def test_wavevector_triangle():
    ray = Ray([0,0,0],[0,0,1],800e-9,1)
    (wavevector_mismatch_mag, original_ray) = diffract_by_wavevector_triangle(aod, ray, acoustics)
    k_i = original_ray.wavevector_vac * aod.calc_refractive_indices_ray(original_ray)[0]
    k_d = ray.wavevector_vac * aod.calc_refractive_indices_ray(ray)[1]
    K = acoustics.wavevector(aod) * aod.order
    zero_sum = k_i + K + aod.normal * wavevector_mismatch_mag - k_d
    assert allclose(zero_sum, 0)

def test_setting_invalid_mode():
    with pytest.raises(ValueError):
        Aod([0,0,1], [1,0,0], 1, 1, 1, 2)