from aol_full import AolFull
from aod import Aod
from ray import Ray
from numpy import array, arange, exp, power
from vector_utils import normalise_list

def set_up_aol( op_wavelength, \
                order=-1, \
                base_freq=40e6, \
                focus_position=[0,0,1e12], \
                focus_velocity=[0,0,0], \
                pair_deflection_ratio=1, \
                ac_power=[1,1,2,2]):
   
    # for centre freq = 40MHz
    orient40  = normalise_list(array([ \
        [ -3.60119805e-02,   1.20407784e-18,  9.99351358e-01], \
        [-0.04799655, -0.03600276,  0.99819844], \
        [-0.01577645, -0.04799655,  0.9987229 ], \
        [ 0.00872665, -0.01570224,  0.99983863]]))
   
    # for centre freq = 35MHz
    orient35 = normalise_list(array([ \
        [ -3.92662040e-02, -0., 9.99228785e-01], \
        [ -0.04613158, -0.03934167,  0.99816036], \
        [ -0.01187817, -0.04380776,  0.99896936], \
        [ 0, -1.17766548e-02,  9.99930653e-01] ]))
    
    # for centre freq = 39MHz     --- rig3
    orient39 = normalise_list(array([ \
        [-0.03634428, 0., 0.99933933], \
        [-0.05410521, -0.03632524,  0.99787429], \
        [-0.02185263, -0.04939282, 0.99854034], \
        [ 0, -2.17538221e-02, 9.99763358e-01] ]))

    aod_spacing = array([5e-2] * 3)
    aods = [0]*4
    orientations = orient40
    aods[0] = make_aod_wide(orientations[0], [1,0,0])
    aods[1] = make_aod_wide(orientations[1], [0,1,0])
    aods[2] = make_aod_narrow(orientations[2], [-1,0,0])
    aods[3] = make_aod_narrow2(orientations[3], [0,-1,0])

    return AolFull.create_aol(aods, aod_spacing, order, op_wavelength, base_freq, pair_deflection_ratio, focus_position, focus_velocity, ac_power=ac_power)

def get_ray_bundle(op_wavelength=800e-9, spacing=5e-3):
    x_array = (arange(3)-1)*spacing
    y_array = x_array
    
    rays = [0] * len(x_array) * len(y_array)
    for xn in range(len(x_array)):
        for yn in range(len(y_array)):    
            rays[xn + yn*len(x_array)] = Ray([x_array[xn],y_array[yn],0], [0,0,1], op_wavelength)
            
    return rays

def p(x, width):
    val = x*0 
    val[x > 0] = exp(-power(x[x > 0], -1) * width)
    return val
    
def q(x, width):
    val = x*0    
    val[[x > 0]] = p(x[x > 0], width) / (p(x[x > 0], width) + p(width - x[x > 0], width))
    return val
    
def r(x, lower, lower_width, upper, upper_width): # 11.13 Priestley, Introduction to Integration
    return q(upper - x, upper_width) * q(x - lower, lower_width)

def transducer_efficiency_narrow(freq): 
    return r(array(freq), 12e6, 10e6, 95e6, 70e6)
def transducer_efficiency_narrow2(freq):
    return r(array(freq), 12e6, 10e6, 70e6, 35e6)
def transducer_efficiency_wide(freq):
    return transducer_efficiency_narrow(freq)
    
def make_aod_wide(orientation, ac_dir):
    return Aod(orientation, ac_dir, 16e-3, 3.3e-3, 8e-3, transducer_efficiency_wide)
def make_aod_narrow(orientation, ac_dir):
    return Aod(orientation, ac_dir, 16e-3, 1.2e-3, 8e-3, transducer_efficiency_narrow)
def make_aod_narrow2(orientation, ac_dir):
    return Aod(orientation, ac_dir, 16e-3, 1.2e-3, 8e-3, transducer_efficiency_narrow2)