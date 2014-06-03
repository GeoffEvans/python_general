from numpy import pi

class Acoustics:
    velocity = 612.8
    frequency = 0
    amplitude = 0
    
    @property
    def wavevector_vac_mag(self):
        return 2 * pi * self.frequency / self.velocity
    
    def __init__(self, frequency, velocity, power):
        self.frequency = frequency
        self.velocity = velocity
        self.amplitude = power
    
    def wavevector_vac(self, direction):
        return self.wavevector_vac_mag * direction