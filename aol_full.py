from aol_simple import AolSimple
from acoustics import AcousticDrive, default_power, teo2_ac_vel
from aol_drive import calculate_drive_freq_4

class Aol(object):
       
    @staticmethod
    def create_aol(aods, space_before_each_aod, order, op_wavelength, base_freq, pair_deflection_ratio,\
                   focus_position, focus_velocity, ac_power=default_power, ac_velocity=teo2_ac_vel):
       
        crystal_thickness = [a.crystal_thickness for a in aods]
       
        (const, linear, quad) = calculate_drive_freq_4(order, op_wavelength, ac_velocity, space_before_each_aod[1:], crystal_thickness, \
                                base_freq, pair_deflection_ratio, focus_position, focus_velocity)
       
        acoustic_drives = AcousticDrive.make_acoustic_drives(const, linear, quad, ac_power, ac_velocity)
        return Aol(aods, space_before_each_aod, acoustic_drives, order, op_wavelength)
       
    def __init__(self, aods, space_before_each_aod, acoustic_drives, order, op_wavelength): 
        self.aods = aods
        self.spacings = space_before_each_aod
        self.acoustic_drives = acoustic_drives
        
        simple = AolSimple(order, self.spacings[1:], self.acoustic_drives)
        simple.set_base_ray_positions(op_wavelength)
        self.base_ray_centres  = simple.base_ray_positions
         
    def propagate_to_distance_past_aol(self, ray, time, distance):
        self.propagate_through_aol(ray, time)
        ray.propagate_free_space_z(distance)
        
    def propagate_through_aol(self, ray, time):
        for k in range(4):
            self.propagate_to_aod_and_diffract(ray, time, k)
        
    def propagate_to_aod_and_diffract(self, ray, time, aod_number):
        idx = aod_number-1
        aod = self.aods[idx]
        base_ray_position = self.base_ray_centres[idx]
        
        ray.propagate_free_space_z(self.spacings[idx])
        
        drive = self.acoustic_drives[idx]
        local_acoustics = drive.get_local_acoustics(time, ray.position, base_ray_position, aod.sound_direction)
        
        aod.propagate_ray(ray, local_acoustics, self.order)