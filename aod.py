from teo2 import calc_refractive_indices
from convert_cartesian_spherical import normalise, perpendicular_component
from numpy import array, dot, arccos, arcsin, sin, cos, sqrt
from numpy.linalg import norm

class Aod:
    normal = [0,0,0]
    sound_direction = [0,0,0] # assuming normal is [0,0,1]
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

    def propagate_ray(self, ray, local_acoustics):
        self.refract_in(ray)
        point_on_exit_plane = ray.position + self.normal * self.crystal_width
        self.diffract_acousto_optically(ray)
        ray.propagate_to_plane(point_on_exit_plane, self.normal)
        self.refract_out(ray)

    def calc_refractive_indices_ray(self, ray):
        get_angle_to_axis = arccos(dot(ray.wavevector_unit, self.optic_axis))
        return calc_refractive_indices(get_angle_to_axis)
        
    def refract_in(self, ray):
        sin_angle_in = sqrt(1 - dot(ray.wavevector_unit, self.optic_axis) ** 2)
        angle_guess = arcsin(sin_angle_in / 2.26)  
        
        ang = 2
        # find angle that gives sin_angle_in = n_ext * sin(angle_out)
        # n_ext = self.calc_refractive_indices_ray(ray)[0]
                
        perpendicular_comp = perpendicular_component(ray.wavevector_unit, self.normal)
        unit_perpendicular = normalise(perpendicular_comp)
        ray.wavevector_unit = cos(ang) * self.normal + sin(ang) * unit_perpendicular 
         
    def refract_out(self, ray):
        n_ord = self.calc_refractive_indices_ray(ray)[1]
        perpendicular_comp = n_ord * perpendicular_component(ray.wavevector_unit, self.normal)
        parallel_component = self.normal * ( 1 - norm(perpendicular_comp, axis=0) )
        ray.wavevector_unit = parallel_component + perpendicular_comp
        # test this returns unit vectors
    
    def diffract_acousto_optically(self, ray, local_acoustics):
        phase_mismatch = self.match_phase(ray)
        ray.energy *= self.get_aod_efficiency(ray, phase_mismatch, local_acoustics)

    def match_phase(self, ray, local_acoustics):
        n_ext = self.calc_refractive_indices_ray(ray)[0]
        wavevector_in = n_ext * ray.wavevector
        wavevector_ac = local_acoustics.wavevector(self.sound_direction)
        resultant = wavevector_in + self.order * wavevector_ac 
        
        # find angle that gives resultant - wavevector_out || normal 
        # wavevector_out magnitude dictated by refractive index
        
        # set new direction on ray
        return 2 # return phase mismatch

    def get_aod_efficiency(self, ray, phase_mismatch, local_acoustics):
        (n_ext, n_ord) = self.calc_refractive_indices_ray(ray) 
        p = -0.12  # for P66' (see appendix p583)
        
        delta_n0 = -0.5 * n_ord**2 * n_ext * p * local_acoustics.amplitude  # Xu&St (2.128)
        delta_n1 = -0.5 * n_ord * n_ext**2 * p * local_acoustics.amplitude
        v0 = - ray.wavevector * delta_n0 * self.transducer_width / dot(self.optic_axis, ray.wavevector_unit) # TODO, check approximation made here
        v1 = - ray.wavevector * delta_n1 * self.transducer_width / dot(self.optic_axis, ray.wavevector_unit) 
        
        zeta = -0.5 * phase_mismatch * self.transducer_width 
        sigma = sqrt(zeta**2 + v0*v1/4) # Xu&St (2.132)
        
        return (v0 / 2)**2 * (sin(sigma) / sigma)**2 # Xu&St (2.134)
    
    def get_ray_direction(self, ray):
        return ray.wavevector_unit # TODO 