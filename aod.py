from teo2 import calc_refractive_indices
from xu_stroud_model import diffract_acousto_optically
from vector_utils import perpendicular_component, normalise
from error_utils import check_is_unit_vector
from numpy import array, sqrt, arccos, arcsin, sin, cos, cross, dot, dtype
from numpy.linalg import norm
from scipy.optimize import newton

class Aod(object):
       
    def __init__(self, normal, sound_direction, aperture_width, transducer_width, crystal_thickness, centre=[0,0,0]):
        self.normal = array(normal, dtype=dtype(float))
        self.relative_acoustic_direction = array(sound_direction, dtype=dtype(float))
        self.aperture_width = aperture_width
        self.crystal_thickness = crystal_thickness
        self.transducer_width = transducer_width    
        self.centre = array(centre, dtype=dtype(float))
        
        check_is_unit_vector(normal)
        check_is_unit_vector(sound_direction)

    @property
    def optic_axis(self):
        return self.normal
    @property
    def acoustic_direction(self):
        # three basis vectors
        z = array([0,0,1.])
        invariant = normalise( cross(self.relative_acoustic_direction, z) )
        t = cross(z,invariant)
        
        # how z transforms
        cosine = dot(z, self.normal) 
        sine = dot(t, self.normal)
        
        # components: s = s1 inv + s2 z + s3 t
        s1 = dot(invariant,self.relative_acoustic_direction)
        s2 = dot(z,self.relative_acoustic_direction)
        s3 = dot(t,self.relative_acoustic_direction)
        
        sound_vector = s1 * invariant + (cosine * s2 - sine * s3) * z + (cosine * s3 + sine * s2) * t
        
        return sound_vector 

    def propagate_ray(self, ray, local_acoustics, order):
        self.refract_in(ray)
        diffract_acousto_optically(self, ray, local_acoustics, order)
        self.move_ray_through_aod(ray)
        self.refract_out(ray)
        
    def move_ray_through_aod(self, ray):
        direction = self.get_ray_direction_ord(ray)
        distance = self.crystal_thickness / dot(direction, self.normal)
        ray.position += distance * direction

    def get_ray_direction_ord(self, ray):      
        
        def n_ord_vector(unit_dir):
            ang = arccos(dot(unit_dir, self.optic_axis))
            return unit_dir * calc_refractive_indices(ang)[1]
            
        w0 = ray.wavevector_unit.copy()
        w1 = ray.wavevector_unit.copy()
        w1[0] += 1e-9
        w1 = normalise(w1)
        w2 = ray.wavevector_unit.copy()
        w2[1] += 1e-9
        w2 = normalise(w2)
        
        d1 = n_ord_vector(w1) - n_ord_vector(w0)
        d2 = n_ord_vector(w2) - n_ord_vector(w0)
        
        return normalise(cross(d1,d2))
    
    def calc_refractive_indices_vector(self, vector):
        get_angle_to_axis = arccos(dot(normalise(vector), self.optic_axis))
        return calc_refractive_indices(get_angle_to_axis)

    def calc_refractive_indices_ray(self, ray):
        angle_to_axis = arccos(dot(ray.wavevector_unit, self.optic_axis))
        return calc_refractive_indices(angle_to_axis)
        
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
        
        ang = newton(zero_func, angle_guess)
                
        ray.wavevector_unit = cos(ang) * self.normal + sin(ang) * unit_perpendicular 
         
    def refract_out(self, ray):
        n_ord = self.calc_refractive_indices_ray(ray)[1]
        perpendicular_comp = perpendicular_component(n_ord * ray.wavevector_unit, self.normal)
        parallel_component = self.normal * sqrt( 1 - norm(perpendicular_comp, axis=0)**2 )
        ray.wavevector_unit = parallel_component + perpendicular_comp 