from teo2 import calc_refractive_indices, calc_polarisations, principal_refractive_indices
from numpy import pi, arange, allclose, array

def test_ord_less_than_ext():
    angles = arange(0,pi/2,pi/10)
    refractive_indices = calc_refractive_indices(angles)
    
    ord_less_than_ext = refractive_indices[1] < refractive_indices[0]
    assert ord_less_than_ext.all()

def test_extreme_ref_vals():
    angles = array([0,pi/2])
    refractive_indices = calc_refractive_indices(angles)
    
    n_e_vals = [2.2598,principal_refractive_indices[0]]
    n_o_vals = [2.2596,principal_refractive_indices[1]]
    
    n_e_eq = allclose(refractive_indices[0], n_e_vals, atol=1e-4)
    n_o_eq = allclose(refractive_indices[1], n_o_vals, atol=1e-4)
    
    return n_o_eq and n_e_eq
    
def test_symmetry():
   
    def all_elements_same(lst):
        return allclose(lst, lst[0], atol=1e-15)
   
    angles = array([0.3,-0.3,0.3+pi,-0.3+pi])
    refractive_indices = calc_refractive_indices(angles)
    
    ext_same = all_elements_same(refractive_indices[0])
    ord_same = all_elements_same(refractive_indices[1])
    
    assert ext_same and ord_same 

def test_polarisation_extremes():
    angles = array([0,pi/2])
    pols = calc_polarisations(angles)
    
    ext = pols[0]
    on_axis_is_circular = allclose(ext[0].real, 0.0, atol=1e-15) and allclose(ext[0].imag, 1.0, atol=1e-15) 
    off_axis_is_linear = abs(ext[1]) > 903
    ext_pass = on_axis_is_circular and off_axis_is_linear
    
    ordin = pols[1]
    on_axis_is_circular = allclose(ordin[0].real, 0.0, atol=1e-15) and allclose(ordin[0].imag, -1.0, atol=1e-15) 
    off_axis_is_linear = abs(ext[1]) > 1/903
    ord_pass = on_axis_is_circular and off_axis_is_linear
        
    assert ord_pass and ext_pass