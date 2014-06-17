from aol_simple import AolSimple
from acoustics import AcousticDrive, default_power, teo2_ac_vel
from aol_drive import calculate_drive_freq_4
from numpy import append, array, dtype, concatenate, zeros
import copy

class AolFull(object):
       
    @staticmethod
    def create_aol(aods, aod_spacing, order, op_wavelength, base_freq, pair_deflection_ratio,\
                   focus_position, focus_velocity, ac_power=[default_power]*4, ac_velocity=teo2_ac_vel):

        crystal_thickness = array([a.crystal_thickness for a in aods], dtype=dtype(float))
        (const, linear, quad) = calculate_drive_freq_4(order, op_wavelength, ac_velocity, aod_spacing, crystal_thickness, \
                                base_freq, pair_deflection_ratio, focus_position, focus_velocity)
       
        acoustic_drives = AcousticDrive.make_acoustic_drives(const, linear, quad, ac_power, ac_velocity)
        return AolFull(aods, aod_spacing, acoustic_drives, order, op_wavelength)
       
    def __init__(self, aods, aod_spacing, acoustic_drives, order, op_wavelength): 
        self.aods = array(aods)
        self.aod_spacing = array(aod_spacing, dtype=dtype(float))
        self.acoustic_drives = array(acoustic_drives)
        self.order = order
        
        simple = AolSimple(order, self.aod_spacing, self.acoustic_drives)
        self.base_ray_positions = simple.find_base_ray_positions(op_wavelength)
     
    def plot_ray_through_aol(self, ray, time, distance):
        import matplotlib as mpl
        from mpl_toolkits.mplot3d import Axes3D
        import matplotlib.pyplot as plt
        from numpy import meshgrid, atleast_2d
        
        new_ray = copy.deepcopy(ray)
        new_ray.propagate_free_space_z(self.aod_spacing.sum())

        (path, _) = self.propagate_to_distance_past_aol(new_ray, time, distance)
        path_extended = concatenate( (atleast_2d(ray.position), path) )
        
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot(path_extended[:,0], path_extended[:,1], path_extended[:,2])
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')  

        def add_planes():        
            for point in path_extended[1:9]:
                (xpts, ypts) = array(meshgrid([1, -1], [1, -1])) * 1e-2
                xpts += point[0]
                ypts += point[1]
                zpts = point[2] + zeros((2,2))
                ax.plot_surface(xpts, ypts, zpts, color='blue', alpha=.3, linewidth=0, zorder=3)

        add_planes()             
        plt.show()
        return plt
        
    def propagate_to_distance_past_aol(self, ray, time, distance=0):
        crystal_thickness = array([a.crystal_thickness for a in self.aods], dtype=dtype(float))
        reduced_spacings = append(self.aod_spacing, distance) - crystal_thickness 
        path = zeros( (9,3) )
        energies = zeros( (4,3) )

        def diffract_and_propagate(ray, time, aod_number):
            path[2*aod_number - 2,:] = ray.position
            self.diffract_at_aod(ray, time, aod_number)
            path[2*aod_number - 1,:] = ray.position
            energies[aod_number-1] = ray.energy
            ray.propagate_free_space_z(reduced_spacings[aod_number-1])
        
        for k in range(4):
            diffract_and_propagate(ray, time, k+1)
        
        path[8,:] = ray.position
        return (path, energies)
        
    def diffract_at_aod(self, ray, time, aod_number):
        idx = aod_number-1
        
        aod = self.aods[idx]
        base_ray_position = self.base_ray_positions[idx]
        drive = self.acoustic_drives[idx]
        local_acoustics = drive.get_local_acoustics(time, ray.position, base_ray_position, aod.acoustic_direction)
        
        aod.propagate_ray(ray, local_acoustics, self.order)