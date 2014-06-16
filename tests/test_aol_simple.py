from aol_simple import AolSimple
from ray import Ray
import pytest
from numpy import allclose, array

wavelength = 800e-9

def test_non_unit_direction():
    with pytest.raises(ValueError):
        AolSimple(1, [1,1,1], [0,0,0,0], [0,0,0,0], aod_directions=[[1,0,0.1],[0,1,0],[-1,0,0],[0,-1,0]])
        
def test_plot():
    aol = AolSimple.create_aol_from_drive(1, [1,1,1], array([1,1,1,1])*1e8, [1,1,1,1], wavelength)
    wavevec = [0,3./5,4./5]
    ray = Ray([0,0,0], wavevec, wavelength)
    plt = aol.plot_ray_through_aol(ray, 1, aol.aod_spacing.sum())
    plt.close()
    assert allclose(ray.position, [0,0,0]) and allclose(ray.wavevector_unit, wavevec)

def test_no_chirp_at_tzero():
    aol = AolSimple.create_aol_from_drive(1, [1,1,1], [0,0,0,0], array([1,1,1,1])*1e9, wavelength)
    aol.set_base_ray_positions(wavelength)
    wavevec = [0,0,1]
    ray = Ray([0,0,0], wavevec, wavelength)
    aol.propagate_to_distance_past_aol(ray, 0, 10)
    assert allclose(ray.wavevector_unit, wavevec)
    
def test_constant_freq_for_zero_chirp():
    aol = AolSimple.create_aol_from_drive(1, [1,1,1], [0,0,0,0], [1,1,1,1], wavelength)
    wavevec = [0,3./5,4./5]
    ray1 = Ray([0,0,0], wavevec, wavelength)
    aol.propagate_to_distance_past_aol(ray1, 0)
    ray2 = Ray([0,0,0], wavevec, wavelength)
    aol.propagate_to_distance_past_aol(ray2, 100)
    assert allclose(ray1.wavevector_unit, ray2.wavevector_unit)    
    
def test_deflect_right_way():
    aol = AolSimple.create_aol_from_drive(1, [1,1,1], [1,0,0,0], [0,0,0,0], wavelength)
    wavevec = [0,3./5,4./5]
    ray = Ray([0,0,0], wavevec, wavelength)
    aol.propagate_to_distance_past_aol(ray, 0)
    assert ray.wavevector_unit[0] > 0    