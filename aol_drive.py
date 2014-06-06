from numpy import array, append, dtype

def calculate_drive_freq_4(order, op_wavelength, ac_velocity, aod_spacing, crystal_depth, base_freq, pair_deflection_ratio, focus_position, focus_velocity):
    
    spacing_correction = crystal_depth * (1 - 1/2.26) # 2.26 is approx TeO2 refractive index
    spacing = append(array(aod_spacing, dtype=dtype(float)), focus_position[2]) - spacing_correction 
    xy_deflection = focus_position[0:2]
    xy_focus_velocity = focus_velocity[0:2]
    
    const = find_constant(order, op_wavelength, ac_velocity, spacing, base_freq, pair_deflection_ratio, xy_deflection)
    linear = find_linear(order, op_wavelength, ac_velocity, spacing, base_freq, pair_deflection_ratio, xy_focus_velocity)
    quadratic = 0 # not yet implemented
    return (const, linear, quadratic)

def find_constant(order, op_wavelength, ac_velocity, spacing, base_freq, pair_deflection_ratio, xy_deflection):
    
    # for constant components, choose r to represent the ratio of ANGULAR deflection on the first of the pair to the second of the pair
    # traditionally, this means r = 1, while all on the second would be r = 0
    
    multiplier = ac_velocity / op_wavelength / order

    dfx = (multiplier * xy_deflection[0] - base_freq * spacing[0:2].sum()) / (pair_deflection_ratio * spacing[0:4].sum() + spacing[2:4].sum())
    dfy = (multiplier * xy_deflection[1] - base_freq * spacing[1:3].sum()) / (pair_deflection_ratio * spacing[1:4].sum() + spacing[3:4].sum())
    
    return array([base_freq + pair_deflection_ratio * dfx, \
                  base_freq + pair_deflection_ratio * dfy, \
                  base_freq - dfx, \
                  base_freq - dfy ])

def find_linear(order, op_wavelength, ac_velocity, spacing, base_freq, pair_deflection_ratio, xy_focus_velocity):
    
    v = xy_focus_velocity / ac_velocity
    
    return array([(1 + v[0])/((1 + v[0]) * spacing[0:2].sum() + 2 * spacing[2:4].sum()), \
                  (1 + v[1])/((1 + v[1]) * spacing[1:3].sum() + 2 * spacing[3:4].sum()), \
                  (1 - v[0])/(2 * spacing[2:4].sum()), \
                  (1 - v[1])/(2 * spacing[3:4].sum()) ])
