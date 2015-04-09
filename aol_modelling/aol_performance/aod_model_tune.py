# take the expt data, fit model trnasducer using least squares
# use smoothing splene to join up points
# check second order
import numpy as np
from scipy.constants import pi
from aol_model.ray import Ray
from aol_model.acoustics import Acoustics
import expt_data as data
import aol_model.set_up_utils as setup
import scipy.optimize as opt
import scipy.interpolate as interp

orientation = [0,0,1]
ac_dir = [1,0,0]
ac_power=1.5
order=-1

def efficiency_freq_max(acc_eff, freq, expt_920, expt_800, aod):

    def func(mhz, op_wavelength_vac):
        deg_range =  np.linspace(0.9, 3, 70)
        rad_range = deg_range * pi / 180
        rays = [Ray([0,0,0], [np.sin(ang), 0, np.cos(ang)], op_wavelength_vac) for ang in rad_range]

        acoustics = Acoustics(mhz*1e6, ac_power * acc_eff)
        aod.propagate_ray(rays, [acoustics] * len(rays), order)

        idx = np.argmax([r.energy for r in rays])
        r = rays[idx]
        return (r.energy, r.resc)

    (eff_800, _) = func(freq, 800e-9)
    (eff_920, _) = func(freq, 920e-9)

    return np.sum(np.power(eff_800 - expt_800, 2)) + np.sum(np.power(eff_920 - expt_920, 2))

def fit_points(aod):
    profile = []
    for freq, expt_920, expt_800 in zip(data.freq_wide_new, data.eff_freq_wide_920_1, data.eff_freq_wide_800_1):
        res = opt.fminbound(efficiency_freq_max, 0.0, 1, args=(freq, expt_920, expt_800, aod))
        profile.append(res)
    print profile
    return profile

def fit_points_narrow():
    aod = setup.make_aod_narrow(orientation, ac_dir)
    return fit_points(aod)

def fit_points_wide():
    aod = setup.make_aod_wide(orientation, ac_dir)
    return fit_points(aod)

def fit_splene(profile_points):
    acc_profile = interp.splrep(data.freq_narrow_new, profile_points)
    return acc_profile

def view_acc_profile(profile_points):
    import matplotlib.pyplot as plt
    rng = np.linspace(20, 50, 300)
    eff = get_transducer_eff_func(profile_points)
    plt.plot(rng, eff(rng))

def get_transducer_eff_func(profile_points):
    return lambda freq: interp.splev(freq, fit_splene(profile_points))

if __name__ == '__main__':
    view_acc_profile(fit_points_wide())


