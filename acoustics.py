from numpy import pi, sqrt, dot, dtype, array
from error_utils import check_is_of_length

teo2_ac_vel = 612.8834
default_power = 1

class Acoustics(object):
    
    def __init__(self, frequency, power=default_power, velocity=teo2_ac_vel):
        self.frequency = frequency
        self.power = power
        self.velocity = velocity

    @property
    def wavevector_mag(self):
        return 2 * pi * self.frequency / self.velocity
    
    def wavevector(self, aod):
        return self.wavevector_mag * aod.acoustic_direction
    
    def amplitude(self, aod):
        teo2_density = 5990;
        numerator = 2 * self.power
        denominator = teo2_density * self.velocity**3 * aod.transducer_width * aod.aperture_width # assumes sqr aperture 
        return sqrt(numerator / denominator)
    
class AcousticDrive(object):

    @staticmethod
    def make_acoustic_drives(const, linear, quad=[0]*4, power=[default_power]*4, velocity=teo2_ac_vel):
        acoustic_drives = [0]*4
        for k in range(4):
            acoustic_drives[k] = AcousticDrive(const[k], linear[k], quad[k], power[k], velocity)
        return array(acoustic_drives)
    
    def __init__(self, const, linear, quad=0, power=default_power, velocity=teo2_ac_vel):
        self.const = array(const, dtype=dtype(float))
        self.linear = array(linear, dtype=dtype(float))
        self.quad = array(quad, dtype=dtype(float))
        self.power = array(power, dtype=dtype(float))
        self.velocity = velocity
        
    def get_local_acoustics(self, time, ray_position, aod_centre, aod_direction):
        distance = dot(ray_position[0:2] - aod_centre, aod_direction[0:2])
        frequency = self.const + self.linear * (time - distance/self.velocity) + self.quad * (time - distance/self.velocity)**2
        return Acoustics(frequency, self.power, self.velocity)