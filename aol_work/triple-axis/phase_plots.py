import numpy as np
import matplotlib.pyplot as plt

def plot_surface(x, y, z):
    fig = plt.figure()
    ax = fig.gca()
    cs = ax.pcolor(x, y, z, cmap='Reds')
    cs.set_rasterized(True)
   
    ax.set_xlabel('x (mm)')
    ax.set_ylabel('y (mm)')
    cb = plt.colorbar(cs, orientation = 'vertical')
    cb.set_label('phase (radians)')
    cb.solids.set_rasterized(True)
    #cs.set_clim(vmin=0,vmax=1)
    plt.tick_params(direction='out')
    plt.axes().set_aspect('equal', 'datalim')
    plt.show()
    
if __name__ == '__main__':
    line = np.linspace(-0.5,0.5)
    x_grid, y_grid = np.meshgrid(line, line)    
    rad120 = np.pi/1.5
    x_grid_120 = np.cos(rad120) * x_grid + np.sin(rad120) * y_grid
    y_grid_120 = np.cos(rad120) * y_grid - np.sin(rad120) * x_grid
    x_grid_240 = np.cos(-rad120) * x_grid + np.sin(-rad120) * y_grid
    y_grid_240 = np.cos(-rad120) * y_grid - np.sin(-rad120) * x_grid
    
    phase = np.zeros(np.shape(x_grid)); # initial
    plot_surface(x_grid, y_grid, phase)
    phase += np.power(x_grid, 2)   # AOD pass
    plot_surface(x_grid, y_grid, phase)
    
    phase = np.power(x_grid_120, 2)     # 1st rotation
    plot_surface(x_grid, y_grid, phase)
    phase += np.power(x_grid, 2)   # AOD pass
    plot_surface(x_grid, y_grid, phase)

    phase = np.power(x_grid_120, 2) + np.power(x_grid_240, 2)    # 2nd rotation
    plot_surface(x_grid, y_grid, phase)
    phase += np.power(x_grid, 2)   # AOD pass
    plot_surface(x_grid, y_grid, phase)
