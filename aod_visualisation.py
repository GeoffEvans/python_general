from aod import Aod
from ray import Ray
from acoustics import Acoustics
from numpy import linspace, pi, sin, cos, abs, sqrt, arcsin
from xu_stroud_model import diffract_by_wavevector_triangle

normal = [0,0,1]
sound_direction = [1,0,0]
aperture_width = 15e-3
transducer_width = 3.6e-3
crystal_thickness = 5e-3
order = -1
op_wavelength_vac = 800e-9
resolution = 40

aod = Aod(normal, sound_direction, aperture_width, transducer_width, crystal_thickness)

mhz_range = linspace(20, 60, resolution)
degrees_range =  linspace(0, 4, resolution) 

def generic_plot_surface(x_array, y_array, z_func, labels):
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    from matplotlib import cm
    from numpy import meshgrid, vectorize
    
    (x, y) = meshgrid(x_array, y_array)
    z_func_vec = vectorize(z_func)
    z = z_func_vec(x, y) 
    
    fig = plt.figure()
    ax = fig.gca()               
    cs = ax.pcolor(x, y, z)   
    
    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])
    cb = plt.colorbar(cs, orientation = 'horizontal') 
    cb.set_label(labels[2]) 
 
    plt.show()

def plot_mismatch_angle_freq():
    
    def func(deg, mhz):
        ang = deg * pi/180
        wavevector_unit = [sin(ang), 0, cos(ang)]
        ray = Ray([0,0,0], wavevector_unit, op_wavelength_vac)
        acoustics = Acoustics(mhz*1e6, 1)
        
        (mismatch,_) = diffract_by_wavevector_triangle(aod, [ray], [acoustics], order)
        return abs(mismatch)
        
    labels = ["incidence angle / deg","frequency / MHz","wavevector mismatch / 1/m"]
    generic_plot_surface(degrees_range, mhz_range, func, labels)

def plot_efficiency_xangle_freq():
    
    def func(deg, mhz):
        ang = deg * pi/180
        wavevector_unit = [sin(ang), 0, cos(ang)]
        ray = Ray([0,0,0], wavevector_unit, op_wavelength_vac)
        acoustics = Acoustics(mhz*1e6, 1)
        
        aod.propagate_ray([ray], [acoustics], order)
        return ray.energy
    
    labels = ["incidence angle / deg","frequency / MHz","efficiency"]
    generic_plot_surface(degrees_range, mhz_range, func, labels)

def plot_efficiency_xangle_yangle():
    
    def func(deg, deg_trans):
        ang = deg * pi/180
        ang_trans = deg_trans * pi/180
        wavevector_unit = [sin(ang), sin(ang_trans), sqrt(1 - sin(ang)**2 - sin(ang_trans)**2)]
        import pdb; pdb.set_trace
        ray = Ray([0,0,0], wavevector_unit, op_wavelength_vac)
        acoustics = Acoustics(35e6, 1)        
        
        aod.propagate_ray([ray], [acoustics], order)
        return ray.energy
    
    labels = ["incidence angle / deg","transverse incidence angle / deg","efficiency"]
    generic_plot_surface(degrees_range, degrees_range, func, labels)

def plot_xangleout_xangle_freq():
    
    def func(deg, mhz):
        ang = deg * pi/180
        wavevector_unit = [sin(ang), 0, cos(ang)]
        ray = Ray([0,0,0], wavevector_unit, op_wavelength_vac)
        acoustics = Acoustics(mhz*1e6, 1)
        
        aod.propagate_ray([ray], [acoustics], order)
        return arcsin(ray.wavevector_unit[0]) * 180/pi

    labels = ["incidence angle / deg","frequency / MHz","diffracted angle / deg"]
    generic_plot_surface(degrees_range, mhz_range, func, labels)

def plot_xangleout_xangle_yangle():
    
    def func(deg, deg_trans):
        ang = deg * pi/180
        ang_trans = deg_trans * pi/180
        wavevector_unit = [sin(ang), sin(ang_trans), sqrt(1 - sin(ang)**2 - sin(ang_trans)**2)]
        ray = Ray([0,0,0], wavevector_unit, op_wavelength_vac)
        acoustics = Acoustics(35e6, 1)        
        
        aod.propagate_ray([ray], [acoustics], order)
        return arcsin(ray.wavevector_unit[0]) * 180/pi
    
    labels = ["incidence angle / deg","transverse incidence angle / deg","diffracted angle / deg"]
    generic_plot_surface(degrees_range, degrees_range, func, labels)
