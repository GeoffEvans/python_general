from aol_full import AolFull
from aod import Aod
from ray import Ray
from numpy import allclose, array, arange, outer, linspace, meshgrid, ravel
from random import random as r

order = 1
op_wavelength = 800e-9
base_freq = 40e6
pair_deflection_ratio = 0.8

focal_length = 1
focus_position = array([.03,.04,focal_length])
focus_velocity = [0,1,0]

aod_spacing = array([5e-2] * 3)

aods = [0]*4
aods[0] = Aod([0,0,1], [ 1, 0,0], 25e-3, 3.2e-3, 8e-3)
aods[1] = Aod([0,0,1], [ 0, 1,0], 25e-3, 3.2e-3, 8e-3)
aods[2] = Aod([0,0,1], [-1, 0,0], 25e-3, 1.6e-3, 8e-3)
aods[3] = Aod([0,0,1], [ 0,-1,0], 25e-3, 1.6e-3, 8e-3)

aol = AolFull.create_aol(aods, aod_spacing, order, op_wavelength, base_freq, pair_deflection_ratio, focus_position, focus_velocity)

def test_plot():
    x,y = meshgrid(linspace(-1,1,10)*1e-2, linspace(-1,1,10)*1e-2)
    list_of_positions = zip(x.ravel(), y.ravel()) 
    rays = [Ray([xy[0], xy[1], 0], [0,0,1], 800e-9) for xy in list_of_positions]
    aol.plot_ray_through_aol(rays, 0, focus_position[2]+1)

def test_ray_passes_through_focus():
    location = [0]*100
    for t in arange(100):
        ray = Ray([r()*5e-2,r()*5e-2,0], [0,0,1], 800e-9)
        aol.propagate_to_distance_past_aol([ray], 0, focal_length)
        location[t] = ray.position
        
    focus_theory = focus_position + [0,0,aod_spacing.sum()] + [0.005, 0.005, 0] # some additional offset constant...
    assert allclose(location, focus_theory, rtol=1e-2, atol=0) and allclose(location, location[0], rtol=1e-3, atol=0)

def test_ray_scans_correctly():
    location = [0]*100
    for t in arange(100):
        ray = Ray([r()*5e-2,r()*5e-2,0], [0,0,1], 800e-9)
        aol.propagate_to_distance_past_aol([ray], t*1e-6, focal_length)
        location[t] = ray.position
    
    focus_theory = focus_position + [0,0,aod_spacing.sum()] + [5e-3, 5e-3, 0] + outer(arange(100)*1e-6, focus_velocity)
    assert allclose(location, focus_theory, rtol=1e-2, atol=0)

test_ray_scans_correctly()
def test_efficiency_low_at_angle():
    ray = Ray([0,0,0], [3./5,0,4./5], 800e-9)
    aol.propagate_to_distance_past_aol([ray], 0, focal_length)
    assert ray.energy < 1e-9