from numpy import pi, array, dot

class Ray:
    position = [0,0,0]
    wavevector_unit = [0,0,0]
    energy = 0
    wavelength_vac = 0
    
    @property
    def wavevector(self):
        return self.wavevector_mag * self.wavevector_unit
    @property
    def wavevector_mag(self):
        return 2*pi/self.wavelength_vac
        
    def __init__(self, position, wavevector_unit, wavelength, energy):
        self.position = array(position)
        self.wavevector_unit = array(wavevector_unit)
        self.wavelength_vac = wavelength
        self.energy = energy
    
    def propagate_free_space(self, distance):
        self.position += self.wavevector_unit * distance
        
    def propagate_to_plane(self, point_on_plane, normal_to_plane):
        from_ray_to_point = point_on_plane - self.position
        distance = dot(from_ray_to_point, normal_to_plane) / dot(self.wavevector_unit, normal_to_plane)
        self.propagate_free_space(distance)