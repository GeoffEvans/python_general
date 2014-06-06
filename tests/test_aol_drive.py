from aol_drive import calculate_drive_freq_4, find_constant, find_linear
from acoustics import Acoustics
from numpy import array, dtype, allclose

order = -1
op_wavelength = 900e-9
aod_spacing = [5e-2, 5e-2, 5e-2]
spacing = array([1,1,1,1])
base_freq = 40e6
ac_velocity = Acoustics(base_freq).velocity
pair_deflection_ratio = 0.9
crystal_depth = 8e-3

def test_constant_pdr_zero():
    
    xy_deflection = array([1,0], dtype=dtype(float))
    consts0 = find_constant(order, op_wavelength, ac_velocity, spacing, base_freq, 0, xy_deflection)
    consts1 = find_constant(order, op_wavelength, ac_velocity, spacing, base_freq, 1, xy_deflection)
    
    assert allclose(consts0[0:2], base_freq) and not allclose(consts1[0:2], base_freq)
    
def test_linear_acoustic_vel():
    
    xy_focus_velocity = array([0,0], dtype=dtype(float))
    
    xy_ac_vel = array([ac_velocity,ac_velocity])
    linear_pos = find_linear(order, op_wavelength, ac_velocity, spacing, base_freq, pair_deflection_ratio,  xy_ac_vel)
    linear_neg = find_linear(order, op_wavelength, ac_velocity, spacing, base_freq, pair_deflection_ratio, -xy_ac_vel) 
    
    assert allclose(linear_pos[2:4], 0) and allclose(linear_neg[0:2], 0)

def test_ray_passes_through_focus():
    
    focus_position = array([1,2,3], dtype=dtype(float))
    focus_velocity = array([5,7,11], dtype=dtype(float))
    
    (const, linear, quad) = calculate_drive_freq_4(order, op_wavelength, ac_velocity, aod_spacing, crystal_depth, base_freq, pair_deflection_ratio, focus_position, focus_velocity)
    
    assert False # waiting to finish aol_simple before this can be tested... 