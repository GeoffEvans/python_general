class Aod:
    transducer_width = 0
    crystal_width = 0
    sound_direction = [0, 0, 0]
    
    def __init__(self, transducer_width, crystal_width, sound_direction):
        self.crystal_width = crystal_width
        self.transducer_width = transducer_width
        self.sound_direction = sound_direction
        
        