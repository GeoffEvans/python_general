from aol_full import AolFull
from aod import Aod
from ray import Ray
from numpy import array, arange
from vector_utils import normalise_list

def set_up_aol(order=-1, op_wavelength=800e-9, base_freq=35e6, \
               focus_position=[0,0,1e21], focus_velocity=[0,0,0], \
               pair_deflection_ratio=1, ac_power=[1,1,3,3]):
    orientations = normalise_list(array([ [ -0.03901281, -0., 0.99923871], \
                                          [ -0.05585054, -0.03899298, 0.99767744], \
                                          [ -0.00671442,  -0.05235988, 0.99860571], \
                                          [ -0., -6.64008463e-03, 9.99977954e-01] ]))
    aod_spacing = array([5e-2] * 3)
    aods = [0]*4
    aods[0] = Aod(orientations[0], [ 1, 0,0], 16e-3, 3.6e-3, 8e-3)
    aods[1] = Aod(orientations[1], [ 0, 1,0], 16e-3, 3.6e-3, 8e-3)
    aods[2] = Aod(orientations[2], [-1, 0,0], 16e-3, 1.2e-3, 8e-3)
    aods[3] = Aod(orientations[3], [ 0,-1,0], 16e-3, 1.2e-3, 8e-3)

    return AolFull.create_aol(aods, aod_spacing, order, op_wavelength, base_freq, pair_deflection_ratio, focus_position, focus_velocity, ac_power=ac_power)

def get_ray_bundle(op_wavelength=800e-9, spacing=5e-3):
    x_array = (arange(3)-1)*spacing
    y_array = x_array
    
    rays = [0] * len(x_array) * len(y_array)
    for xn in range(len(x_array)):
        for yn in range(len(y_array)):    
            rays[xn + yn*len(x_array)] = Ray([x_array[xn],y_array[yn],0], [0,0,1], op_wavelength)
            
    return rays