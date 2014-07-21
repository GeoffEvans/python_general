from aol_full import AolFull
from aod import Aod
from ray import Ray
from numpy import array, arange, exp, power
from vector_utils import normalise_list

def set_up_aol( order=-1, \
                op_wavelength=800e-9, \
                base_freq=35e6, \
                focus_position=[0,0,1e21], \
                focus_velocity=[0,0,0], \
                pair_deflection_ratio=1, \
                ac_power=[1,1,3,3]):
                   
    orientations_flat = normalise_list(array([ [ -3.92662040e-02, -0., 9.99228785e-01], \
                                          [ -0.04613158, -0.03934167,  0.99816036], \
                                          [ -0.01187817, -0.04380776,  0.99896936], \
                                          [ 0, -1.17766548e-02,  9.99930653e-01] ]))

    aod_spacing = array([5e-2] * 3)
    aods = [0]*4
    aods[0] = make_aod_wide(orientations_flat[0], [1,0,0])
    aods[1] = make_aod_wide(orientations_flat[1], [0,1,0])
    aods[2] = make_aod_narrow(orientations_flat[2], [-1,0,0])
    aods[3] = make_aod_narrow(orientations_flat[3], [0,-1,0])

    return AolFull.create_aol(aods, aod_spacing, order, op_wavelength, base_freq, pair_deflection_ratio, focus_position, focus_velocity, ac_power=ac_power)

def get_ray_bundle(op_wavelength=800e-9, spacing=5e-3):
    x_array = (arange(3)-1)*spacing
    y_array = x_array
    
    rays = [0] * len(x_array) * len(y_array)
    for xn in range(len(x_array)):
        for yn in range(len(y_array)):    
            rays[xn + yn*len(x_array)] = Ray([x_array[xn],y_array[yn],0], [0,0,1], op_wavelength)
            
    return rays

def transducer_efficiency_narrow(x):
    return exp(- power(array(x) - 40e6, 2.) / (2 * power(30e6, 2.)))
def transducer_efficiency_wide(x):
    return exp(- power(array(x) - 40e6, 2.) / (2 * power(14e6, 2.)))
    
def make_aod_wide(orientation, ac_dir):
    return Aod(orientation, ac_dir, 16e-3, 3.6e-3, 8e-3, transducer_efficiency_wide)
def make_aod_narrow(orientation, ac_dir):
    return Aod(orientation, ac_dir, 16e-3, 1.2e-3, 8e-3, transducer_efficiency_narrow)