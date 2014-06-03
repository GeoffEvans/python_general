from convert_cartesian_spherical import normalise
from numpy import dot, sin, sqrt
from numpy.linalg import norm
from scipy.optimize import fsolve
from scipy.constants import c, pi
from copy import copy

def diffract_acousto_optically(aod, ray, local_acoustics):
    (wavevector_mismatch_mag, original_ray) = diffract_by_wavevector_triangle(aod, ray)
    ray.energy *= get_aod_efficiency(aod, ray, wavevector_mismatch_mag, original_ray, ray, local_acoustics)

def diffract_by_wavevector_triangle(aod, ray, local_acoustics):
    n_ext = aod.calc_refractive_indices_ray(ray)[0]
    
    wavevector_in = n_ext * ray.wavevector_vac
    wavevector_ac = local_acoustics.wavevector_vac(aod.sound_direction)
    resultant = wavevector_in + aod.order * wavevector_ac 
    
    wavevector_vac_mag_out = ray.wavevector_vac + (2 * pi / c) * local_acoustics.frequency # from w_out = w_in + w_ac
    
    def zero_func(mismatch):
        wavevector_mismatch = mismatch * aod.normal
        wavevector_out = resultant + wavevector_mismatch
        wavevector_out_mag1 = norm(wavevector_out, axis=0)
          
        n_ord = aod.calc_refractive_indices_vector(wavevector_out)[1]
        wavevector_out_mag2 = n_ord * wavevector_vac_mag_out
        
        return wavevector_out_mag1 - wavevector_out_mag2 

    (wavevector_mismatch_mag, _) = fsolve(zero_func, 0)
    
    wavevector_mismatch = wavevector_mismatch_mag * aod.normal
    wavevector_out = resultant + wavevector_mismatch
    
    original_ray = copy(ray)
    ray.wavevector_vac_mag = wavevector_vac_mag_out
    ray.wavevector_vac_unit = normalise(wavevector_out)
    return  (wavevector_mismatch_mag, original_ray) # return phase mismatch

def get_aod_efficiency(aod, wavevector_mismatch_mag, ray_in, ray_out, local_acoustics):
    
    (n_in, _) = aod.calc_refractive_indices_ray(ray_in) # extraordinary in
    (_, n_out) = aod.calc_refractive_indices_ray(ray_out) 
    p = -0.12  # for P66' (see appendix p583)
    
    delta_n0 = -0.5 * n_in**2 * n_out * p * local_acoustics.amplitude  # Xu&St (2.128)
    delta_n1 = -0.5 * n_out**2 * n_in * p * local_acoustics.amplitude
    v0 = - ray_out.wavevector_vac_mag * delta_n0 * aod.transducer_width / dot(aod.normal, ray_out.wavevector_unit) # TODO, check approximation made here
    v1 = - ray_in.wavevector_vac_mag  * delta_n1 * aod.transducer_width / dot(aod.normal, ray_in.wavevector_unit) 
    
    zeta = -0.5 * wavevector_mismatch_mag * aod.transducer_width 
    sigma = sqrt(zeta**2 + v0*v1/4) # Xu&St (2.132)
    
    return (v0 / 2)**2 * (sin(sigma) / sigma)**2 # Xu&St (2.134)