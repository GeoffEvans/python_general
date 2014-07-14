from vector_utils import normalise_list
from numpy import dot, sin, sqrt, array, zeros, outer, allclose, exp, power
from numpy.linalg import norm
from scipy.optimize import fsolve
from scipy.constants import c, pi

def diffract_acousto_optically(aod, rays, local_acoustics, order, ext_to_ord=True, rescattering=True):
    if order > 1:
        raise ValueError("Order only supports +1, -1 and 0")
    
    ref_inds = (1,0) # ord->ext
    if ext_to_ord:
        ref_inds = (0,1) # ext->ord

    wavevecs_in_mag  = [r.wavevector_vac_mag for r in rays] # store these
    wavevecs_in_unit  = [r.wavevector_unit for r in rays ]
    wavevector_mismatches_mag = diffract_by_wavevector_triangle(aod, rays, local_acoustics, order, ref_inds)

    wavevecs_out_mag = [r.wavevector_vac_mag for r in rays]
    wavevecs_out_unit = [r.wavevector_unit for r in rays]    
    efficiencies = get_efficiency(aod, wavevector_mismatches_mag, wavevecs_in_mag, wavevecs_in_unit, wavevecs_out_mag, wavevecs_out_unit, local_acoustics, ref_inds)
    for m in range(len(rays)):
        rays[m].energy *= efficiencies[m]
        
    if rescattering:
        rev_ref_inds = ref_inds[::-1]
        
        wavevecs_in_mag  = [r.wavevector_vac_mag for r in rays] # store these
        wavevecs_in_unit  = [r.wavevector_unit for r in rays ]
        wavevector_mismatches_mag = diffract_by_wavevector_triangle(aod, rays, local_acoustics, order, rev_ref_inds)
        
        wavevecs_out_mag = [r.wavevector_vac_mag for r in rays]
        wavevecs_out_unit = [r.wavevector_unit for r in rays]    
        efficiencies = get_efficiency(aod, wavevector_mismatches_mag, wavevecs_in_mag, wavevecs_in_unit, wavevecs_out_mag, wavevecs_out_unit, local_acoustics, rev_ref_inds)
        
        for m in range(len(rays)):
            rays[m].energy -= rays[m].energy * efficiencies[m] * 0.6 # experimental fudge factor
            rays[m].wavevector_unit = wavevecs_in_unit[m] # we don't want to change the wavevectors again
            rays[m].wavevector_vac_mag = wavevecs_in_mag[m]

def diffract_by_wavevector_triangle(aod, rays, local_acoustics, order, ref_inds):
    n_in = aod.calc_refractive_indices_rays(rays)[ref_inds[0]]
    
    wavevectors_in = (n_in * array([r.wavevector_vac for r in rays]).T).T
    wavevectors_ac = outer(array([a.wavevector_mag for a in local_acoustics]), aod.acoustic_direction)
    resultants = wavevectors_in + order * wavevectors_ac 
    
    wavevectors_vac_mag_out = [r.wavevector_vac_mag for r in rays] + (2 * pi / c) * array([a.frequency for a in local_acoustics]) # from w_out = w_in + w_ac

    def zero_func(mismatches):
        wavevector_mismatches = outer(mismatches * 1e6, aod.normal)
        wavevectors_out = resultants + wavevector_mismatches
        wavevectors_out_mag1 = norm(wavevectors_out, axis=1)
          
        n_out = aod.calc_refractive_indices_vectors(wavevectors_out)[ref_inds[1]]
        wavevectors_out_mag2 = n_out * wavevectors_vac_mag_out # n_out pretty much constant
        
        return wavevectors_out_mag2 - wavevectors_out_mag1 
    
    initial_guess = zeros(len(rays))
    wavevector_mismatches_mag = fsolve(zero_func, initial_guess, band=(0,0)) * 1e6
    wavevector_mismatches = outer(wavevector_mismatches_mag, aod.normal)
    wavevectors_out = resultants + wavevector_mismatches
    
    n_out = aod.calc_refractive_indices_vectors(wavevectors_out)[ref_inds[1]]
    wavevectors_out_mag2 = n_out * wavevectors_vac_mag_out
    wavevectors_out_mag1 = norm(wavevectors_out, axis=1)
    assert allclose(wavevectors_out_mag1, wavevectors_out_mag2)
    
    wavevectors_out_unit = normalise_list(wavevectors_out)
    
    for m in range(len(rays)):
        rays[m].wavevector_vac_mag = wavevectors_vac_mag_out[m]
        rays[m].wavevector_unit = wavevectors_out_unit[m]
    return wavevector_mismatches_mag

def get_efficiency(aod, wavevector_mismatches_mag, wavevecs_in_mag, wavevecs_in_unit, wavevecs_out_mag, wavevecs_out_unit, acoustics, ref_inds):
    amp = [a.amplitude(aod) for a in acoustics] * aod.transducer_efficiency_func([a.frequency for a in acoustics])
    
    n_in = aod.calc_refractive_indices_vectors(wavevecs_in_unit)[ref_inds[0]]
    n_out = aod.calc_refractive_indices_vectors(wavevecs_out_unit)[ref_inds[1]] 
    p = -0.12  # for P66' (see appendix p583)
    
    delta_n0 = -0.5 * power(n_in, 2.) * n_out * p * amp # Xu&St (2.128)
    delta_n1 = -0.5 * power(n_out, 2.) * n_in * p * amp
    v0 = - array(wavevecs_out_mag) * delta_n0 * aod.transducer_width / dot(wavevecs_out_unit, aod.normal)
    v1 = - array(wavevecs_in_mag)  * delta_n1 * aod.transducer_width / dot(wavevecs_in_unit , aod.normal) 
    
    zeta = -0.5 * wavevector_mismatches_mag * aod.transducer_width 
    sigma = sqrt(power(zeta, 2.) + v0*v1/4) # Xu&St (2.132)
    
    return v0*v1/4 * power((sin(sigma) / sigma), 2.) # Xu&St (2.134)