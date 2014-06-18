from numpy import array, linspace, outer, concatenate, zeros, tile, ceil, allclose, arange,\
    atleast_2d, dot
from aol_simple import AolSimple
from numpy.linalg.linalg import norm

def get_drive( \
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
                       ac_power, \
                       ac_velocity, \
                       op_wavelength, \
                       crystal_thickness, \
                       aod_spacing):

    aod_xy_centres = -1e-3 * array([ [0,0], [2.3,0], [4.6,2.3], [4.6,4.6] ])
    reference_shift = array([0, 0, 0])
    common_offsets = array([4.65, 5.45]) # common is for eliminating scan speed displacement
    differential_offsets = array([-0.85, 3.6]) # differential is for compensating XZ shifts

    transducer_offsets = -1e-3 * array([common_offsets(0) - differential_offsets(0),  \
                                       common_offsets(1) - differential_offsets(1),  \
                                       common_offsets(0) + differential_offsets(0),  \
                                       common_offsets(1) + differential_offsets(1)])

    aol = AolSimple.create_aol(order, op_wavelength, ac_velocity, aod_spacing, base_freq, \
                               pair_deflection_ratio, [0,0,100], [0,0,0], crystal_thickness=crystal_thickness)

    (a,b,c,t) = (array([[]]),array([[]]),array([[]]),array([[]]))  
    
    (focus_pos, focus_vel, ramp_time) = convert_normalised_to_cartesian(xy_num_elems, zoom_factor, acceptance_angle, focus_pos_normalised, \
                                                                        focus_disp_normalised, reference_shift)
    
    for m in range(len(focus_pos)):
        aol.update_drive(focus_pos[m], focus_vel[m], op_wavelength, base_freq, pair_deflection_ratio, crystal_thickness)
        
        base_freq_offset = compensate_freq_for_transducer_location(aol, aod_xy_centres, transducer_offsets, reference_shift)    
        
        (a_,b_,c_,t_) = compute_returns_for_labview(aol, base_freq_offset, ramp_time, system_clock_freq, data_time_interval)
        
        a = concatenate((a, atleast_2d(a_)))
        b = concatenate((b, atleast_2d(b_)))
        c = concatenate((c, atleast_2d(c_)))
        t = concatenate((t, atleast_2d(t_)))
        
    return (a,b,c,t)
 
def convert_normalised_to_cartesian(imaging_mode, xy_num_elems, zoom_factor, acceptance_angle, aod_aperture, \
                                    focus_pos_normalised, focus_disp_normalised, dwell_time, reference_shift):
    
    # Originally, half deflection went on each of the pair, so if max deflection on one is accAngle then total def is twice that, hence factor of 2 below
    z_focus_pos_normalised = focus_pos_normalised[:,2]
    z_focus_pos_normalised = (z_focus_pos_normalised == 0) * 1e-6 + z_focus_pos_normalised # avoid divide by 0
    
    z_focus_pos = aod_aperture / (4 * acceptance_angle * z_focus_pos_normalised)
    
    xy_extreme_rel_to_base_ray = 2 * acceptance_angle / zoom_factor * z_focus_pos
    
    (xy_focus_pos, xy_focus_vel, ramp_time) = adjust_for_mode(imaging_mode, xy_num_elems, xy_extreme_rel_to_base_ray, \
                                                              dwell_time, focus_disp_normalised, focus_pos_normalised)
    xy_focus_pos += reference_shift

    focus_pos = concatenate(xy_focus_pos, z_focus_pos)
    focus_vel = concatenate(xy_focus_vel, zeros( (xy_focus_vel.shape[1], 1) ))
    return (focus_pos, focus_vel, ramp_time)

