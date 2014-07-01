from optimise_aol import set_up_aol
from scan_speed_efficiency import calculate_efficiency

op_wavelength = 800e-9
aol = set_up_aol(op_wavelength=op_wavelength, focus_position=[0,0,1]) 
  
def test_calculate_efficiency():
    e0 = calculate_efficiency(aol, 0)
    e1 = calculate_efficiency(aol, 1e-4)
    assert e0 > 0.36 and e1 < 2e-2
    
if __name__ == '__main__':
    test_calculate_efficiency()