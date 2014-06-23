from aol_full import AolFull
from aod import Aod
from ray import Ray
from numpy import array, arange, append, sqrt, dtype, zeros, isnan
from numpy.linalg import norm
import copy
from scipy import optimize
from vector_utils import normalise, normalise_list

op_wavelength = 800e-9

def optimise_aol():
    aol = set_up_aol()
     
    for aod_num in arange(1, 5):
        optimise_nth_aod(aod_num, aol)
        
    return array([a.normal for a in aol.aods], dtype=dtype(float))
    

def optimise_nth_aod(aod_num, aol):
    
    def min_fun(xy_normal):
        new_normal = append(xy_normal, sqrt(1 - norm(xy_normal)**2))
        change_orientation(aol, aod_num, new_normal)
        return - calculate_efficiency(aol, aod_num)

    acoustics = aol.acoustic_drives[aod_num-1]
    this_aod = aol.aods[aod_num-1]
    
    bragg_angle = op_wavelength * acoustics.const / acoustics.velocity
    guess = normalise(this_aod.normal + this_aod.acoustic_direction * bragg_angle * aol.order / 2.26)   
    
    result = optimize.minimize(min_fun, guess[0:2], method='L-BFGS-B', bounds=[(-0.5,0.5), (-0.5,0.5)])
    xy_normal = result.x
    new_optimal_normal = append(xy_normal, sqrt(1 - norm(xy_normal)**2))
    change_orientation(aol, aod_num, new_optimal_normal)

def set_up_aol():
    order = 1
    base_freq = 40e6
    pair_deflection_ratio = 0.8
    
    focal_length = 100
    focus_position = array([.1,.2,focal_length])
    focus_velocity = [0,1,0]
    
    aod_spacing = array([5e-2] * 3)
    
    orientations = normalise_list(array([ [  4.03663526e-02,   7.19263615e-08,   9.99184947e-01], \
                          [ 7.19263615e-08,  4.03663526e-02,  9.99184947e-01], \
                          [ 4.03663526e-02,   7.19263615e-08,   9.99184947e-01], \
                          [ 7.19263615e-08,  4.03663526e-02,  9.99184947e-01] ]))
    
    orientation = normalise_list([[  1.05807270e-01,   3.75889637e-07,   9.94386656e-01] ,\
                            [ -3.38090520e-04,   5.72771621e-02,   9.98358259e-01] ,\
                            [ -4.89868339e-02,  -9.71658841e-04,   9.98798952e-01] ,\
                            [  5.27145634e-06,  -4.66860201e-02,   9.98909613e-01]])
    
    aods = [0]*4
    aods[0] = Aod(orientations[0], [ 1, 0,0], 25e-3, 3.2e-3, 8e-3)
    aods[1] = Aod(orientations[1], [ 0, 1,0], 25e-3, 3.2e-3, 8e-3)
    aods[2] = Aod(orientations[2], [-1, 0,0], 25e-3, 1.6e-3, 8e-3)
    aods[3] = Aod(orientations[3], [ 0,-1,0], 25e-3, 1.6e-3, 8e-3)
    
    return AolFull.create_aol(aods, aod_spacing, order, op_wavelength, base_freq, pair_deflection_ratio, focus_position, focus_velocity)

def change_orientation(aol, aod_num, new_normal):
    assert not any(isnan(new_normal))
    aol.aods[aod_num-1].normal = new_normal

def calculate_efficiency(aol, after_nth_aod):
    time_array = (arange(3)-1)*5e-5
    x_array = (arange(3)-1)*2e-3
    y_array = x_array
    
    energy = 0
    ray_count = 0
    
    rays = [0] * len(x_array) * len(y_array)
    for t in time_array:
        for xn in range(len(x_array)):
            for yn in range(len(y_array)):    
                rays[xn + yn*len(x_array)] = Ray([x_array[xn],y_array[yn],0], [0,0,1], op_wavelength)
        
        (_,energies) = aol.propagate_to_distance_past_aol(rays, t)
        energy += sum(energies[:,after_nth_aod-1])
        ray_count += len(rays)
                
    return energy / ray_count

if __name__ == '__main__':
    #calculate_efficiency(set_up_aol(), 4)
    optimise_aol()