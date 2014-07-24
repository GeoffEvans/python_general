from numpy.linalg import norm
from numpy import dot, outer, zeros, abs, all, power, sum
from scipy.optimize import fsolve
from vector_utils import normalise_list

def original(sum_vector, base_length, normal, multiplier_func):
    
    def zero_func(mismatches):
        wavevector_mismatches = outer(mismatches * 1e6, normal)
        wavevectors_out = sum_vector + wavevector_mismatches
        wavevectors_out_mag1 = norm(wavevectors_out, axis=1)
          
        n_out = multiplier_func(wavevectors_out)
        wavevectors_out_mag2 = n_out * base_length # n_out pretty much constant
        
        return wavevectors_out_mag2 - wavevectors_out_mag1 
    
    initial_guess = zeros(len(sum_vector))
    wavevector_mismatches_mag = fsolve(zero_func, initial_guess, band=(0,0)) * 1e6
    
    wavevector_mismatches = outer(wavevector_mismatches_mag, normal)
    wavevectors_out = sum_vector + wavevector_mismatches

    wavevectors_out_unit = normalise_list(wavevectors_out)
    return (wavevector_mismatches_mag, wavevectors_out_unit, base_length)

def method1(sum_vector, base_length, normal, multiplier_func):

    def tail_rec_solve(sv):        
        multiplier = multiplier_func(sv)
        ratio = base_length * multiplier / norm(sv, axis=1)
        if all(abs(ratio - 1) < 1e-14):
            return sv
        new_sum_vector = sv - outer(dot(sv, normal) * (1 - ratio), normal)
        return tail_rec_solve(new_sum_vector)
        
    wavevec_out = tail_rec_solve(sum_vector)
    wavevectors_out_unit = normalise_list(wavevec_out)
    
    wavevector_mismatches_mag = dot(wavevec_out - sum_vector, normal)    
    
    return (wavevector_mismatches_mag, wavevectors_out_unit, base_length)
    
def method2(sum_vector, base_length, normal, multiplier_func): #not working
    
    def tail_rec_solve(sv):
        multiplier = multiplier_func(sv)
        
        ratio = base_length * multiplier / norm(sv, axis=1)
        if all(abs(ratio - 1) < 1e-14):
            return sv
            
        dir = normalise_list(sv)
        new_dir = dir + normal * 1e-12
        new_multiplier = multiplier_func(new_dir)

        k = (multiplier * dir.T * base_length).T
        new_k = (new_multiplier * new_dir.T * base_length).T
        tangent = normalise_list(new_k - k)
        
        shift = (dot(sv, normal) - dot_(sv, tangent) * dot(tangent, normal)) / (1 - power(dot(tangent, normal), 2.))
        new_sum_vector = sv + outer(shift, normal)
        return tail_rec_solve(new_sum_vector)
        
    wavevec_out = tail_rec_solve(sum_vector)
    wavevectors_out_unit = normalise_list(wavevec_out)
    
    wavevector_mismatches_mag = dot(wavevec_out - sum_vector, normal)    
    
    return (wavevector_mismatches_mag, wavevectors_out_unit, base_length)
    
def dot_(a, b):
    return sum(a * b, axis=1)