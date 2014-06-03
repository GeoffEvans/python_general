from teo2 import calc_refractive_indices
from convert_cartesian_spherical import normalise, perpendicular_component
from numpy import array, dot, arccos, arcsin, sin, cos, sqrt, cross
from numpy.linalg import norm
from scipy.optimize import fsolve
from scipy.constants import c, pi
from copy import copy
from testutils import check_is_unit_vector

class Aod:
    normal = [0,0,0]
    sound_direction = [0,0,0] # in the frame where the normal is [0,0,1]
    aperture_width = 0 
    transducer_width = 0
    crystal_width = 0
    order = 1
    
    @property
    def optic_axis(self):
        return self.normal
    
    def __init__(self, normal, sound_direction, aperture_width, transducer_width, crystal_width, order):
        self.normal = array(normal)
        self.sound_direction = array(sound_direction)
        self.aperture_width = aperture_width
        self.crystal_width = crystal_width
        self.transducer_width = transducer_width    
        self.order= order
        
        if order > 1:
            raise ValueError("Order only supports +1, -1 and 0")
        check_is_unit_vector(normal)
        check_is_unit_vector(sound_direction)

    def propagate_ray(self, ray, local_acoustics):
        self.refract_in(ray)
        self.diffract_acousto_optically(ray)
        self.update_ray_location(ray)
        self.refract_out(ray)
        
        def update_ray_location(self, ray):
            direction = self.get_ray_direction_ord(ray)
            distance = self.crystal_width / dot(direction, self.normal)
            ray.position += distance * direction

    def get_ray_direction_ord(self, ray):      
        
        def n_ord_vector(unit_dir):
            ang = arccos(dot(unit_dir, self.optic_axis))
            return unit_dir * calc_refractive_indices(ang)[1]
            
        w0 = ray.wavevector_unit
        w1 = ray.wavevector_unit
        w1[0,:] += 1e-9
        w2 = ray.wavevector_unit
        w2[1,:] += 1e-9
        
        d1 = n_ord_vector(w1) - n_ord_vector(w0)
        d2 = n_ord_vector(w2) - n_ord_vector(w0)
        
        return normalise(cross(d1,d2))

    def calc_refractive_indices_vector(self, vector):
        get_angle_to_axis = arccos(dot(normalise(vector), self.optic_axis))
        return calc_refractive_indices(get_angle_to_axis)

    def calc_refractive_indices_ray(self, ray):
        get_angle_to_axis = arccos(dot(ray.wavevector_unit, self.optic_axis))
        return calc_refractive_indices(get_angle_to_axis)
        
    def refract_in(self, ray):
        # get vectors perpendicular and parallel to normal
        perpendicular_comp = perpendicular_component(ray.wavevector_unit, self.normal) 
        unit_perpendicular = normalise(perpendicular_comp)
        
        sin_angle_in = sqrt(1 - dot(ray.wavevector_unit, self.optic_axis) ** 2)
        angle_guess = arcsin(sin_angle_in / 2.26)  
              
        def zero_func(angle_out):
            wavevector_unit = cos(angle_out) * self.normal + sin(angle_out) * unit_perpendicular
            n_ext = self.calc_refractive_indices_vector(wavevector_unit)[0]
            return (n_ext * sin(angle_out)) - sin_angle_in 
        
        (ang, _) = fsolve(zero_func, angle_guess)
                
        ray.wavevector_unit = cos(ang) * self.normal + sin(ang) * unit_perpendicular 
         
    def refract_out(self, ray):
        n_ord = self.calc_refractive_indices_ray(ray)[1]
        perpendicular_comp = n_ord * perpendicular_component(ray.wavevector_unit, self.normal)
        parallel_component = self.normal * ( 1 - norm(perpendicular_comp, axis=0) )
        ray.wavevector_unit = parallel_component + perpendicular_comp
        # test this returns unit vectors
    
    def diffract_acousto_optically(self, ray, local_acoustics):
        (wavevector_mismatch_mag, original_ray) = self.diffract_by_wavevector_triangle(ray)
        ray.energy *= self.get_aod_efficiency(ray, wavevector_mismatch_mag, original_ray, ray, local_acoustics)

    def diffract_by_wavevector_triangle(self, ray, local_acoustics):
        n_ext = self.calc_refractive_indices_ray(ray)[0]
        
        wavevector_in = n_ext * ray.wavevector_vac
        wavevector_ac = local_acoustics.wavevector_vac(self.sound_direction)
        resultant = wavevector_in + self.order * wavevector_ac 
        
        wavevector_vac_mag_out = ray.wavevector_vac + (2 * pi / c) * local_acoustics.frequency # from w_out = w_in + w_ac
        
        def zero_func(mismatch):
            wavevector_mismatch = mismatch * self.normal
            wavevector_out = resultant + wavevector_mismatch
            wavevector_out_mag1 = norm(wavevector_out, axis=0)
              
            n_ord = self.calc_refractive_indices_vector(wavevector_out)[1]
            wavevector_out_mag2 = n_ord * wavevector_vac_mag_out
            
            return wavevector_out_mag1 - wavevector_out_mag2 

        (wavevector_mismatch_mag, _) = fsolve(zero_func, 0)
        
        wavevector_mismatch = wavevector_mismatch_mag * self.normal
        wavevector_out = resultant + wavevector_mismatch
        
        original_ray = copy(ray)
        ray.wavevector_vac_mag = wavevector_vac_mag_out
        ray.wavevector_vac_unit = normalise(wavevector_out)
        return  (wavevector_mismatch_mag, original_ray)# return phase mismatch

    def get_aod_efficiency(self, wavevector_mismatch_mag, ray_in, ray_out, local_acoustics):
        
        (n_in, _) = self.calc_refractive_indices_ray(ray_in) # extraordinary in
        (_, n_out) = self.calc_refractive_indices_ray(ray_out) 
        p = -0.12  # for P66' (see appendix p583)
        
        delta_n0 = -0.5 * n_in**2 * n_out * p * local_acoustics.amplitude  # Xu&St (2.128)
        delta_n1 = -0.5 * n_out**2 * n_in * p * local_acoustics.amplitude
        v0 = - ray_out.wavevector_vac_mag * delta_n0 * self.transducer_width / dot(self.normal, ray_out.wavevector_unit) # TODO, check approximation made here
        v1 = - ray_in.wavevector_vac_mag  * delta_n1 * self.transducer_width / dot(self.normal, ray_in.wavevector_unit) 
        
        zeta = -0.5 * wavevector_mismatch_mag * self.transducer_width 
        sigma = sqrt(zeta**2 + v0*v1/4) # Xu&St (2.132)
        
        return (v0 / 2)**2 * (sin(sigma) / sigma)**2 # Xu&St (2.134)
    