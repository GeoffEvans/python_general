from teo2 import calc_refractive_indices
from xu_stroud_model import diffract_acousto_optically
from vector_utils import perpendicular_component_list, normalise_list, normalise
from error_utils import check_is_unit_vector
from numpy import array, sqrt, arccos, arcsin, sin, cos, cross, dot, dtype, allclose, outer
from numpy.linalg import norm
from scipy.optimize import fsolve

class Aod(object):
       
    def __init__(self, normal, relative_ac_dir, aperture_width, transducer_width, crystal_thickness):
        self.normal = array(normal, dtype=dtype(float))
        self.relative_acoustic_direction = array(relative_ac_dir, dtype=dtype(float))
        self.aperture_width = aperture_width
        self.crystal_thickness = crystal_thickness
        self.transducer_width = transducer_width    
        
        check_is_unit_vector(normal)
        check_is_unit_vector(relative_ac_dir)

    @property
    def optic_axis(self):
        return self.normal
    @property
    def acoustic_direction(self):
        # three basis vectors
        z = array([0.,0.,1.])
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

    def propagate_ray(self, rays, local_acoustics, order):
        self.refract_in(rays)
        diffract_acousto_optically(self, rays, local_acoustics, order)
        self.move_ray_through_aod(rays)
        self.refract_out(rays)
        
    def move_ray_through_aod(self, rays):
        directions = self.get_ray_direction_ord(rays)
        distances = self.crystal_thickness / dot(directions, self.normal)
        for m in range(len(rays)):
            rays[m].position += distances[m] * directions[m]

    def get_ray_direction_ord(self, rays):      
        
        def n_ord_vectors(unit_dirs):
            angles = arccos(dot(unit_dirs, self.optic_axis))
            return (unit_dirs.T * calc_refractive_indices(angles)[1]).T
            
        w0 = array([r.wavevector_unit.copy() for r in rays])
        w1 = array([r.wavevector_unit.copy() for r in rays])
        w1[:,0] += 1e-9
        w1 = normalise_list(w1)
        w2 = array([r.wavevector_unit.copy() for r in rays])
        w2[:,1] += 1e-9
        w2 = normalise_list(w2)
        
        d1 = n_ord_vectors(w1) - n_ord_vectors(w0)
        d2 = n_ord_vectors(w2) - n_ord_vectors(w0)
        
        return normalise_list(cross(d1,d2))
    
    def calc_refractive_indices_vectors(self, vectors):
        angles_to_axis = arccos(dot(normalise_list(vectors), self.optic_axis))
        return calc_refractive_indices(angles_to_axis)

    def calc_refractive_indices_rays(self, rays):
        wavevecs = [r.wavevector_unit for r in rays]
        angles_to_axis = arccos(dot(wavevecs, self.optic_axis))
        return calc_refractive_indices(angles_to_axis)
        
    def refract_in(self, rays):
        # get vectors perpendicular and parallel to normal
        wavevecs = [r.wavevector_unit for r in rays]
        perpendicular_comps = perpendicular_component_list(wavevecs, self.normal) 
        
        unit_perpendiculars = normalise_list(perpendicular_comps)
        
        sin_angles_in = sqrt(1 - dot(wavevecs, self.optic_axis) ** 2)
        angle_guesses = arcsin(sin_angles_in / 2.26)  
              
        def zero_func(angles_out):
            wavevector_unit = outer(cos(angles_out), self.normal) + (sin(angles_out) * unit_perpendiculars.T).T
            n_ext = self.calc_refractive_indices_vectors(wavevector_unit)[0]
            return (n_ext * sin(angles_out)) - sin_angles_in 
        
        angles = fsolve(zero_func, angle_guesses, band=(0,0))
        
        for m in range(len(rays)):        
            rays[m].wavevector_unit = cos(angles[m]) * self.normal + sin(angles[m]) * unit_perpendiculars[m]
         
    def refract_out(self, rays):
        wavevecs = array([r.wavevector_unit for r in rays])
        n_ords = self.calc_refractive_indices_rays(rays)[1]
        perpendicular_comps = perpendicular_component_list((n_ords * wavevecs.T).T, self.normal)
        parallel_components = outer(sqrt( 1 - norm(perpendicular_comps, axis=1)**2 ), self.normal)
        for m in range(len(rays)):        
            rays[m].wavevector_unit = parallel_components[m] + perpendicular_comps[m] 
            