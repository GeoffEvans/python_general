from microscope_driver import get_drive, convert_normalised_to_cartesian
from driver_wrapper import FocusInfo
from numpy import array, allclose
from test_aol_full import focal_length

is_structural = 0
is_raster = 1
is_pointing = 2
is_miniscan = 3

reference_shift = [0,0,0]
order = -1
xy_num_elems = 10
acceptance_angle = 4.35e-3 
dwell_time = 10e-6
zoom_factor = 1
base_freq = 40e6
system_clock_freq = 240e6
pair_deflection_ratio = 0.8
data_time_interval = 50e-9
aod_aperture = 15e-3
ac_power = 1
ac_velocity = 613
op_wavelength = 900e-9
crystal_thickness = array([8e-3]*4)
aod_spacing = array([5e-2]*3)
focus_pos_normalised = [[1,-2,3],[-4,5,6]]
focus_disp_normalised = [[-9,8,0],[]] 

focus_info_normalised = FocusInfo.create_focus_info(focus_pos_normalised, focus_disp_normalised)

def test_structural():
    imaging_mode = is_structural
    (focus_pos, focus_vel, ramp_time) = convert_normalised_to_cartesian(imaging_mode, xy_num_elems, zoom_factor, acceptance_angle, aod_aperture, \
                                                                        focus_pos_normalised, focus_disp_normalised, dwell_time, reference_shift)
    
    right_shapes = focus_pos.shape == (xy_num_elems, 3) and focus_vel.shape == (xy_num_elems, 3) and ramp_time.shape == (xy_num_elems)
    
    assert right_shapes and \
            allclose(focus_vel, 0, rtol=0, atol=1e-15) and \
            allclose(focus_pos, 0, rtol=0, atol=1e-15) and \
            allclose(ramp_time, dwell_time, rtol=0, atol=1e-15)
            
def test_raster():
    imaging_mode = is_raster
    (focus_pos, focus_vel, ramp_time) = convert_normalised_to_cartesian(imaging_mode, xy_num_elems, zoom_factor, acceptance_angle, aod_aperture, \
                                                                        focus_pos_normalised, focus_disp_normalised, dwell_time, reference_shift)

    right_shapes = focus_pos.shape == (xy_num_elems, 3) and focus_vel.shape == (xy_num_elems, 3) and ramp_time.shape == (xy_num_elems)
    
    assert right_shapes and \
            allclose(focus_vel[:,1], 0, rtol=0, atol=1e-15) and \
            allclose(focus_pos[:,0], 0, rtol=0, atol=1e-15) and \
            allclose(ramp_time, dwell_time*xy_num_elems, rtol=0, atol=1e-15)
                            
def test_miniscan():
    imaging_mode = is_miniscan
    (focus_pos, focus_vel, ramp_time) = convert_normalised_to_cartesian(imaging_mode, xy_num_elems, zoom_factor, acceptance_angle, aod_aperture, \
                                                                        focus_pos_normalised, focus_disp_normalised, dwell_time, reference_shift)

    right_shapes = focus_pos.shape == (len(focus_info_normalised), 3) and focus_vel.shape == (len(focus_info_normalised), 3) and ramp_time.shape == (len(focus_info_normalised))

    assert right_shapes
    
def test_pointing():
    imaging_mode = is_pointing
    (focus_pos, focus_vel, ramp_time) = convert_normalised_to_cartesian(imaging_mode, xy_num_elems, zoom_factor, acceptance_angle, aod_aperture, \
                                                                        focus_pos_normalised, focus_disp_normalised, dwell_time, reference_shift)
    
    right_shapes = focus_pos.shape == (len(focus_info_normalised), 3) and focus_vel.shape == (len(focus_info_normalised), 3) and ramp_time.shape == (len(focus_info_normalised))
    
    assert right_shapes and \
            allclose(focus_vel, 0, rtol=0, atol=1e-15) and \
            allclose(ramp_time, dwell_time, rtol=0, atol=1e-15)