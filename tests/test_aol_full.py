from aol_full import AolFull
from aod import Aod
from ray import Ray
from numpy import allclose, array, arange, outer, linspace, meshgrid, dot
from random import random as r
from vector_utils import normalise
from aol_simple import AolSimple
from acoustics import teo2_ac_vel

order = 1
op_wavelength = 800e-9
base_freq = 40e6
pair_deflection_ratio = 0.8
crystal_thickness = 8e-3

focal_length = 10
focus_position = array([-.1,-.2,focal_length])
focus_velocity = [0,1,0]

aod_spacing = array([5e-2] * 3)

aods = [0]*4
aods[0] = Aod(normalise([0,0.2,5]), [ 1, 0,0], 25e-3, 3.2e-3, crystal_thickness)
aods[1] = Aod(normalise([0,-0.2,5]), [ 0, 1,0], 25e-3, 3.2e-3, crystal_thickness)
aods[2] = Aod([0,0,1], [-1, 0,0], 25e-3, 1.6e-3, crystal_thickness)
aods[3] = Aod([0,0,1], [ 0,-1,0], 25e-3, 1.6e-3, crystal_thickness)

aol = AolFull.create_aol(aods, aod_spacing, order, op_wavelength, base_freq, pair_deflection_ratio, focus_position, focus_velocity)
aol_simple = AolSimple.create_aol(order, op_wavelength, teo2_ac_vel, aod_spacing, base_freq, pair_deflection_ratio, focus_position, focus_velocity, crystal_thickness)
# check that the drives generated for the als above are the same
# use base ray position on simple to offset focus_theory

def test_plot():
    x,y = meshgrid(linspace(-1,1,10)*1e-2, linspace(-1,1,10)*1e-2)
    list_of_positions = zip(x.ravel(), y.ravel()) 
    rays = [Ray([xy[0], xy[1], 0], [0,0,1], 800e-9) for xy in list_of_positions]
    aol.plot_ray_through_aol(rays, 0, focus_position[2]+0.01)

def test_angles_on_aods():
    x,y = meshgrid(linspace(-1,1,10)*1e-2, linspace(-1,1,10)*1e-2)
    list_of_positions = zip(x.ravel(), y.ravel()) 
    rays = [Ray([xy[0], xy[1], 0], [0,0,1], 800e-9) for xy in list_of_positions]
    paths,_ = aol.propagate_to_distance_past_aol(rays, 3e-6)
    for m in range(8):
        dot_prods = dot(paths[:,m,:], aol.aods[m/2].normal)
        assert allclose(dot_prods, dot_prods[0])
    assert allclose([p[2] for p in paths[:,8,:]], aod_spacing.sum())

def test_ray_passes_through_focus():
    location = [0]*100
    for t in arange(100):
        ray = Ray([r()*5e-2,r()*5e-2,0], [0,0,1], 800e-9)
        aol.propagate_to_distance_past_aol([ray], 0, focal_length)
        location[t] = ray.position
    
    
    focus_theory = aol_simple.propagate_to_distance_past_aol(ray, time, distance)
    assert allclose(location, focus_theory, rtol=0, atol=1e-3) and allclose(location, location[0], rtol=1e-3, atol=0)
test_ray_passes_through_focus()
def test_ray_scans_correctly():
    location = [0]*100
    for t in arange(100):
        ray = Ray([r()*5e-2,r()*5e-2,0], [0,0,1], 800e-9)
        aol.propagate_to_distance_past_aol([ray], t*1e-6, focal_length)
        location[t] = ray.position
    
    focus_theory = focus_position + [0,0,aod_spacing.sum()] + [5e-3, 5e-3, 0] + outer(arange(100)*1e-6, focus_velocity)
    assert allclose(location, focus_theory, rtol=1e-2, atol=0)

def test_efficiency_low_at_angle():
    ray = Ray([0,0,0], [3./5,0,4./5], 800e-9)
    aol.propagate_to_distance_past_aol([ray], 0, focal_length)
    assert ray.energy < 1e-9