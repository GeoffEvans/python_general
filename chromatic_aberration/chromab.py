import numpy as np
from scipy.constants import c
import matplotlib.pyplot as plt

ac_vel = 613
wavelength = 800e-9
focal_length = np.linspace(-100, 100) * 1e-6
angular_range = np.linspace(-1, 1) * 6.8 * 2 * 1e-6 # 300um
lateral_range = np.linspace(-120, 120) * 1e-6

# time-bandwidth uncertainty Dt Df = 1/4pi, pulse width 140e-15

frequency_fwhm = 2.3e12
wavelength_fwhm = frequency_fwhm * wavelength**2 / c    # fl = c, dl = -df * l**2 / c

focal_fwhm = focal_length / wavelength * wavelength_fwhm
angular_fwhm = lateral_range / wavelength * wavelength_fwhm

focal_quad = np.sqrt(4.7e-6 ** 2 + focal_fwhm ** 2)
focal_quad2 = np.sqrt(4.3e-6 ** 2 + focal_fwhm ** 2 + ((focal_length/70e-3)**2 + 2e-6) ** 2)
angular_quad = np.sqrt(0.7e-6 ** 2 + angular_fwhm ** 2)

fig = plt.figure()
plt.plot(lateral_range * 1e6, angular_quad * 1e6)
fig.axes[0].set_ylim([0, 10])
plt.hold(True)
plt.plot(focal_length * 1e6, focal_quad * 1e6)
plt.plot(focal_length * 1e6, focal_quad2 * 1e6)
plt.legend(['lateral', 'axial', 'axial with spherical'])
plt.show()
