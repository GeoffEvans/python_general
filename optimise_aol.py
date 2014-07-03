from numpy import arange, sqrt, linspace, pi
from scipy import optimize
from aod_visualisation import generic_plot_surface
from optimisation_params import OptParams
from set_up_utils import set_up_aol, get_ray_bundle

op_wavelength = 800e-9

def optimise_nth_aod_by_hand(aod_num, aol):
    p = OptParams()
    p.configure_traits()
    
    result = optimize.fminbound(min_fun, p.min_val(), p.max_val(), (p, aod_num, aol), full_output=True)
    new_optimal_normal = p.get_normal(result[0])
    aol.change_orientation(aod_num, new_optimal_normal)
    return new_optimal_normal

def plot_region(aod_num, aol):
    
    def func(scan_deg, y_deg):
        x = scan_deg * pi/180
        y = y_deg * pi/180
        new_normal = [x, y, sqrt(1 - x**2 - y**2)]
        aol.change_orientation(aod_num, new_normal)
        energies = calculate_efficiency(aol, aod_num)
        return energies
        
    labels = ["incidence angle / deg","transverse incidence angle / deg","efficiency"]
    generic_plot_surface(linspace(-0.1, 0.1, 30)*180/pi, linspace(-0.1, 0.1, 30)*180/pi, func, labels)

def min_fun(variable, params, aod_num, aol):
    new_normal = params.get_normal(variable)
    aol.change_orientation(aod_num, new_normal)
    return - calculate_efficiency(aol, aod_num)

def calculate_efficiency(aol, after_nth_aod, op_wavelength=op_wavelength):
    time_array = (arange(3)-1)*5e-5
    
    energy = 0
    ray_count = 0
    
    for t in time_array:
        rays = get_ray_bundle(op_wavelength)
        
        (_,energies) = aol.propagate_to_distance_past_aol(rays, t)
        energy += sum(energies[:,after_nth_aod-1])
        ray_count += len(rays)
                
    return energy / ray_count

if __name__ == '__main__':
    aol = set_up_aol(op_wavelength=op_wavelength)
    plot_region(1, aol)
    #optimise_nth_aod_by_hand(1, aol)
    #print calculate_efficiency(aol, 4)

