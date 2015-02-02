import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import set_up_utils as s

def update_lines(num, line_data, lines) :
    for line, data in zip(lines, line_data[num]) :
        # set xy then z stupid api        
        line.set_xdata(data[:,0])
        line.set_ydata(data[:,1])
        line.set_3d_properties(data[:,2])
    return lines
    
wavelength = 800e-9    
distance = 0.5
num_times = 151
aol = s.set_up_aol(wavelength, focus_position=[0,0,0.5] )    
line_data = []

for time in np.linspace(-15e-6, 15e-6, num_times)[:-1]:
    rays = s.get_ray_bundle(wavelength)
    
    start = np.atleast_3d([r.position for r in rays]).transpose((0,2,1))
    [r.propagate_free_space(10e-2) for r in rays]
    (paths, _) = aol.propagate_to_distance_past_aol(rays, time, distance)
    
    paths_extended = np.concatenate( (start, paths), axis=1).copy()
    line_data.append(paths_extended) # [time, rays, plane, xyz]

fig = plt.figure()
ax = p3.Axes3D(fig)

lines = [ax.plot(data[:,0], data[:,1], data[:,2])[0] for data in line_data[0]]

ax.set_xlim3d([-0.02, 0.02])
ax.set_xlabel('X')

ax.set_ylim3d([-0.02, 0.02])
ax.set_ylabel('Y')

ax.set_zlim3d([0.0, 1.0])
ax.set_zlabel('Z')

ax.set_title('3D Test')

line_ani = animation.FuncAnimation(fig, update_lines, num_times, fargs=(line_data, lines),
                              interval=50, blit=False)

plt.show()