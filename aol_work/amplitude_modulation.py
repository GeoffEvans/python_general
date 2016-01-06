import aol_model.set_up_utils as setup
import numpy as np
from scipy.optimize import minimize_scalar
import matplotlib.pyplot as plt

pdr = 1
op_wavelen = 920e-9
z = 1e9
aol = setup.set_up_aol(op_wavelen, focus_position=[0,0,z], ac_power=[1.5,1.5,1.5,1.5], pair_deflection_ratio=pdr)

def get_average_aod_eff(aol):
    rays = setup.get_ray_bundle(op_wavelen)
    _, effs = aol.propagate_to_distance_past_aol(rays, 0)
    eff_av = np.sum(effs, axis=0) / len(rays)
    aod_eff = eff_av / [1, eff_av[0], eff_av[1], eff_av[2]]
    return aod_eff

eff_ref = get_average_aod_eff(aol)

acceptance_angle = 10e-3

positions = []
p1 = []
p2 = []
es = []
for ang in np.linspace(-1,1.5,15) * acceptance_angle:
    x = ang * z
    power1, power2 = (1.5, 1.5)
    aol = setup.set_up_aol(op_wavelen, focus_position=[x,0,z], ac_power=[1.5,1.5,1.5,1.5], pair_deflection_ratio=pdr)

    def get_x1_power(drive_power_x1):
        aol.acoustic_drives[0].power = drive_power_x1
        eff = get_average_aod_eff(aol)
        return (eff[0] - eff_ref[0])**2

    def get_x2_power(drive_power_x2):
        aol.acoustic_drives[2].power = drive_power_x2
        eff = get_average_aod_eff(aol)
        return (eff[2] - eff_ref[2])**2

    res1 = minimize_scalar(get_x1_power, bounds=(1,4))
    res2 = minimize_scalar(get_x2_power, bounds=(1,4))
    eff = get_average_aod_eff(aol)
    positions.append(ang)
    p1.append(res1.x)
    p2.append(res2.x)
    es.append(np.prod(eff))

plt.plot(positions, p1)
plt.plot(positions, p2)
plt.plot(positions, es)

order = 2
coeffs1 = np.polyfit(positions, p1, order)
coeffs2 = np.polyfit(positions, p2, order)
poly1 = np.poly1d(coeffs1)
poly2 = np.poly1d(coeffs2)

plt.plot(positions, poly1(positions))
plt.plot(positions, poly2(positions))