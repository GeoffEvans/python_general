#Take a field, transform, propagate, inverse-transform, look at metric.
import numpy as np
import numpy.fft as ft
import matplotlib.pyplot as plt

k = 20
z = 2e3
step = 1

x_arr = np.arange(-200, 200, step)
z_arr = np.linspace(z*0.5, z*2, 199)

square = (np.abs(x_arr) < 10) * 1
gaussian = np.exp(- np.power(x_arr, 2) * 1. / (2 * 4000) )
focusing = gaussian * np.exp(-1j * k/2/z * np.power(x_arr, 2))
sph_ab = focusing * np.exp(-1j * k * np.power(x_arr, 4) * 1e-9)

def propagate_field(z_elem, k_x_field, k_z):
        new_k_x_field = k_x_field * np.exp(1j * k_z * z_elem)
        new_x_field = ft.fftshift(ft.ifft(new_k_x_field))
        return new_x_field

def get_resolution(spherical, do_plot=False):
    x_field = focusing * np.exp(-1j * k * np.power(x_arr, 4) * 1e-9 * spherical)
    k_x_field = ft.fft(ft.ifftshift(x_field))

    k_x = 2 * np.pi * ft.fftfreq(k_x_field.size, step)

    k_z = np.zeros(k_x.shape, np.cfloat)
    index1 = np.power(k_x, 2) <= np.power(k, 2)
    k_z[index1] = np.power(np.power(k, 2) - np.power(k_x[index1], 2), 0.5).astype(np.cfloat)
    index2 = np.power(k_x, 2) > np.power(k, 2)
    k_z[index2] = 1j * np.power(- np.power(k, 2) + np.power(k_x[index2], 2), 0.5)    
    
    new_xz_fields = [propagate_field(z_elem, k_x_field, k_z) for z_elem in z_arr]
    
    if do_plot:
        plt.subplot(221)
        plt.plot(x_arr, np.abs(x_field))
        
        plt.subplot(222)
        plt.plot(x_arr, ft.fftshift(np.abs(k_x_field)))
        
        plt.subplot(2, 2, (3, 4))
        plt.pcolor(x_arr, z_arr, np.abs(new_xz_fields))
    
    field_max = np.max(np.power(np.abs(new_xz_fields), 4))
    elem_filter = np.power(np.abs(new_xz_fields), 4) >= field_max/2
    fwhm_x = 2 * np.max(np.abs(x_arr[np.any(elem_filter, 0)]))
    fwhm_z = 2 * np.max(np.abs(z_arr[np.any(elem_filter, 1)] - z))
    return (fwhm_x, fwhm_z)

spherical = np.linspace(-10,10,199)
fwhm_x, fwhm_z = zip(*[get_resolution(sph) for sph in spherical])
plt.hold(True)
plt.plot(spherical, fwhm_x)
plt.plot(spherical, map(lambda x: x/100, fwhm_z))
plt.hold(False)
print np.min(fwhm_x), np.min(fwhm_z)