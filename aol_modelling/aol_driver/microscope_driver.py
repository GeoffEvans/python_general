from numpy import array, linspace, outer, concatenate, zeros, tile, ceil, allclose, arange,\
    atleast_2d, dot, mean
from aol_model.aol_simple import AolSimple
from numpy.linalg.linalg import norm

mode_structural = 0
mode_raster = 1
mode_pointing = 2
mode_miniscan = 3

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
                       aod_apertures, \
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

    aol_simple = AolSimple.create_aol(order, op_wavelength, ac_velocity, aod_spacing, base_freq, \
                               pair_deflection_ratio, [0,0,100], [0,0,0], crystal_thickness=crystal_thickness)

    (a,b,c,t) = (array([[]]),array([[]]),array([[]]),array([[]]))  
    
    (focus_pos, focus_vel, ramp_time) = convert_normalised_to_cartesian(imaging_mode, xy_num_elems, zoom_factor, acceptance_angle, aod_apertures, \
                                                                        focus_pos_normalised, focus_disp_normalised, dwell_time, reference_shift)
    
    for m in range(len(focus_pos)):
        aol_simple.update_drive(focus_pos[m], focus_vel[m], op_wavelength, base_freq, pair_deflection_ratio, crystal_thickness)
        
        base_freq_offset = compensate_freq_for_transducer_location(aol_simple, aod_xy_centres, transducer_offsets, reference_shift, aod_apertures)    
        
        (a_,b_,c_,t_) = compute_returns_for_labview(aol_simple, base_freq_offset, ramp_time, system_clock_freq, data_time_interval)
        
        a = concatenate((a, atleast_2d(a_)))
        b = concatenate((b, atleast_2d(b_)))
        c = concatenate((c, atleast_2d(c_)))
        t = concatenate((t, atleast_2d(t_)))
        
    return (a,b,c,t)
 
def convert_normalised_to_cartesian(imaging_mode, xy_num_elems, zoom_factor, acceptance_angle, aod_apertures, \
                                    focus_pos_normalised, focus_disp_normalised, dwell_time, reference_shift):
    is_structural = (imaging_mode == mode_structural)
    is_raster = (imaging_mode == mode_raster)
    is_pointing = (imaging_mode == mode_pointing)
    is_miniscan = (imaging_mode == mode_miniscan)
    
    # Originally, half deflection went on each of the pair, so if max deflection on one is accAngle then total def is twice that, hence factor of 2 below
    z_focus_pos_normalised = focus_pos_normalised[:,2]
    z_focus_pos_normalised[z_focus_pos_normalised == 0] +=  1e-7 # avoid divide by 0, don't try to use inf because it doesn't work in cartesian coords

    z_focus_pos = mean(aod_apertures) / (4 * acceptance_angle * z_focus_pos_normalised) + reference_shift[2]
    xy_extreme_rel_to_base_ray = 2 * acceptance_angle / zoom_factor * z_focus_pos
    
    if is_structural or is_raster:
        z_focus_pos = [z_focus_pos[0]]*xy_num_elems # should only be looking at one z plane but don't worry if not...
        xy_extreme_rel_to_base_ray = xy_extreme_rel_to_base_ray[0]
        
        xy_row_rel_to_base_ray = linspace(-xy_extreme_rel_to_base_ray, xy_extreme_rel_to_base_ray, xy_num_elems)
        if xy_num_elems == 1:
            xy_row_rel_to_base_ray = 0
    
    if is_structural: 
        ramp_time = tile(dwell_time, xy_num_elems )
        xy_focus_vel = tile([0,0], (xy_num_elems, 1))
        xy_focus_pos = outer(xy_row_rel_to_base_ray,[1,1])
        
    if is_raster: 
        ramp_time = tile(dwell_time * xy_num_elems, xy_num_elems )
        xy_focus_vel = outer(xy_extreme_rel_to_base_ray / ramp_time, array([2,0])) # scan x
        xy_focus_pos = outer(xy_row_rel_to_base_ray,[0,1])
            
    if is_miniscan:
        ramp_time = dwell_time * xy_num_elems * norm(focus_disp_normalised[:,0:2], axis=0) / 2 # divide by 2 because scan from -1 to +1
        xy_focus_vel = focus_disp_normalised[:,0:2] * xy_extreme_rel_to_base_ray / ramp_time
        xy_focus_pos = focus_pos_normalised[:,0:2] * xy_extreme_rel_to_base_ray
        
    if is_pointing:
        ramp_time = tile(dwell_time, focus_disp_normalised.shape[0] )
        xy_focus_vel = 0 * focus_disp_normalised[:,0:2]
        xy_focus_pos = focus_pos_normalised[:,0:2] * xy_extreme_rel_to_base_ray
    
    xy_focus_pos += reference_shift[0:2]
    focus_pos = concatenate( (xy_focus_pos, atleast_2d(z_focus_pos).T), axis=1)
    
    z_vel_zeros = zeros( (xy_focus_vel.shape[0], 1) )
    focus_vel = concatenate( (xy_focus_vel, z_vel_zeros), axis=1)
    
    return (focus_pos, focus_vel, ramp_time)

def compensate_freq_for_transducer_location(aol_simple, aod_xy_centres, transducer_offsets, aod_apertures):
    linear = array([a.linear for a in aol_simple.acoustic_drives])
    ac_direction_vectors = array([a for a in aol_simple.aod_directions])

    time_from_transducer_to_base_ray = zeros(4)
    for k in arange(4):
        xy_displacement = aol_simple.base_ray_positions[k] - aod_xy_centres[k]
        distance_transducer_to_base_ray = aod_apertures[k]/2 + transducer_offsets[k] + dot(ac_direction_vectors[k,0:2], xy_displacement)
        time_from_transducer_to_base_ray[k] = distance_transducer_to_base_ray / aol_simple.acoustic_drives[k].velocity
        
    freq_offset = linear * time_from_transducer_to_base_ray
    return freq_offset

def compute_returns_for_labview(aol_simple, base_freq_offset, ramp_time, system_clock_freq, data_time_interval, aod_apertures):
    
    def swap_scale_round(arr, scaling):
        arr[:,[1,2]] = arr[:,[2,1]]
        arr *= scaling
        arr = ceil(arr)
        return arr
    
    const = [a.const for a in aol_simple.acoustic_drives]
    linear = [a.linear for a in aol_simple.acoustic_drives] 
    quad = linear * 0
    ac_velocity = [a.velocity for a in aol_simple.acoustic_drives]
    aod_apertures
    
    a = swap_scale_round(const, 2**32 / system_clock_freq)
    b = swap_scale_round(linear, 2**32 / system_clock_freq^2 / 8) # scale B down here and expand later
    c = swap_scale_round(quad, 2**32 / system_clock_freq^3)
    
    aod_fill_times = data_time_interval * ceil(aod_apertures / ac_velocity / data_time_interval)
    scan_times = outer(aod_fill_times, ramp_time) # the time needed for each point
    ticks_per_ramp =  swap_scale_round(scan_times, system_clock_freq)

    return (a, b, c, ticks_per_ramp)