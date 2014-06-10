from numpy import array, dtype, pi, zeros, atleast_2d, concatenate
from acoustics import Acoustics
from testutils import check_is_unit_vector, check_is_of_length
import copy

class Aol(object):
# Can work with ray or ray_paraxial

    def __init__(self, order, aod_spacing, freq_const, freq_linear, aod_directions=[[1,0,0],[0,1,0],[-1,0,0],[0,-1,0]]):
        self.order = order
        self.aod_spacing = array(aod_spacing, dtype=dtype(float))
        self.freq_const = array(freq_const, dtype=dtype(float))
        self.freq_linear = array(freq_linear, dtype=dtype(float))
        self.aod_directions = array(aod_directions, dtype=dtype(float))
        self.normal_to_plane = array([0, 0, 1], dtype=dtype(float))
        
        for d in self.aod_directions:
            check_is_unit_vector(d)
        check_is_of_length(3, self.aod_spacing)
        check_is_of_length(4, self.freq_const)
        check_is_of_length(4, self.freq_linear)
        check_is_of_length(4, self.aod_directions)
            
    def plot_ray_through_aol(self, ray, time, distance):
        import matplotlib as mpl
        from mpl_toolkits.mplot3d import Axes3D
        import matplotlib.pyplot as plt
        from numpy import zeros, meshgrid
        
        new_ray = copy.deepcopy(ray)
        path = self.propagate_to_distance_from_aol(new_ray, time, distance)

        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot(path[:,0], path[:,1], path[:,2])
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')  
        
        for point in path[1:5]:
            (xpts, ypts) = meshgrid([1, -1], [1, -1])
            xpts += point[0]
            ypts += point[1]
            zpts = point[2] + zeros((2,2))
            ax.plot_surface(xpts, ypts, zpts, color='blue', alpha=.3, linewidth=0, zorder=3)
             
        plt.show()
        return plt
    
    def propagate_to_distance_from_aol(self, ray, time, distance):
        path = self.propagate_through_aol(ray, time)
        point_on_plane = ray.position + [0, 0, distance]
        ray.propagate_to_plane(point_on_plane, self.normal_to_plane)
        return concatenate( (path, atleast_2d(ray.position)) )
        
    def propagate_through_aol(self, ray, time):

        positions = zeros( (5,3) )
        positions[0,:] = ray.position

        def propagate_and_deflect(aod_number, distance):
            ray.propagate_free_space_z(distance)
            positions[aod_number,:] = ray.position
            self.deflect_at_aod(ray, time, aod_number)

        propagate_and_deflect(1, self.aod_spacing[0]*2)
        propagate_and_deflect(2, self.aod_spacing[0])
        propagate_and_deflect(3, self.aod_spacing[1])
        propagate_and_deflect(4, self.aod_spacing[2])
        
        return positions
        
    def deflect_at_aod(self, ray, time, aod_number):
        frequency = self.freq_const[aod_number-1] + self.freq_linear[aod_number-1] * time
        acoustics = Acoustics(frequency)
        
        wavevector_shift = self.order * (2 * pi * acoustics.frequency / acoustics.velocity) * self.aod_directions[aod_number-1] 
        ray.wavevector_vac += wavevector_shift 