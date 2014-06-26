from aol_full import AolFull
from aod import Aod
from ray import Ray
from numpy import array, arange, append, sqrt, dtype, isnan, linspace, pi, cos, sin, arctan2
from numpy.linalg import norm
from scipy import optimize
from vector_utils import normalise_list
from aod_visualisation import generic_plot_surface
import optimisation_params
from optimisation_params import OptParams

op_wavelength = 800e-9

def optimise_nth_aod_by_hand(aod_num, aol):
    p = OptParams()
    p.configure_traits()
    
    result = optimize.fminbound(min_fun, p.min_val(), p.max_val(), (p, aod_num, aol), full_output=True)
    new_optimal_normal = p.get_normal(result[0])
    change_orientation(aol, aod_num, new_optimal_normal)
    return new_optimal_normal

def plot_region(aod_num, aol):
    def func(x_deg, y_deg):
        x = x_deg * pi/180
        y = y_deg * pi/180
        new_normal = [x, y, sqrt(1 - x**2 - y**2)]
        change_orientation(aol, aod_num, new_normal)
        energies = calculate_efficiency(aol, aod_num)
        print '.'
        return energies
        
    labels = ["incidence angle / deg","transverse incidence angle / deg","efficiency"]
    generic_plot_surface(linspace(-0.1, 0.1, 50)*180/pi, linspace(-0.1, 0.1, 50)*180/pi, func, labels)

def min_fun(variable, params, aod_num, aol):
    new_normal = params.get_normal(variable)
    change_orientation(aol, aod_num, new_normal)
    print ','
    return - calculate_efficiency(aol, aod_num)

def set_up_aol():
    order = 1
    base_freq = 35e6
    pair_deflection_ratio = 1
    
    focal_length = -1e1
    focus_position = array([1e-1,0,focal_length])
    focus_velocity = [0,0,0]
    
    aod_spacing = array([5e-2] * 3)
    
    orientations = normalise_list(array([ [ 0.03901281, 0., 0.99923871], \
                                          [ 0.05585054, 0.03899298, 0.99767744], \
                                          [ 0.00671442,  0.05235988, 0.99860571], \
                                          [ 0., 6.64008463e-03, 9.99977954e-01] ]))
    
    aods = [0]*4
    aods[0] = Aod(orientations[0], [ 1, 0,0], 25e-3, 3.6e-3, 8e-3)
    aods[1] = Aod(orientations[1], [ 0, 1,0], 15e-3, 3.6e-3, 8e-3)
    aods[2] = Aod(orientations[2], [-1, 0,0], 15e-3, 1.2e-3, 8e-3)
    aods[3] = Aod(orientations[3], [ 0,-1,0], 15e-3, 1.2e-3, 8e-3)

    return AolFull.create_aol(aods, aod_spacing, order, op_wavelength, base_freq, pair_deflection_ratio, focus_position, focus_velocity)

def change_orientation(aol, aod_num, new_normal):
    assert not any(isnan(new_normal))
    aol.aods[aod_num-1].normal = array(new_normal)

def calculate_efficiency(aol, after_nth_aod):
    time_array = (arange(3)-1)*5e-5
    x_array = (arange(3)-1)*2e-3
    y_array = x_array
    
    energy = 0
    ray_count = 0
    
    rays = [0] * len(x_array) * len(y_array)
    for t in time_array:
        for xn in range(len(x_array)):
            for yn in range(len(y_array)):    
                rays[xn + yn*len(x_array)] = Ray([x_array[xn],y_array[yn],0], [0,0,1], op_wavelength)
        
        (_,energies) = aol.propagate_to_distance_past_aol(rays, t)
        energy += sum(energies[:,after_nth_aod-1])
        ray_count += len(rays)
                
    return energy / ray_count

if __name__ == '__main__':
    aol = set_up_aol()
    #plot_region(4, aol)
    #optimise_nth_aod_by_hand(4, aol)
    print calculate_efficiency(aol, 4)
    print calculate_efficiency(aol, 3)
    print calculate_efficiency(aol, 2)
    print calculate_efficiency(aol, 1)
