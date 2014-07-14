from vector_utils import normalise_list
from numpy import dot, sin, sqrt, array, zeros, outer, allclose, power
from numpy.linalg import norm
from scipy.optimize import fsolve
from scipy.constants import c, pi

def diffract_acousto_optically(aod, rays, local_acoustics, order, ext_to_ord=True, rescattering=True):
    if not abs(order) == 1:
        raise ValueError("Order only supports +1, -1")
    
    ref_inds = (1,0) # ord->ext
    if ext_to_ord:
        ref_inds = (0,1) # ext->ord

    wavevecs_in_mag  = [r.wavevector_vac_mag for r in rays] # store these
    wavevecs_in_unit  = array([r.wavevector_unit for r in rays])
    
    (efficiencies, wavevecs_out_unit, wavevecs_out_mag) = \
        get_diffracted_wavevectors_and_efficiency(aod, wavevecs_in_unit, wavevecs_in_mag, local_acoustics, order, ref_inds)
    
    if rescattering:
        rev_ref_inds = ref_inds[::-1]
        same_ref_inds = [ref_inds[1]]*2
        (efficiencies_r1,_,_) = get_diffracted_wavevectors_and_efficiency(aod, wavevecs_out_unit, wavevecs_out_mag, local_acoustics, order, rev_ref_inds)
        (efficiencies_r2,_,_) = get_diffracted_wavevectors_and_efficiency(aod, wavevecs_out_unit, wavevecs_out_mag, local_acoustics, order, same_ref_inds)
        efficiencies *= (1 - efficiencies_r1 - efficiencies_r2)
        
    for m in range(len(rays)):
        rays[m].wavevector_vac_mag = wavevecs_out_mag[m]
        rays[m].wavevector_unit = wavevecs_out_unit[m]
        rays[m].energy *= efficiencies[m]

def get_diffracted_wavevectors_and_efficiency(aod, wavevecs_in_unit, wavevecs_in_mag, local_acoustics, order, ref_inds):
    (wavevector_mismatches_mag, wavevecs_out_unit, wavevecs_out_mag) = diffract_by_wavevector_triangle(aod, wavevecs_in_unit, wavevecs_in_mag, local_acoustics, order, ref_inds)
    efficiencies = get_efficiency(aod, wavevector_mismatches_mag, wavevecs_in_mag, wavevecs_in_unit, wavevecs_out_mag, wavevecs_out_unit, local_acoustics, ref_inds)
    return (efficiencies, wavevecs_out_unit, wavevecs_out_mag)

def diffract_by_wavevector_triangle(aod, wavevec_unit_in, wavevec_vac_mag_in, local_acoustics, order, ref_inds):
    wavevectors_vac_mag_out = wavevec_vac_mag_in + (2 * pi / c) * array([a.frequency for a in local_acoustics]) # from w_out = w_in + w_ac
    resultants = get_resultant_wavevectors(aod, wavevec_unit_in, wavevec_vac_mag_in, local_acoustics, order, ref_inds)

    def zero_func(mismatches):
        wavevector_mismatches = outer(mismatches * 1e6, aod.normal)
        wavevectors_out = resultants + wavevector_mismatches
        wavevectors_out_mag1 = norm(wavevectors_out, axis=1)
          
        n_out = aod.calc_refractive_indices_vectors(wavevectors_out)[ref_inds[1]]
        wavevectors_out_mag2 = n_out * wavevectors_vac_mag_out # n_out pretty much constant
        
        return wavevectors_out_mag2 - wavevectors_out_mag1 
    
    initial_guess = zeros(len(wavevec_vac_mag_in))
    wavevector_mismatches_mag = fsolve(zero_func, initial_guess, band=(0,0)) * 1e6
    
    wavevector_mismatches = outer(wavevector_mismatches_mag, aod.normal)
    wavevectors_out = resultants + wavevector_mismatches
    
    check_matching(aod, wavevectors_out, wavevectors_vac_mag_out, ref_inds)

    wavevectors_out_unit = normalise_list(wavevectors_out)
    return (wavevector_mismatches_mag, wavevectors_out_unit, wavevectors_vac_mag_out)

def get_resultant_wavevectors(aod, wavevec_unit_in, wavevec_vac_mag_in, local_acoustics, order, ref_inds):
    n_in = aod.calc_refractive_indices_vectors(wavevec_unit_in)[ref_inds[0]]
    wavevectors_in = (n_in * wavevec_vac_mag_in * wavevec_unit_in.T).T
    wavevectors_ac = outer(array([a.wavevector_mag for a in local_acoustics]), aod.acoustic_direction)
    return wavevectors_in + order * wavevectors_ac 

def check_matching(aod, wavevectors_out, wavevectors_vac_mag_out, ref_inds):
    n_out = aod.calc_refractive_indices_vectors(wavevectors_out)[ref_inds[1]]
    wavevectors_out_mag2 = n_out * wavevectors_vac_mag_out
    wavevectors_out_mag1 = norm(wavevectors_out, axis=1)
    assert allclose(wavevectors_out_mag1, wavevectors_out_mag2)

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
