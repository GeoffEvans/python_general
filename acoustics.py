from numpy import pi, sqrt

class Acoustics(object):
    velocity = 612.8
    frequency = 0
    power = 0
    
    @property
    def wavevector_mag(self):
        return 2 * pi * self.frequency / self.velocity
    
    def __init__(self, frequency, velocity, power):
        self.frequency = frequency
        self.velocity = velocity
        self.power = power
    
    def wavevector(self, aod):
        return self.wavevector_mag * aod.acoustic_direction
    
    def amplitude(self, aod):
        teo2_density = 5990;
        numerator = 2 * self.power
        denominator = teo2_density * self.velocity**3 * aod.transducer_width * aod.aperture_width # assumes sqr aperture 
        return sqrt(numerator / denominator)