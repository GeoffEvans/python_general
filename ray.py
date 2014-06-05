from numpy import pi, array, dot, dtype
from testutils import check_is_unit_vector

class Ray(object):
        
    def __init__(self, position, wavevector_unit, wavelength, energy=1):
        self.position = array(position, dtype=dtype(float))
        self.wavevector_unit = array(wavevector_unit, dtype=dtype(float))
        self.wavelength_vac = wavelength
        self.energy = energy

    @property
    def wavevector_vac(self):
        return self.wavevector_vac_mag * self.wavevector_unit

    @property
    def wavevector_unit(self):
        return self._wavevector_unit
    @wavevector_unit.setter
    def wavevector_unit(self, v):
        check_is_unit_vector(v)
        self._wavevector_unit = array(v, dtype=dtype(float))
        
    @property
    def wavevector_vac_mag(self):
        return 2 * pi / self.wavelength_vac
    @wavevector_vac_mag.setter
    def wavevector_vac_mag(self, v):
        self.wavelength_vac = 2 * pi / v
    
    def propagate_free_space(self, distance):
        self.position += self.wavevector_unit * distance
        
    def propagate_to_plane(self, point_on_plane, normal_to_plane):
        from_ray_to_point = point_on_plane - self.position
        distance = dot(from_ray_to_point, normal_to_plane) / dot(self.wavevector_unit, normal_to_plane)
        self.propagate_free_space(distance)
