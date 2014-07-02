from plot_utils import generic_plot_surface_vals, multi_line_plot_vals
from numpy import linspace, pi, array, meshgrid, arange, prod, transpose, outer
from set_up_utils import get_ray_bundle, set_up_aol
from test_aol_full import focal_length

op_wavelength = 800e-9

def plot_fov_lines(focal_lengths):
    x_rad = linspace(-18, 18, 18) * 1e-3
    x_deg = x_rad * 180/pi
    focus_position_many = []
    for f in focal_lengths:
        x = f * x_rad
        focus_position_many.append( array([x, 0*x, f+0*x]) )
    effs = get_effs(transpose(focus_position_many, [0,2,1]))
    
    labels = ["xangle / deg", "efficiency"]
    multi_line_plot_vals(x_deg, array(effs), labels, focal_lengths, (min(x_deg),max(x_deg),0,1))
        
def plot_fov_surf(focal_length):
    x_rad = linspace(-10, 10, 10) * 1e-3
    x_deg = x_rad * 180/pi
    (x_deg_m, y_deg_m) = meshgrid(x_deg, x_deg) 

    x_array = x_rad * focal_length
    (x, y) = meshgrid(x_array, x_array)
    focus_position_many = transpose(array([x, y, focal_length+0*x]), [1,2,0])
    
    effs = get_effs(focus_position_many)
    
    labels = ["xangle / deg", "yangle / deg", "efficiency"]
    generic_plot_surface_vals(x_deg_m, y_deg_m, array(effs), labels)   

def get_effs(focus_position_many):
    #get eff for a 2d array for focus positions (so 3d array input)
    shp = focus_position_many.shape[0:2]
    aols = [set_up_aol(focus_position=f, op_wavelength=op_wavelength) for f in focus_position_many.reshape(prod(shp), 3)] 
    effs = [calculate_efficiency(a) for a in aols]
    return array(effs).reshape(shp)
    
def calculate_efficiency(aol):
    time_array = (arange(3)-1)*5e-5
    energy = 0
    ray_count = 0

    for time in time_array:
        rays = get_ray_bundle(op_wavelength)
        (_,energies) = aol.propagate_to_distance_past_aol(rays, time, 0)
        energy += sum(energies[:,-1])
        ray_count += len(rays)
                
    return energy / ray_count

if __name__ == '__main__':
    plot_fov_lines([1e0, 2, 3e0, 1e1, 1e6, 1e12])