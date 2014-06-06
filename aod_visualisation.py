from aod import Aod
from ray import Ray
from acoustics import Acoustics
from numpy import linspace, pi, sin, cos, zeros, shape, arange, abs, sqrt, arcsin

normal = [0,0,1]
sound_direction = [1,0,0]
aperture_width = 15e-3
transducer_width = 3.6e-3
crystal_thickness = 5e-3
order = -1

aod = Aod(normal, sound_direction, aperture_width, transducer_width, crystal_thickness, order)

mhz_range = linspace(20, 60, 20)
degrees_range =  linspace(0, 2, 20) 

def plot_surface(x_array, y_array, z_func, labels):
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    from matplotlib import cm
    from numpy import meshgrid, vectorize
    
    (x, y) = meshgrid(x_array, y_array)
    z_func_vec = vectorize(z_func)
    z = z_func_vec(x, y) 
    
    fig = plt.figure()
    ax = fig.gca(projection='3d')               # to work in 3d
    
    surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0)   # plot a 3d surface plot
    
    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])
    ax.set_zlabel(labels[2])
    
    #fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()

def plot_mismatch_angle_freq():
    
    def func(deg, mhz):
        from xu_stroud_model import diffract_by_wavevector_triangle
    
        ang = deg * pi/180
        wavevector_unit = [sin(ang), 0, cos(ang)]
        ray = Ray([0,0,0], wavevector_unit, 800e-9)
        acoustics = Acoustics(mhz*1e6, 1)
        
        (mismatch,_) = diffract_by_wavevector_triangle(aod, ray, acoustics)
        return abs(mismatch)
        
    labels = ["incidence angle / deg","frequency / MHz","wavevector mismatch / 1/m"]
    plot_surface(degrees_range, mhz_range, func, labels)
    
def plot_efficiency_xangle_freq():
    
    def func(deg, mhz):
        from xu_stroud_model import diffract_acousto_optically
    
        ang = deg * pi/180
        wavevector_unit = [sin(ang), 0, cos(ang)]
        ray = Ray([0,0,0], wavevector_unit, 800e-9)
        acoustics = Acoustics(mhz*1e6, 1)
        
        diffract_acousto_optically(aod, ray, acoustics)
        return ray.energy
    
    labels = ["incidence angle / deg","frequency / MHz","efficiency"]
    plot_surface(degrees_range, mhz_range, func, labels)

def plot_efficiency_xangle_yangle():
    
    def func(deg, deg_trans):
        from xu_stroud_model import diffract_acousto_optically
    
        ang = deg * pi/180
        ang_trans = deg_trans * pi/180
        wavevector_unit = [sin(ang), sin(ang_trans), sqrt(1 - sin(ang)**2 - sin(ang_trans)**2)]
        import pdb; pdb.set_trace
        ray = Ray([0,0,0], wavevector_unit, 800e-9)
        acoustics = Acoustics(35e6, 1)        
        
        diffract_acousto_optically(aod, ray, acoustics)
        return ray.energy
    
    labels = ["incidence angle / deg","transverse incidence angle / deg","efficiency"]
    plot_surface(degrees_range, degrees_range, func, labels)

def plot_xangleout_xangle_freq():
    
    def func(deg, mhz):
        from xu_stroud_model import diffract_acousto_optically
    
        ang = deg * pi/180
        wavevector_unit = [sin(ang), 0, cos(ang)]
        ray = Ray([0,0,0], wavevector_unit, 800e-9)
        acoustics = Acoustics(mhz*1e6, 1)
        
        diffract_acousto_optically(aod, ray, acoustics)
        return arcsin(ray.wavevector_unit[0]) * 180/pi

    labels = ["incidence angle / deg","frequency / MHz","diffracted angle / deg"]
    plot_surface(degrees_range, mhz_range, func, labels)

def plot_xangleout_xangle_yangle():
    
    def func(deg, deg_trans):
        from xu_stroud_model import diffract_acousto_optically
    
        ang = deg * pi/180
        ang_trans = deg_trans * pi/180
        wavevector_unit = [sin(ang), sin(ang_trans), sqrt(1 - sin(ang)**2 - sin(ang_trans)**2)]
        ray = Ray([0,0,0], wavevector_unit, 800e-9)
        acoustics = Acoustics(35e6, 1)        
        
        diffract_acousto_optically(aod, ray, acoustics)
        return arcsin(ray.wavevector_unit[0]) * 180/pi
    
    labels = ["incidence angle / deg","transverse incidence angle / deg","diffracted angle / deg"]
    plot_surface(degrees_range, degrees_range, func, labels)
