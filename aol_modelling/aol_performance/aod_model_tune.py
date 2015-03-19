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
aod = setup.make_aod_narrow(orientation, ac_dir)
ac_power=1.5
order=-1

def efficiency_freq_max(acc_eff, freq, expt_920, expt_800):

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

def fit_points():
    profile = []
    for freq, expt_920, expt_800 in zip(data.freq_narrow_new, data.eff_freq_narrow_920_1, data.eff_freq_narrow_800_1):
        res = opt.minimize_scalar(efficiency_freq_max, args=(freq, expt_920, expt_800), bounds=(0.4,1))
        profile.append(res.x)
    print profile
    return profile

def fit_splene():
    #profile_points = [0.51881431826297331, 0.54563277527028697, 0.61370347460152419, 0.68000545310886851, 0.6271404013325097, 0.47065260758742261, 0.42424021503614689, 0.48318274174364162, 0.65686287128036835, 0.7719469967251249, 0.81941008497831003, 0.89248388301729809, 0.92488454146740506, 0.90568429358280944, 0.84614669570942136, 0.82345819605853321, 0.80131755161871676, 0.74798408757387858, 0.68946343073870586, 0.65158032453530412]
    profile_points = [0.92783797410438429, 0.91311979456817405, 0.90500665022614346, 0.91349934563092816, 0.92792288662050959, 0.95657310382979777, 0.96685609483056456, 0.97517396991524163, 0.98741269383815766, 0.99424309806874178, 0.99768743961134931, 0.99816360606760868, 0.99790486746739604, 0.99744763980068496, 0.99702660894923345, 0.99632383130520452, 0.99634374228170042, 0.99689566836427745, 0.99844661290532466, 0.99957471302264944]
    acc_profile = interp.splrep(data.freq_narrow_new, profile_points)
    return acc_profile

def view_acc_profile():
    import matplotlib.pyplot as plt
    rng = np.linspace(20, 50, 300)
    eff = get_transducer_eff_func()
    plt.plot(rng, eff(rng))

def get_transducer_eff_func():
    return lambda freq: interp.splev(freq, fit_splene())

if __name__ == '__main__':
    fit_points()
    #view_acc_profile()