def adjust_for_mode(imaging_mode, xy_num_elems, xy_extreme_rel_to_base_ray, dwell_time, focus_disp_normalised, focus_pos_normalised):
    xy_row_rel_to_base_ray = linspace(-xy_extreme_rel_to_base_ray, xy_extreme_rel_to_base_ray, xy_num_elems)
    if xy_num_elems == 1:
        xy_row_rel_to_base_ray = 0
    
    is_structural = imaging_mode == 0
    is_raster = imaging_mode == 1
    is_pointing = imaging_mode == 2
    is_miniscan = imaging_mode == 3
    
    if is_miniscan:
        ramp_time = dwell_time * xy_num_elems * norm(focus_disp_normalised[:,0:2], axis=0) / 2 # divide by 2 because scan from -1 to +1
        xy_focus_vel = focus_disp_normalised[:,0:2] * xy_extreme_rel_to_base_ray / ramp_time
        xy_focus_pos = focus_pos_normalised[:,0:2] * xy_extreme_rel_to_base_ray
        
    if is_pointing:
        ramp_time = tile(dwell_time, (xy_num_elems,1) )
        xy_focus_vel = 0 * focus_disp_normalised[:,0:2]
        xy_focus_pos = focus_pos_normalised[:,0:2] * xy_extreme_rel_to_base_ray

    if is_structural: # assumes single point but doesn't throw if not...
        ramp_time = tile(dwell_time, (xy_num_elems,1) )
        xy_focus_vel = tile([0,0], (xy_num_elems, 1))
        xy_focus_pos = outer(xy_row_rel_to_base_ray,[1,1])
        
    if is_raster: # assumes single point but doesn't throw if not...
        ramp_time = tile(dwell_time * xy_num_elems, (xy_num_elems,1) )
        xy_focus_vel = tile(array([2,0]) * xy_extreme_rel_to_base_ray / ramp_time, (xy_num_elems,1)) # scan x
        xy_focus_pos = outer(xy_row_rel_to_base_ray,[0,1])
        
    return (xy_focus_pos, xy_focus_vel, ramp_time)

def compensate_freq_for_transducer_location(aol, aod_xy_centres, transducer_offsets):
    linear = array([a.acoustic_drives.linear for a in aol.aods])
    ac_direction_vectors = array([a.acoustic_direction for a in aol.aods])

    time_from_transducer_to_base_ray = zeros(4)
    for k in arange(4):
        xy_displacement = aol.base_ray_positions[k] - aod_xy_centres[k]
        aod_aperture = aol.aods[k].aperture_width
        distance_transducer_to_base_ray = aod_aperture/2 + transducer_offsets[k] + dot(ac_direction_vectors[k], xy_displacement)
        time_from_transducer_to_base_ray[k] = distance_transducer_to_base_ray / aol.acoustic_drives[k].velocity
        
    return linear * time_from_transducer_to_base_ray

def compute_returns_for_labview(aol, base_freq_offset, ramp_time, system_clock_freq, data_time_interval):
    
    def swap_scale_round(arr, scaling):
        arr[:,[1,2]] = arr[:,[2,1]]
        arr *= scaling
        arr = ceil(arr)
        return arr
    
    const = [a.acoustic_drive.const for a in aol.aods]
    linear = [a.acoustic_drive.linear for a in aol.aods] 
    quad = linear * 0
    ac_velocity = [a.acoustic_drive.velocity for a in aol.aods]
    aod_aperture = [a.aperture_width for a in aol.aods]
    
    a = swap_scale_round(const, 2**32 / system_clock_freq)
    b = swap_scale_round(linear, 2**32 / system_clock_freq^2 / 8) # scale B down here and expand later
    c = swap_scale_round(quad, 2**32 / system_clock_freq^3)
    
    aod_fill_time = data_time_interval * ceil(aod_aperture / ac_velocity / data_time_interval)
    scan_time = aod_fill_time + ramp_time # the time needed for each point
    ticks_per_ramp =  swap_scale_round( tile(scan_time, (4,1) ), system_clock_freq)

    return (a, b, c, ticks_per_ramp)