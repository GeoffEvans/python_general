from aod import Aod
from ray import Ray
from numpy import sqrt, allclose, cross, dot

aod = Aod([0,0,1], [1,0,0], 1, 1, 1, 1)

def test_on_axis_ray_displacement():
    r = Ray([0,0,0],[0,0,1],800e-9,1)
    aod.move_ray_through_aod(r)
    still_on_axis = allclose(cross(r.position, [0,0,1]), [0,0,0])
    direction_unchanged = allclose(r.wavevector_unit, [0,0,1])
    assert still_on_axis and direction_unchanged
    
def test_off_axis_ray_displacement():
    wavevec = [17./145,0,144./145]
    r = Ray([0,0,0],wavevec,800e-9,1)
    aod.move_ray_through_aod(r)
    off_wavevector = not allclose(cross(r.position, wavevec), [0,0,0])
    direction_unchanged = allclose(r.wavevector_unit, wavevec)
    assert off_wavevector and direction_unchanged

def test_refractive_indices_match():
    wavevec = [3./5,0,4./5]
    r = Ray([0,0,0],wavevec,800e-9,1)
    n1 = aod.calc_refractive_indices_vector(r.wavevector_unit) 
    n2 = aod.calc_refractive_indices_ray(r)
    assert allclose(n1,n2)

def test_refracting_in_towards_normal():
    wavevec = [3./5,0,4./5]
    r = Ray([0,0,0],wavevec,800e-9,1)
    aod.refract_in(r)
    cosine_outside = dot(wavevec, aod.normal) 
    cosine_inside =  dot(r.wavevector_unit, aod.normal)
    towards_normal = abs(cosine_outside) < abs(cosine_inside)
    not_reflected = cosine_outside * cosine_inside >= 0
    assert towards_normal and not_reflected
    
def test_refracting_out_away_from_normal():
    wavevec = [17./145,0,144./145]
    r = Ray([0,0,0],wavevec,800e-9,1)
    aod.refract_out(r)
    cosine_outside =  dot(r.wavevector_unit, aod.normal)
    cosine_inside = dot(wavevec, aod.normal)
    towards_normal = abs(cosine_outside) < abs(cosine_inside)
    not_reflected = cosine_outside * cosine_inside >= 0
    assert towards_normal and not_reflected

def test_refraction_in_out_no_change():
    wavevec = [3./5,0,4./5]
    r = Ray([0,0,0],wavevec,800e-9,1)
    aod.refract_in(r)
    aod.refract_out(r)
    assert allclose(r.wavevector_unit, [3./5,0,4./5], rtol=5e-3)
    
def test_absolute_sound_direction_trivial():
    direc = aod.acoustic_direction
    assert allclose(direc, [1,0,0])
    
def test_absolite_sound_direction():
    aod_new = Aod([1,0,1]/sqrt(2), [1,0,0], 1, 1, 1, 1)
    direc = aod_new.acoustic_direction
    assert allclose(direc, [1,0,-1]/sqrt(2))

    