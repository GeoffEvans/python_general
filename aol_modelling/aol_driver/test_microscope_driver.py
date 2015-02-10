from microscope_driver import convert_normalised_to_cartesian, compensate_freq_for_transducer_location, \
    mode_structural, mode_miniscan, mode_pointing, mode_raster
from numpy import array, allclose, dtype, zeros
from aol_model.aol_simple import AolSimple

reference_shift = [0,0,0]
order = -1
xy_num_elems = 11
acceptance_angle = 4.35e-3 
dwell_time = 10e-6
zoom_factor = 1
base_freq = 40e6
system_clock_freq = 240e6
pair_deflection_ratio = 0.8
data_time_interval = 50e-9
aod_apertures = [15e-3]*4
ac_power = 1
ac_velocity = 613
op_wavelength = 900e-9
crystal_thickness = array([8e-3]*4)
aod_spacing = array([5e-2]*3)
focus_pos_normalised = array([[1,-2,0],[-4,5,6]], dtype=dtype(float))
focus_disp_normalised = array([[-9,8,0],[0,0,0]], dtype=dtype(float)) 

def test_structural():
    imaging_mode = mode_structural
    (focus_pos, focus_vel, ramp_time) = convert_normalised_to_cartesian(imaging_mode, xy_num_elems, zoom_factor, acceptance_angle, aod_apertures, \
                                                                        focus_pos_normalised, focus_disp_normalised, dwell_time, reference_shift)
    
    right_shapes = focus_pos.shape == (xy_num_elems, 3) and focus_vel.shape == (xy_num_elems, 3) and ramp_time.shape == (xy_num_elems,)
    
    assert right_shapes and \
            allclose(focus_vel, 0, rtol=0, atol=1e-15) and \
            allclose(ramp_time, dwell_time, rtol=0, atol=1e-15) and \
            (focus_pos[(xy_num_elems-1)/2,0:2] == 0).all() # centre point it (0,0,z)

def test_raster():
    imaging_mode = mode_raster
    (focus_pos, focus_vel, ramp_time) = convert_normalised_to_cartesian(imaging_mode, xy_num_elems, zoom_factor, acceptance_angle, aod_apertures, \
                                                                        focus_pos_normalised, focus_disp_normalised, dwell_time, reference_shift)

    right_shapes = focus_pos.shape == (xy_num_elems, 3) and focus_vel.shape == (xy_num_elems, 3) and ramp_time.shape == (xy_num_elems,)
    
    assert right_shapes and \
            allclose(focus_vel[:,1:3], 0, rtol=0, atol=1e-15) and \
            allclose(focus_pos[:,0], 0, rtol=0, atol=1e-15) and \
            allclose(ramp_time, dwell_time*xy_num_elems, rtol=0, atol=1e-15) and \
            focus_pos[(xy_num_elems-1)/2,1] == 0

def test_miniscan():
    imaging_mode = mode_miniscan
    (focus_pos, focus_vel, ramp_time) = convert_normalised_to_cartesian(imaging_mode, xy_num_elems, zoom_factor, acceptance_angle, aod_apertures, \
                                                                        focus_pos_normalised, focus_disp_normalised, dwell_time, reference_shift)

    right_shapes = focus_pos.shape == (len(focus_pos_normalised), 3) and focus_vel.shape == (len(focus_pos_normalised), 3) and ramp_time.shape == (len(focus_pos_normalised),)

    assert right_shapes and allclose(focus_vel[:,2], 0, rtol=0, atol=1e-15)

def test_pointing():
    imaging_mode = mode_pointing
    (focus_pos, focus_vel, ramp_time) = convert_normalised_to_cartesian(imaging_mode, xy_num_elems, zoom_factor, acceptance_angle, aod_apertures, \
                                                                        focus_pos_normalised, focus_disp_normalised, dwell_time, reference_shift)
    
    right_shapes = focus_pos.shape == focus_pos_normalised.shape and focus_vel.shape == focus_pos_normalised.shape and ramp_time.shape == (focus_pos_normalised.shape[0],)
    
    assert right_shapes and \
            allclose(focus_vel, 0, rtol=0, atol=1e-15) and \
            allclose(ramp_time, dwell_time, rtol=0, atol=1e-15)
            
def test_transducer_offset():
    aol_simple = AolSimple.create_aol_from_drive(1, [1e3]*3, [1e6]*4, [1e9]*4, 900e-9)
    apertures = [1.]*4
    transducer_at_base_ray = aol_simple.base_ray_positions + (aol_simple.aod_directions[:,0:2].T * apertures/2).T
    freq_offset = compensate_freq_for_transducer_location(aol_simple, transducer_at_base_ray, zeros(4), apertures)
    assert allclose(freq_offset, 0, rtol=0, atol=1e-15)
