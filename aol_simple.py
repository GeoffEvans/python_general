from numpy import array, dtype, pi, atleast_2d, concatenate, zeros, append
from acoustics import AcousticDrive
from error_utils import check_is_unit_vector, check_is_of_length
import copy

class AolSimple(object):
# Can work with ray or ray_paraxial

    @staticmethod
    def create_aol(order, op_wavelength, ac_velocity, aod_spacing, base_freq, pair_deflection_ratio, focus_position, focus_velocity):
        from aol_drive import calculate_drive_freq_4
        
        (const, linear, _) = calculate_drive_freq_4(order, op_wavelength, ac_velocity, aod_spacing, 0, \
                                                base_freq, pair_deflection_ratio, focus_position, focus_velocity)
        acoustic_drives = AcousticDrive.make_acoustic_drives(const, linear)

        aol = AolSimple(order, aod_spacing, acoustic_drives)
        aol.set_base_ray_positions(op_wavelength)
        return aol

    @staticmethod
    def create_aol_from_drive(order, aod_spacing, const, linear, op_wavelength):
        
        acoustic_drives = AcousticDrive.make_acoustic_drives(const, linear)

        aol = AolSimple(order, aod_spacing, acoustic_drives)
        aol.set_base_ray_positions(op_wavelength)
        return aol

    def __init__(self, order, aod_spacing, acoustic_drives, base_ray_positions=zeros((4,2)), aod_directions=[[1,0,0],[0,1,0],[-1,0,0],[0,-1,0]]):
        self.order = order
        self.aod_spacing = array(aod_spacing, dtype=dtype(float))
        self.acoustic_drives = acoustic_drives
        self.aod_directions = array(aod_directions, dtype=dtype(float))
        self.base_ray_positions = array(base_ray_positions, dtype=dtype(float))
        
        for d in self.aod_directions:
            check_is_unit_vector(d)
        check_is_of_length(3, self.aod_spacing)
        check_is_of_length(4, self.acoustic_drives)
        check_is_of_length(4, self.aod_directions)
        check_is_of_length(4, self.base_ray_positions)
    
    def set_base_ray_positions(self, op_wavelength):
        self.base_ray_positions = self.find_base_ray_positions(op_wavelength)
    
    def find_base_ray_positions(self, op_wavelength):
        from ray_paraxial import RayParaxial
        tracer_ray = RayParaxial([0,0,0], [0,0,1], op_wavelength)
        path = self.propagate_to_distance_past_aol(tracer_ray, 0)
        return path[:,0:2]
    
    def plot_ray_through_aol(self, ray, time, distance):
        import matplotlib as mpl
        from mpl_toolkits.mplot3d import Axes3D
        import matplotlib.pyplot as plt
        from numpy import meshgrid, atleast_2d
        
        new_ray = copy.deepcopy(ray)
        new_ray.propagate_free_space_z(self.aod_spacing.sum())

        path = self.propagate_to_distance_past_aol(new_ray, time, distance)
        path_extended = concatenate( (atleast_2d(ray.position), path) )
        
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot(path_extended[:,0], path_extended[:,1], path_extended[:,2])
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')  

        def add_planes():        
            for point in path_extended[1:5]:
                (xpts, ypts) = meshgrid([1, -1], [1, -1])
                xpts += point[0]
                ypts += point[1]
                zpts = point[2] + zeros((2,2))
                ax.plot_surface(xpts, ypts, zpts, color='blue', alpha=.3, linewidth=0, zorder=3)

        add_planes()             
        plt.show()
        return plt
    
    def propagate_to_distance_past_aol(self, ray, time, distance=0):
        path = zeros( (4,3) )
        path[0,:] = ray.position
        
        spacings = append(self.aod_spacing, distance) 
            
        def diffract_and_propagate(aod_number):
            path[aod_number-1,:] = ray.position
            self.diffract_at_aod(ray, time, aod_number)
            ray.propagate_free_space_z(spacings[aod_number-1])

        for k in range(spacings.size):
            diffract_and_propagate(k+1)
        
        return path
        
    def diffract_at_aod(self, ray, time, aod_number):
        idx = aod_number-1
        
        aod_dir = self.aod_directions[idx]
        drive = self.acoustic_drives[idx]
        
        local_acoustics = drive.get_local_acoustics(time, ray.position, self.base_ray_positions[idx], aod_dir)
        
        wavevector_shift = self.order * (2 * pi * local_acoustics.frequency / local_acoustics.velocity) * aod_dir 
        ray.wavevector_vac += wavevector_shift 