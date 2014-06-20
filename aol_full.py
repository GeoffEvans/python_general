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
     
    def plot_ray_through_aol(self, rays, time, distance):
        import matplotlib as mpl
        from mpl_toolkits.mplot3d import Axes3D
        import matplotlib.pyplot as plt
        from numpy import meshgrid, atleast_3d, mean
        
        num_rays = len(rays)
        new_rays = [0]*num_rays
        for m in range(num_rays): 
            new_rays[m] = copy.deepcopy(rays[m])
            new_rays[m].propagate_free_space_z(self.aod_spacing.sum())

        (paths, _) = self.propagate_to_distance_past_aol(new_rays, time, distance)
        start = atleast_3d([r.position for r in rays]).transpose((0,2,1))
        paths_extended = concatenate((start, paths), axis=1)
        
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        for m in range(num_rays):
            ax.plot(paths_extended[m,:,0], paths_extended[m,:,1], paths_extended[m,:,2])
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')  

        def add_planes():        
            for point in mean(paths_extended[1:9], axis=0):
                (xpts, ypts) = array(meshgrid([1, -1], [1, -1])) * 1e-2
                xpts += point[0]
                ypts += point[1]
                zpts = point[2] + zeros((2,2))
                ax.generic_plot_surface(xpts, ypts, zpts, color='blue', alpha=.3, linewidth=0, zorder=3)

        add_planes()             
        plt.show()
        return plt
        
    def propagate_to_distance_past_aol(self, rays, time, distance=0):
        num_rays = len(rays)
        crystal_thickness = array([a.crystal_thickness for a in self.aods], dtype=dtype(float))
        reduced_spacings = append(self.aod_spacing, distance) - crystal_thickness 
        paths = zeros( (len(rays),9,3) )
        energies = zeros( (len(rays),4) )

        def diffract_and_propagate(aod_number):
            for m in range(num_rays):
                paths[m,2*aod_number - 2,:] = rays[m].position
            self.diffract_at_aod(rays, time, aod_number)
            for m in range(num_rays):
                paths[m,2*aod_number - 1,:] = rays[m].position
                energies[m,aod_number-1] = rays[m].energy
                rays[m].propagate_free_space_z(reduced_spacings[aod_number-1])
        
        for k in range(4):
            diffract_and_propagate(k+1)
        
        for m in range(num_rays):
            paths[m,8,:] = rays[m].position
        return (paths, energies)
        
    def diffract_at_aod(self, rays, time, aod_number):
        idx = aod_number-1
        
        aod = self.aods[idx]
        base_ray_position = self.base_ray_positions[idx]
        drive = self.acoustic_drives[idx]
        local_acoustics = [drive.get_local_acoustics(time, r.position, base_ray_position, aod.acoustic_direction) for r in rays]
        
        aod.propagate_ray(rays, local_acoustics, self.order)