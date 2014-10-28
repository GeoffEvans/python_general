#Take a field, transform, propagate, inverse-transform, look at metric.
import numpy as np
import numpy.fft as ft
import matplotlib.pyplot as plt

k = 20
z = 2e3
step = 1

arr = np.arange(-200, 200, step)
x_arr, y_arr = np.meshgrid(arr, arr)
z_arr = np.linspace(z*0.5, z*2, 100)

circle = (np.power(x_arr, 2) + np.power(y_arr, 2) < 100) * 1
gaussian = np.exp(- (np.power(x_arr, 2) + np.power(y_arr, 2)) \
    * 1. / (2 * 4000) )
focusing = gaussian * np.exp(-1j * k/2/z * \
    (np.power(x_arr, 2) + np.power(y_arr, 2)))
sph_ab = focusing * np.exp(-1j * k * 5e-9 * \
    np.power(np.power(x_arr, 2) + np.power(y_arr, 2), 2))

def propagate_field(z_elem, k_xy_field, kz):
    new_k_xy_field = k_xy_field * np.exp(1j * kz * z_elem)
    new_xy_field = ft.fftshift(ft.ifft2(new_k_xy_field))
    return new_xy_field

def get_resolution(correction, do_plot=False):
    xy_field = sph_ab * np.exp(-1j * k * 1e-9 * correction * \
        (np.power(x_arr, 4) + np.power(y_arr, 4)))
    k_xy_field = ft.fft2(ft.ifftshift(xy_field))
    
    kx, ky = np.meshgrid(\
        2 * np.pi * ft.fftfreq(k_xy_field.shape[0], step),\
        2 * np.pi * ft.fftfreq(k_xy_field.shape[1], step))
        
    kz = np.zeros(kx.shape, np.cfloat)
    index1 = np.power(kx, 2) + np.power(ky, 2) <= np.power(k, 2)
    kz[index1] = np.power(np.power(k, 2) - np.power(kx[index1], 2) \
        - np.power(ky[index1], 2), 0.5).astype(np.cfloat)
    index2 = np.power(kx, 2) + np.power(ky, 2) > np.power(k, 2)
    kz[index2] = 1j * np.power(- np.power(k, 2) \
        + np.power(kx[index2], 2) + np.power(ky[index2], 2), 0.5)
    
    new_xyz_fields = [propagate_field(z_elem, k_xy_field, kz) for z_elem in z_arr]
    
    x = x_arr
    y = y_arr
    
    if do_plot:
        plt.subplot(221)
        plt.pcolor(x, y, np.abs(xy_field))
        plt.subplot(222)
        plt.pcolor(ft.fftshift(kx), ft.fftshift(ky), ft.fftshift(np.abs(k_xy_field)))
        plt.subplot(2, 2, (3,4))
        plt.pcolor(x, y, np.abs(new_xyz_fields[0]))
    
    field_max = np.max(np.power(np.abs(new_xyz_fields), 4))
    elem_filter = np.power(np.abs(new_xyz_fields), 4) >= field_max/2
    r_arr = np.sqrt(np.power(x_arr, 2) + np.power(y_arr, 2))
    fwhm_x = 2 * np.max(np.abs(x_arr[np.any(elem_filter, 0)]))
    fwhm_r = 2 * np.max(r_arr[np.any(elem_filter, 0)])
    fwhm_z = 2 * np.max(np.abs(z_arr[np.any(np.any(elem_filter, 1), 1)] - z))
    return (fwhm_x, fwhm_r, fwhm_z)
    
correction = np.linspace(-20,-10,11)
fwhm_x, fwhm_r, fwhm_z = zip(*[get_resolution(c) for c in correction])
plt.hold(True)
plt.plot(correction, fwhm_r)
plt.plot(correction, map(lambda x: x/100, fwhm_z))
plt.hold(False)
plt.ylim((0,10))
print np.min(fwhm_r), np.min(fwhm_z)