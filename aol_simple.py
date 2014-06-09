from numpy import array, dtype
from acoustics import Acoustics
from testutils import check_is_unit_vector, check_is_of_length

class Aol(object):

    def __init__(self, order, aod_spacing, freq_const, freq_linear, aod_directions):
        self.order = order
        self.aod_spacing = array(aod_spacing, dtype=dtype(float))
        self.freq_const = array(freq_const, dtype=dtype(float))
        self.freq_linear = array(freq_linear, dtype=dtype(float))
        self.aod_directions = array(aod_directions, dtype=dtype(float))
        self.normal_to_plane = array([0, 0, 1], dtype=dtype(float))
        
        for d in self.aod_directions:
            check_is_unit_vector(d)
        check_is_of_length(3, self.aod_spacing)
        check_is_of_length(4, self.freq_const)
        check_is_of_length(4, self.freq_linear)
        check_is_of_length(4, self.aod_directions)
            
    def propagate_to_distance_from_aol(self, ray, distance):
        self.propagate_through_aol(ray)
        point_on_plane = ray.position + [0, 0, distance]
        ray.propagate_to_plane(point_on_plane, self.normal_to_plane)
        
    def propagate_through_aol(self, ray, time):
        self.deflect_at_aod(ray, time, 1)
        ray.propagate_to_plane(ray.position + [0, 0, self.aod_spacing[0]], self.normal_to_plane)
        self.deflect_at_aod(ray, time, 2)
        ray.propagate_to_plane(ray.position + [0, 0, self.aod_spacing[1]], self.normal_to_plane)
        self.deflect_at_aod(ray, time, 3)
        ray.propagate_to_plane(ray.position + [0, 0, self.aod_spacing[2]], self.normal_to_plane)
        self.deflect_at_aod(ray, time, 4)
        
    def deflect_at_aod(self, ray, time, aod_number):
        frequency = self.freq_const[aod_number-1] + self.freq_linear[aod_number-1] * time
        acoustics = Acoustics(frequency)
        
        wavevector_shift = self.order * (ray.wavelength_vac / acoustics.velocity) * acoustics.frequency * self.aod_directions[aod_number-1] 
        ray.wavevector_vac += wavevector_shift 