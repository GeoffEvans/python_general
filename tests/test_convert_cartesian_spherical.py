from aol_model.convert_cartesian_spherical import *
from numpy import allclose, pi, array
from scipy import rand

def test_cart_to_sph_and_back():
    xyz = rand(3,100)
    sph = cartesian_to_spherical(xyz)
    xyz_new = spherical_to_cartesian(sph)
    assert allclose(xyz, xyz_new)

def test_spherical_to_cartesian_special():
    r = array([1,2,3])
    theta = array([0,pi/2,pi/2])
    phi = array([0,0,pi/2])
    sph = vstack( (r, theta, phi) )
    xyz = spherical_to_cartesian(sph)
    expected = array([[0,2,0],[0,0,3],[1,0,0]])
    assert allclose(xyz,expected)
    
