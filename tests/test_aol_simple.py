from aol_simple import Aol
from ray import Ray
import pytest
from numpy import allclose

def test_non_unit_direction():
    with pytest.raises(ValueError):
        Aol(1, [1,1,1], [0,0,0,0],[0,0,0,0], [[1,0,0.1],[0,1,0],[-1,0,0],[0,-1,0]])
        
def test_no_chirp_at_tzero():
    aol = Aol(1, [1,1,1], [0,0,0,0],[1,1,1,1], [[1,0,0],[0,1,0],[-1,0,0],[0,-1,0]])
    wavevec = [0,3./5,4./5]
    ray = Ray([0,0,0], wavevec, 800e-9)
    aol.propagate_through_aol(ray, 0)
    assert allclose(ray.wavevector_unit, wavevec)

test_no_chirp_at_tzero()

def test_constant_freq_for_zero_chirp():
    aol = Aol(1, [1,1,1], [0,0,0,0],[1,1,1,1], [[1,0,0],[0,1,0],[-1,0,0],[0,-1,0]])
    wavevec = [0,3./5,4./5]
    ray1 = Ray([0,0,0], wavevec, 800e-9)
    aol.propagate_through_aol(ray1, 0)
    ray2 = Ray([0,0,0], wavevec, 800e-9)
    aol.propagate_through_aol(ray2, 100)
    assert allclose(ray1.wavevector_unit, ray2.wavevector_unit)    
    
def test_deflect_right_way():
    aol = Aol(1, [1,1,1], [1,0,0,0],[0,0,0,0], [[1,0,0],[0,1,0],[-1,0,0],[0,-1,0]])
    wavevec = [0,3./5,4./5]
    ray = Ray([0,0,0], wavevec, 800e-9)
    aol.propagate_through_aol(ray, 0)
    assert ray.wavevector_unit[0] > 0    