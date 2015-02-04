import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import set_up_utils as s
import acoustics as a
from acoustics import pointing_ramp_time

def update_lines(num, line_data, lines, freq, linef, r1):
    for line, data in zip(lines, line_data[num]):
        # set xy then z stupid api        
        line.set_xdata(data[:,2])
        line.set_ydata(data[:,0])
    linef.set_ydata(freq[num])
    return lines, linef, r1
    
wavelength = 800e-9    
distance = 0.5
num_times = 61
aod = s.make_aod_wide([0,0,1], [1,0,0])
line_data = []
freq = []

x_list = np.linspace(-1, 1) * 7e-3

def chirp(t):
    n = t/pointing_ramp_time
    if n > 5:
        return (10 - n) * 2e11
    return n * 2e11

def centre(t):
    n = t/pointing_ramp_time
    if n > 5:
        return (10 - n) * 12e6 + 10e6
    return n * 12e6 + 10e6

for time in np.linspace(-0/2, pointing_ramp_time/2, num_times)[:-1]:
    rays = s.get_ray_bundle(wavelength)
    drive = a.AcousticDrive(40e6, 0)
    
    start = np.array([r.position for r in rays]).copy()
    [r.propagate_free_space(10e-2) for r in rays]
    enter_aod = np.array([r.position for r in rays]).copy()
    local_acoustics = drive.get_local_acoustics(time, [r.position for r in rays], [0,0], aod.acoustic_direction)
    aod.propagate_ray(rays, local_acoustics, 1)
    exit_aod = np.array([r.position for r in rays]).copy()
    [r.propagate_to_plane([0,0,1],[0,0,1]) for r in rays]
    end = np.array([r.position for r in rays]).copy()
    
    paths_extended = np.dstack( (start, enter_aod, exit_aod, end)).transpose([0,2,1])
    line_data.append(paths_extended) # [time, rays, plane, xyz]
    
    local_acoustics2 = drive.get_local_acoustics(time, [[x,0] for x in x_list], [0,0], aod.acoustic_direction)
    freq.append([la.frequency for la in local_acoustics2])

fig = plt.figure()
plt.subplot(2, 1, 1)
ax = fig.gca()
lines = [ax.plot(data[:,2], data[:,0])[0] for data in line_data[0]]

ax.set_ylim([-0.01, 0.06])
ax.set_ylabel('x / m')
ax.set_xlim([0.0, .8])
ax.set_xlabel('z / m')

r1 = plt.Rectangle((0.1, -0.01), 0.008, 0.02, fc='y')
ax.add_patch(r1)

af = plt.subplot(2, 1, 2)
linef = af.plot(x_list, freq[0])[0]
af.set_xlabel('x / m')
af.set_ylabel('frequency / Hz')
af.set_ylim([0e6, 70e6])

#line_ani = animation.FuncAnimation(fig, update_lines, num_times-1, \
#    fargs=(line_data, lines, freq, linef, r1), interval=50, blit=False)

#plt.rcParams['animation.ffmpeg_path'] ='C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe'
#mywriter = animation.FFMpegWriter(fps=80)
#plt.rcParams['animation.convert_path'] ='C:\\Program Files\\ImageMagick-6.9.0-Q8\\convert.exe'
#line_ani.save('ani.gif', writer='imagemagick', fps=20)

plt.show()