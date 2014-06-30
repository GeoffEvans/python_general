from optimise_aol import set_up_aol
from aod_visualisation import generic_plot, generic_plot_surface
from numpy import linspace, pi, arange, dot, sin, cos, array, arctan2
from ray import Ray

op_wavelength = 900e-9

def plot_line(focal_length, vel):
    focus_velocity = vel
    angle_of_scan = arctan2(focus_velocity[1], focus_velocity[0])
    focus_position_tzero = [0,0,focal_length]
    aol = set_up_aol(focus_position=focus_position_tzero, focus_velocity=focus_velocity, op_wavelength=op_wavelength)
    
    def func(scan_deg):
        scan_distance = focal_length * scan_deg * pi / 180
        focus_position = scan_distance * array([cos(angle_of_scan), sin(angle_of_scan), 0]) + focus_position_tzero
        time = dot(focus_position, focus_velocity) / dot(focus_velocity, focus_velocity)
        return calculate_efficiency(aol, time)
    
    labels = ["scan angle / deg", "efficiency"]
    scan_range_mrad = linspace(-20, 20, 40)
    generic_plot(scan_range_mrad * 180/pi * 1e-3, func, labels)
    
def calculate_efficiency(aol, time):
    x_array = (arange(3)-1)*2e-3
    y_array = x_array
    
    rays = [0] * len(x_array) * len(y_array)
    for xn in range(len(x_array)):
        for yn in range(len(y_array)):    
            rays[xn + yn*len(x_array)] = Ray([x_array[xn],y_array[yn],0], [0,0,1], op_wavelength)
                
    (_,energies) = aol.propagate_to_distance_past_aol(rays, time)
    energy = sum(energies[:,-1])
    ray_count = len(rays)
                
    return energy / ray_count

if __name__ == '__main__':
    
    plot_line(1, [1,0,0])
