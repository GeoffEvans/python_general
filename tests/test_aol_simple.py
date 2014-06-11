from aol_simple import Aol
from ray import Ray
import pytest
from numpy import allclose, array

wavelength = 800e-9

def test_non_unit_direction():
    with pytest.raises(ValueError):
        Aol(1, [1,1,1], [0,0,0,0],[0,0,0,0], aod_directions=[[1,0,0.1],[0,1,0],[-1,0,0],[0,-1,0]])
        
def test_plot():
    aol = Aol(1, [1,1,1], array([1,1,1,1])*1e9,[1,1,1,1])
    wavevec = [0,3./5,4./5]
    ray = Ray([0,0,0], wavevec, wavelength)
    plt = aol.plot_ray_through_aol(ray, 1, 1)
    plt.close()
    assert allclose(ray.position, [0,0,0]) and allclose(ray.wavevector_unit, wavevec)

def test_no_chirp_at_tzero():
    aol = Aol(1, [1,1,1], [0,0,0,0],array([1,1,1,1])*1e9)
    aol.set_centres_for_wavelengh(wavelength)
    wavevec = [0,0,1]
    ray = Ray([0,0,0], wavevec, wavelength)
    aol.propagate_to_distance_from_aol(ray, 0, 10)
    assert allclose(ray.wavevector_unit, wavevec)

def test_constant_freq_for_zero_chirp():
    aol = Aol(1, [1,1,1], [0,0,0,0],[1,1,1,1])
    wavevec = [0,3./5,4./5]
    ray1 = Ray([0,0,0], wavevec, wavelength)
    aol.propagate_through_aol(ray1, 0)
    ray2 = Ray([0,0,0], wavevec, wavelength)
    aol.propagate_through_aol(ray2, 100)
    assert allclose(ray1.wavevector_unit, ray2.wavevector_unit)    
    
def test_deflect_right_way():
    aol = Aol(1, [1,1,1], [1,0,0,0],[0,0,0,0])
    wavevec = [0,3./5,4./5]
    ray = Ray([0,0,0], wavevec, wavelength)
    aol.propagate_through_aol(ray, 0)
    assert ray.wavevector_unit[0] > 0    