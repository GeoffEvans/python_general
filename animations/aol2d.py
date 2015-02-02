import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import set_up_utils as s

def update_lines(num, line_data, lines, f1, line1, f2, line2) :
    for line, data in zip(lines, line_data[num]) :
        # set xy then z stupid api        
        line.set_xdata(data[:,0])
        line.set_ydata(data[:,2])
    line1.set_ydata(f1[num])
    line2.set_ydata(f2[num])
    return lines, line1, line2
    
wavelength = 800e-9    
distance = 0.5
num_times = 61
aol = s.set_up_aol(wavelength, focus_position=[0,0,0.5] )    
line_data = []
f1 = []
f2 = []

x = np.linspace(-1, 1) * 7e-3

for time in np.linspace(0, 60e-6, num_times)[:-1]:
    rays = s.get_ray_bundle(wavelength)
    
    start = np.atleast_3d([r.position for r in rays]).transpose((0,2,1))
    [r.propagate_free_space(10e-2) for r in rays]
    (paths, _) = aol.propagate_to_distance_past_aol(rays, time, distance)
    
    paths_extended = np.concatenate( (start, paths), axis=1).copy()
    line_data.append(paths_extended) # [time, rays, plane, xyz]
    f1.append([f.frequency for f in aol.acoustic_drives[0].get_local_acoustics(time, [[pos,0,0] for pos in x], [0,0], aol.aods[0].acoustic_direction)])
    f2.append([f.frequency for f in aol.acoustic_drives[0].get_local_acoustics(time, [[pos,0,0] for pos in x], [0,0], aol.aods[2].acoustic_direction)])    

fig = plt.figure()
plt.subplot(1, 2, 1)
ax = fig.gca()
lines = [ax.plot(data[:,0], data[:,1])[0] for data in line_data[0]]

ax.set_xlim([-0.02, 0.02])
ax.set_xlabel('x / m')
ax.set_ylim([0.0, .8])
ax.set_ylabel('z / m')

a1 = plt.subplot(2, 2, 4)
line1 = a1.plot(x, f1[0])[0]
a1.set_xlabel('ray position at AOD2 / m')
a1.set_ylabel('frequency / Hz')
a1.set_ylim([25e6, 55e6])

a2 = plt.subplot(2, 2, 2)
line2 = a2.plot(x, f2[0])[0]
a2.set_xlabel('ray position at AOD1 / m')
a2.set_ylabel('frequency / Hz')
a2.set_ylim([25e6, 55e6])

line_ani = animation.FuncAnimation(fig, update_lines, num_times-1, fargs=(line_data, lines, f1, line1, f2, line2),
                              interval=50, blit=False)

plt.show()