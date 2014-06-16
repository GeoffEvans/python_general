from numpy import array, linspace, append
from aol_simple import AolSimple
from numpy.linalg.linalg import norm

def microscope_driver( \
                       imaging_mode, \
                       order, \
                       xy_num_elems, \
                       acceptance_angle, \
                       dwell_time, \
                       zoom_factor, \
                       base_freq, \
                       focus_pos_normalised, \
                       focus_disp_normalised, \
                       system_clock_freq, \
                       pair_deflection_ratio, \
                       data_time_interval, \
                       aod_aperture, \
                       ac_velocity, \
                       op_wavelength, \
                       aod_thicknesses, \
                       aod_spacing):

    is_structural = imaging_mode == 0
    is_raster = imaging_mode == 1
    is_pointing = imaging_mode == 2
    is_miniscan = imaging_mode == 3

    aod_xy_centres = -1e-3 * array([ [0,0], [2.3,0], [4.6,2.3], [4.6,4.6] ])
    reference_shift = array([0, 0, 0])
    common_offsets = array([4.65, 5.45]) # common is for eliminating scan speed displacement
    differential_offsets = array([-0.85, 3.6]) # differential is for compensating XZ shifts

    transducerOffsets = -1e-3 * array([common_offsets(0) - differential_offsets(0),  \
                                       common_offsets(1) - differential_offsets(1),  \
                                       common_offsets(0) + differential_offsets(0),  \
                                       common_offsets(1) + differential_offsets(1)])

    aol = AolSimple.create_aol(order, op_wavelength, ac_velocity, aod_spacing, base_freq, pair_deflection_ratio, focus_position, focus_velocity)
    reference_point = aol.base_ray_positions[-1] + reference_shift


    (focus_pos, focus_vel, ramp_time) = convert_normalised_to_cartesian(xy_num_elems, zoom_factor, acceptance_angle, focus_pos_normalised, \
                                                                        focus_disp_normalised, reference_point)
    
    def convert_normalised_to_cartesian(xy_num_elems, zoom_factor, acceptance_angle, focus_pos_normalised, focus_disp_normalised, reference_point):
        
        # Originally, half deflection went on each of the pair, so if max deflection on one is accAngle then total def is twice that, hence factor of 2 below
        z_focus_pos_normalised = focus_pos_normalised[2,:]
        z_focus_pos_normalised = (z_focus_pos_normalised == 0) * 1e-6 + z_focus_pos_normalised # avoid divide by 0
        z_image_centre = aod_aperture / (4 * acceptance_angle * z_focus_pos_normalised)
        
        xy_extreme_rel_to_base_ray = 2 * acceptance_angle / zoom_factor * z_image_centre
        
        xy_focus_pos = focus_pos_normalised[0:2,:] * xy_extreme_rel_to_base_ray
        
        xy_row_rel_to_base_ray = linspace(-xy_extreme_rel_to_base_ray, xy_extreme_rel_to_base_ray, xy_num_elems)
        if xy_num_elems == 1:
            xy_row_rel_to_base_ray = 0
        
        if is_miniscan:
            ramp_time = dwell_time * xy_num_elems * norm(focus_disp_normalised[0:2,:], axis=0) / 2 #qq check dimensions and axis
            focus_vel = focus_disp_normalised[0:2,:] * xy_extreme_rel_to_base_ray / ramp_time #qq
            
        if is_pointing:
            ramp_time = dwell_time
            focus_vel = 0 * focus_disp_normalised

        if is_structural: # assumes single point but doesn't throw if not...
            ramp_time = dwell_time
            focus_vel = 0 * focus_disp_normalised
            xy_focus_pos = reference_point + xy_row_rel_to_base_ray #qq
            
        if is_raster: # assumes single point but doesn't throw if not...
            ramp_time = dwell_time * xy_num_elems
            focus_vel = array([2,0,0]) * xy_extreme_rel_to_base_ray / ramp_time # scan x
            

                
        return (focus_pos, focus_vel, ramp_time)
    
    [aodDirectionVectors, generalCentres, ~, aolDrives] = calculate_aol_drive(4, driveParams, aodMode)
    
    [baseFreqCompensated,chirp] = CompensateFreqForTransducerLocation(aodXyCentres, transducerOffsets, generalCentres, aodDirectionVectors, aolDrives)
    
    [a, b, c] = ComputeReturnsForLabview(baseFreqCompensated,chirp,rampTime)


    return (a, b, c, ticksPerRamp)