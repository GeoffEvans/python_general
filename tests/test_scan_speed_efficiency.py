from optimise_aol import set_up_aol
from aod_visualisation import multi_line_plot, generic_plot_surface
from numpy import linspace, pi, arange, dot, sin, cos, array, arctan2
from ray import Ray
from scan_speed_efficiency import calculate_efficiency

op_wavelength = 800e-9
aol = set_up_aol() 
  
def test_calculate_efficiency():
    e0 = calculate_efficiency(aol, 0)
    e1 = calculate_efficiency(aol, 1e-2)
    assert e0 > 0.36 and e1 < 1e-3
    
if __name__ == '__main__':
    test_calculate_efficiency()