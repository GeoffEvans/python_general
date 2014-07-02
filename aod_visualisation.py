from aod import Aod
from ray import Ray
from acoustics import Acoustics
from numpy import linspace, pi, sin, cos, abs, sqrt, arcsin
from plot_utils import generic_plot_surface, generic_plot
from xu_stroud_model import diffract_by_wavevector_triangle
from vector_utils import normalise

normal = normalise([0,0,100])
sound_direction = [1,0,0]
aperture_width = 15e-3
transducer_width = 1.2e-3
crystal_thickness = 8e-3
order = -1
op_wavelength_vac = 900e-9
resolution = 30
pwr = 5

aod = Aod(normal, sound_direction, aperture_width, transducer_width, crystal_thickness)

mhz_range = linspace(10, 60, resolution)
degrees_range =  linspace(-1, 6, resolution) 

def plot_mismatch_angle_freq():
    
    def func(deg, mhz):
        ang = deg * pi/180
        wavevector_unit = [sin(ang), 0, cos(ang)]
        ray = Ray([0,0,0], wavevector_unit, op_wavelength_vac)
        acoustics = Acoustics(mhz*1e6, pwr)
        
        (mismatch,_) = diffract_by_wavevector_triangle(aod, [ray], [acoustics], order)
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
        acoustics = Acoustics(35e6, 1)        
        
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
    
if __name__ == '__main__':
    plot_efficiency_xangle_freq()