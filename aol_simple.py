from numpy import array
from acoustics import Acoustics

class Aol(object):

    def __init__(self, order, aod_spacing, freq_const, freq_linear, aod_directions):
        self.order = order
        self.aod_spacing = array(aod_spacing)
        self.freq_const = freq_const
        self.freq_linear = freq_linear
        self.aod_directions = aod_directions
        self.normal_to_plane = array([0, 0, 1])
            
    def propagate_to_distance_from_aol(self, ray, distance):
        self.propagate_through_aol(ray)
        point_on_plane = [0, 0, self.aod_spacing.sum() + distance]
        ray.propagate_to_plane(point_on_plane, self.normal_to_plane)
        
    def propagate_through_aol(self, ray, time):
        self.deflect_at_aod(self, ray, time, 1)
        ray.propagate_to_plane([0, 0, self.aod_spacing[0:1].sum()], self.normal_to_plane)
        self.deflect_at_aod(self, ray, time, 2)
        ray.propagate_to_plane([0, 0, self.aod_spacing[1:2].sum()], self.normal_to_plane)
        self.deflect_at_aod(self, ray, time, 3)
        ray.propagate_to_plane([0, 0, self.aod_spacing[2:3].sum()], self.normal_to_plane)
        self.deflect_at_aod(self, ray, time, 4)
        
    def deflect_at_aod(self, ray, time, aod_number):
        frequency = self.freq_const + self.freq_linear * time
        acoustics = Acoustics(frequency)
        
        wavevector_shift = self.order * ray.wavelength_vac / acoustics.velocity * acoustics.frequency * self.aod_directions[aod_number-1] 
        ray.wavevector_vac += wavevector_shift 