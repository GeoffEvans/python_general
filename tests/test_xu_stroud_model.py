from aol_model.aod import Aod
from aol_model.ray import Ray
from aol_model.acoustics import Acoustics
from aol_model.xu_stroud_model import diffract_acousto_optically,diffract_by_wavevector_triangle,get_aod_efficiency
from aol_model.convert_cartesian_spherical import normalise
import pytest
from numpy import allclose, all
from random import random
from scipy import less_equal, greater_equal

acoustic = Acoustics(40e6, 613, 2)

def test_order_sym():
    r1 = Ray([0,0,0],[-17/145,0,144/145],800e-9,1)
    aod1 = Aod([0,0,1], [1,0,0], 1, 1, 1, 1)
    r2 = Ray([0,0,0],[ 17/145,0,144/145],800e-9,1)
    aod2 = Aod([0,0,1], [1,0,0], 1, 1, 1, -1)
    
    diffract_acousto_optically(aod1, r1, acoustic)
    diffract_acousto_optically(aod2, r2, acoustic)
    
    opposite_xcomps = allclose(r1.wavevector_unit[0], -r2.wavevector_unit[0])
    assert allclose(r1.energy, r2.energy) and opposite_xcomps  
    
def test_efficiency_range():
    aod = Aod([0,0,1], [1,0,0], 1, 1, 1, -1)
    
    def eff_fun():
        v1 = normalise([random(),random(),random()])
        v2 = normalise([random(),random(),random()])
        ray_in = Ray([0,0,0],v1,800e-9,1)
        ray_out = Ray([0,0,0],v2,800e-9,1)
        get_aod_efficiency(aod, random(), ray_in, ray_out, acoustic)
        
    effs = [ eff_fun() for _ in range(10) ]
    assert all(less_equal(effs,1)) and all(greater_equal(effs,0))  
        
def test_wavevector_triangle():
    ray = Ray([0,0,0],[1,0,0],800e-9,1)
    aod = Aod([0,0,1], [1,0,0], 1, 1, 1, 1)
    (wavevector_mismatch_mag, original_ray) = diffract_by_wavevector_triangle(aod, ray, acoustic)
    k_i = original_ray.wavevector_vac * aod.calc_refractive_indices_ray(original_ray)
    k_d = ray.wavevector_vac * aod.calc_refractive_indices_ray(ray)
    K = acoustic.wavevector(aod) * aod.order
    zero_sum = k_i + K + aod.normal * wavevector_mismatch_mag - k_d
    assert allclose(zero_sum, 0)

def test_setting_bad_mode():
    with pytest.raises(ValueError):
        Aod([0,0,1], [1,0,0], 1, 1, 1, 2)