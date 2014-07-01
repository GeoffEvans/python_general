from plot_utils import multi_line_plot, generic_plot_surface_vals
from numpy import linspace, pi, array, meshgrid, arange, prod, transpose
from set_up_utils import get_ray_bundle, set_up_aol
from test_aol_full import focal_length

op_wavelength = 800e-9

def plot_lines(focal_length):
    x_rad = linspace(-10, 10, 10) * 1e-3
    x_deg = x_rad * 180/pi
    x = x_rad * focal_length
    focus_position_many = transpose(array([x, 0*x, focal_length+0*x]), [1,2,0])
    effs = get_effs(focus_position_many)
    
    labels = ["xangle / deg", "efficiency"]
    #do the plot....
        
def plot_surf(focal_length):
    x_rad = linspace(-10, 10, 10) * 1e-3
    x_deg = x_rad * 180/pi
    y_deg = x_deg

    x_array = x_rad * focal_length
    y_array = x_array
    
    (x, y) = meshgrid(x_array, y_array)
    focus_position_many = transpose(array([x, y, focal_length+0*x]), [1,2,0])
    
    effs = get_effs(focus_position_many)
    
    labels = ["xangle / deg", "yangle / deg", "efficiency"]
    generic_plot_surface_vals(x, y, array(effs), labels)   

def get_effs(focus_position_many):
    shp = focus_position_many.shape[0:2]
    aols = [set_up_aol(focus_position=f, op_wavelength=op_wavelength) for f in focus_position_many.reshape(prod(shp), 3)] 
    effs = [calculate_efficiency(a) for a in aols]
    return array(effs).reshape(shp)
    
def calculate_efficiency(aol):
    time_array = (arange(3)-1)*5e-5
    energy = 0
    ray_count = 0

    for time in time_array:
        rays = get_ray_bundle(op_wavelength, 2e-3)
        (_,energies) = aol.propagate_to_distance_past_aol(rays, time, 0)
        energy += sum(energies[:,-1])
        ray_count += len(rays)
                
    return energy / ray_count

if __name__ == '__main__':
    plot_surf(1e1)