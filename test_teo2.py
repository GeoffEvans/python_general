from teo2_optical import *
from numpy import pi, arange

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
    
    n_e_eq = equal_within_tol(refractive_indices[0], n_e_vals, 0.0001)
    n_o_eq = equal_within_tol(refractive_indices[1], n_o_vals, 0.0001)
    
    return n_o_eq & n_e_eq
    
def test_symmetry():
   
    def all_elements_same(lst):
        same = lst[1:] == lst[:-1]
        return same.all()
   
    angles = array([0.3,-0.3,0.3+pi,-0.3+pi])
    refractive_indices = calc_refractive_indices(angles)
    
    ext_same = all_elements_same(refractive_indices[0])
    ord_same = all_elements_same(refractive_indices[1])
    
    assert ext_same & ord_same 

def test_polarisation_extremes():
    
    def check_pols(pair):
        return pair[0].real == 0.0 & pair[1].imag == 0.0
        
    angles = array([0,pi/2])
    pols = calc_polarisations(angles)
    assert check_pols(pols[0]) & check_pols(pols[1])

def equal_within_tol(x,val,tol):
    diff = abs(x-val)
    eq = diff < tol
    return eq.all()