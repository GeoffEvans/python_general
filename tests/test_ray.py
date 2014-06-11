from ray import Ray
from numpy import allclose, array
import pytest

position = [0,0,2]
wavevector_unit = [1,0,0]
wavelength = 10
energy = 1

def test_setting_non_unit_vector():
    with pytest.raises(ValueError):
        Ray(position, [1,0,0.1], wavelength, energy)
    
def test_wavevectors():
    r = Ray(position, wavevector_unit, wavelength, energy)
    assert allclose(r.wavevector_unit * r.wavevector_vac_mag, r.wavevector_vac)
    
def test_propagating_normal_to_plane():
    r1 = Ray(position, wavevector_unit, wavelength, energy)
    r1.propagate_free_space(10)
    
    r2 = Ray(position, wavevector_unit, wavelength, energy)
    r2.propagate_to_plane([10,10,10], wavevector_unit)
    
    assert allclose(r1.position, r2.position)
    
def test_propagating_angle_to_plane():
    r = Ray(position, [3./5,4./5,0], wavelength, energy)
    r.propagate_to_plane([12,0,0], [1,0,0])
    assert allclose(r.position, position + array([12,16,0]))

def test_setting_wavevector_property():
    r = Ray(position, [3./5,4./5,0], wavelength, energy)
    r.wavevector_vac = [144,0,17]
    mag_correct = allclose(r.wavevector_vac_mag, 145)
    dir_correct = allclose(r.wavevector_unit, [144./145, 0, 17./145])
    assert mag_correct and dir_correct

