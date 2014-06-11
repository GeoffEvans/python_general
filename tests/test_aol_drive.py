from aol_drive import find_constant, find_linear
from acoustics import teo2_ac_vel
from aol_simple import AolSimple
from ray_paraxial import RayParaxial
from numpy import array, dtype, allclose

order = 1
op_wavelength = 900e-9
aod_spacing = [5e-2, 5e-2, 5e-2]
spacing = array([1,1,1,1])
base_freq = 40e6
ac_velocity = teo2_ac_vel
pair_deflection_ratio = 0.9

def test_constant_freq_for_pair_def_ratio_zero():
    
    xy_deflection = array([1,0], dtype=dtype(float))
    consts0 = find_constant(order, op_wavelength, ac_velocity, spacing, base_freq, 0, xy_deflection)
    consts1 = find_constant(order, op_wavelength, ac_velocity, spacing, base_freq, 1, xy_deflection)
    
    assert allclose(consts0[0:2], base_freq) and not allclose(consts1[0:2], base_freq)
    
def test_linear_freq_for_acoustic_vel_scan():
    
    xy_ac_vel = array([ac_velocity,ac_velocity], dtype=dtype(float))
    linear_pos = find_linear(order, op_wavelength, ac_velocity, spacing, base_freq, pair_deflection_ratio,  xy_ac_vel)
    linear_neg = find_linear(order, op_wavelength, ac_velocity, spacing, base_freq, pair_deflection_ratio, -xy_ac_vel) 
    
    assert allclose(linear_pos[2:4], 0) and allclose(linear_neg[0:2], 0)

def test_ray_passes_through_focus():
    
    focus_position = array([1.,2.,3.], dtype=dtype(float))
    focus_velocity = array([0,0,0], dtype=dtype(float))
    
    aol = AolSimple.create_aol(order, op_wavelength, ac_velocity, aod_spacing, base_freq, pair_deflection_ratio, focus_position, focus_velocity)

    ray1 = RayParaxial([0,0,0], [0,0,1], op_wavelength)
    aol.propagate_to_distance_from_aol(ray1, 0, focus_position[2]) # t = 0
    
    ray2 = RayParaxial([0,0,0], [0,0,1], op_wavelength)
    aol.propagate_to_distance_from_aol(ray2, 11, focus_position[2]) # t != 0
    
    ray3 = RayParaxial([1,0,0], [0,0,1], op_wavelength) # position not origin
    aol.propagate_to_distance_from_aol(ray3, 0, focus_position[2]) # t = 0
        
    expected_position = focus_position + [0,0,sum(aod_spacing)]
    assert allclose(ray1.position, expected_position) and allclose(ray2.position, expected_position) and allclose(ray3.position, expected_position)
  
def test_focus_scans_correctly():
 
    focus_position = array([.1,.2,3], dtype=dtype(float))
    focus_velocity = array([5,7,0], dtype=dtype(float))
    time = 10 
     
    ray1 = RayParaxial([0,0,0], [0,0,1], op_wavelength)
    aol1 = AolSimple.create_aol(1, op_wavelength, ac_velocity, aod_spacing, base_freq, pair_deflection_ratio, focus_position, focus_velocity)
    aol1.propagate_to_distance_from_aol(ray1, time, focus_position[2])
     
    ray2 = RayParaxial([0,0,0], [0,0,1], op_wavelength)
    aol2 = AolSimple.create_aol(order, op_wavelength, ac_velocity, aod_spacing, base_freq, pair_deflection_ratio, focus_position, focus_velocity)
    aol2.propagate_to_distance_from_aol(ray2, time, focus_position[2])
         
    expected_position = focus_position + [0,0,sum(aod_spacing)] + time * focus_velocity
    assert allclose(ray1.position, expected_position) and allclose(ray2.position, expected_position) 