from aod import Aod
from ray import Ray
from acoustics import Acoustics
from numpy import linspace, pi, sin, cos, abs, sqrt, arcsin, max
from plot_utils import generic_plot_surface, generic_plot
from xu_stroud_model import diffract_by_wavevector_triangle
from vector_utils import normalise
from set_up_utils import transducer_efficiency_narrow,\
    transducer_efficiency_wide

normal = normalise([0,0,100])
sound_direction = [1,0,0]
transducer_height = 16e-3
transducer_width = 1.2e-3
crystal_thickness = 8e-3
order = -1
op_wavelength_vac = 800e-9
resolution = 30
pwr = 1.5

aod = Aod(normal, sound_direction, transducer_height, transducer_width, crystal_thickness, transducer_efficiency_narrow)

mhz_range = linspace(10, 70, resolution)
degrees_range =  linspace(0, 5, resolution) 

def plot_mismatch_angle_freq():
    
    def func(deg, mhz):
        ang = deg * pi/180
        wavevector_unit = [sin(ang), 0, cos(ang)]
        ray = Ray([0,0,0], wavevector_unit, op_wavelength_vac)
        acoustics = Acoustics(mhz*1e6, pwr)
        
        (mismatch,_) = diffract_by_wavevector_triangle(aod, [ray], [acoustics], order, (0,1))
        return abs(mismatch)
        
    labels = ["incidence angle / deg","frequency / MHz","wavevector mismatch / 1/m"]
    generic_plot_surface(degrees_range, mhz_range, func, labels)

def plot_efficiency_xangle_freq():
    
    def func(deg, mhz):
        ang = deg * pi/180
        wavevector_unit = [sin(ang), 0, cos(ang)]
        ray = Ray([0,0,0], wavevector_unit, op_wavelength_vac)
        acoustics = Acoustics(mhz*1e6, pwr)
        
        aod.propagate_ray([ray], [acoustics], order)
        return ray.energy
    
    labels = ["incidence angle / deg","frequency / MHz","efficiency"]
    generic_plot_surface(degrees_range, mhz_range, func, labels)

def plot_efficiency_xangle_yangle():
    
    def func(deg, deg_trans):
        ang = deg * pi/180
        ang_trans = deg_trans * pi/180
        wavevector_unit = [ang, ang_trans, sqrt(1 - ang**2 - ang_trans**2)]
        ray = Ray([0,0,0], wavevector_unit, op_wavelength_vac)
        acoustics = Acoustics(35e6, pwr)        
        
        aod.propagate_ray([ray], [acoustics], order)
        return ray.energy
    
    labels = ["incidence angle / deg","transverse incidence angle / deg","efficiency"]
    generic_plot_surface(linspace(0.00, 0.1, 20)/pi*180, linspace(-0.3, 0.3, 60)/pi*180, func, labels)

def plot_xangleout_xangle_freq():
    
    def func(deg, mhz):
        ang = deg * pi/180
        wavevector_unit = [sin(ang), 0, cos(ang)]
        ray = Ray([0,0,0], wavevector_unit, op_wavelength_vac)
        acoustics = Acoustics(mhz*1e6, pwr)
        
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
    generic_plot_surface(degrees_range, linspace(-5, 5, resolution), func, labels)

def plot_efficiency_freq():
     
    def func(mhz):
        ang = 2.2 * pi / 180
        wavevector_unit = [sin(ang), 0, cos(ang)]
        ray = Ray([0,0,0], wavevector_unit, op_wavelength_vac)
        acoustics = Acoustics(mhz*1e6, pwr)
        
        aod.propagate_ray([ray], [acoustics], order)
        return ray.energy
    
    labels = ["frequency / MHz","efficiency"]
    generic_plot(mhz_range, func, labels)
    
def plot_efficiency_freq_max():
     
    def func(mhz):
        deg_range =  linspace(1.9, 3.1, 40) 
        rad_range = deg_range * pi / 180
        rays = [Ray([0,0,0], [sin(ang), 0, cos(ang)], op_wavelength_vac) for ang in rad_range]
        acoustics = Acoustics(mhz*1e6, pwr)
        
        aod.propagate_ray(rays, [acoustics]*len(rays), order)
        return max([r.energy for r in rays])
    
    labels = ["frequency / MHz","efficiency"]
    generic_plot(mhz_range, func, labels, (20,50,0,1))
    
def plot_efficiency_xangle():
    
    def func(deg):
        ang = deg * pi/180
        wavevector_unit = [sin(ang), 0, cos(ang)]
        ray = Ray([0,0,0], wavevector_unit, op_wavelength_vac)
        acoustics = Acoustics(35e6, 1.5)
        
        aod.propagate_ray([ray], [acoustics], order)
        return ray.energy
    
    labels = ["incidence angle / deg","efficiency"]
    generic_plot(degrees_range, func, labels)

def plot_efficiency_power():
    
    def func(pwr):
        deg_range =  linspace(1.9, 3.1, 40) 
        rad_range = deg_range * pi / 180
        rays = [Ray([0,0,0], [sin(ang), 0, cos(ang)], op_wavelength_vac) for ang in rad_range]
        acoustics = Acoustics(40e6, pwr)
        
        aod.propagate_ray(rays, [acoustics]*len(rays), order)
        return max([r.energy for r in rays])
    
    labels = ["acoustic power / Watts","efficiency"]
    generic_plot(linspace(0,2.5,20), func, labels)
    
if __name__ == '__main__':
    plot_efficiency_xangle_yangle()