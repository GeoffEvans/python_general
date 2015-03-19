from aol_model.aod_visualisation import AodVisualisation
from aol_model.vector_utils import normalise
import expt_data as d
import matplotlib.pyplot as plt

av_wide = AodVisualisation(785e-9, ac_dir_rel=[1,0,0], is_wide=True, deg_bnds=(-1,4))
av_narrow = AodVisualisation(785e-9, ac_dir_rel=normalise([1,0,0]), is_wide=False, deg_bnds=(-1,6))
av_narrow_800 = AodVisualisation(800e-9, ac_dir_rel=normalise([1,0,0]), is_wide=False, deg_bnds=(-1,6))
av_narrow_920 = AodVisualisation(920e-9, ac_dir_rel=normalise([1,0,0]), is_wide=False, deg_bnds=(-1,6))

def plot_eff_pwr_wide():
    plt.plot(d.power, d.eff_power_wide, 'ro')
    av_wide.plot_efficiency_power()

def plot_eff_freq_wide():
    plt.plot(d.freq_wide, d.eff_freq_wide, 'ro')
    av_wide.plot_efficiency_freq_max()

def plot_eff_ang_wide():
    plt.plot(d.angle_wide, d.eff_angle_wide, 'ro')
    av_wide.plot_efficiency_xangle()

def plot_eff_pwr_narrow():
    plt.plot(d.power, d.eff_power_narrow, 'ro')
    av_narrow.plot_efficiency_power()

def plot_eff_freq_narrow():
    plt.plot(d.freq_narrow, d.eff_freq_narrow, 'ro')
    av_narrow.plot_efficiency_freq_max()

def plot_eff_ang_narrow():
    plt.plot(d.angle_narrow, d.eff_angle_narrow, 'ro')
    av_narrow.plot_efficiency_xangle()

def plot_eff_freq_narrow_920():
    #plt.plot(d.freq_narrow_920, d.eff_freq_narrow_920_12, 'go')
    plt.plot(d.freq_narrow_new, d.eff_freq_narrow_920_1, 'bo')
    plt.plot(d.freq_narrow_new, d.eff_freq_narrow_920_2, 'ro')
    av_narrow_920.plot_efficiency_freq_max()

def plot_eff_freq_narrow_800():
    #plt.plot(d.freq_narrow_920, d.eff_freq_narrow_800_12, 'yo')
    plt.plot(d.freq_narrow_new, d.eff_freq_narrow_800_1, 'co')
    plt.plot(d.freq_narrow_new, d.eff_freq_narrow_800_23, 'mo')
    av_narrow_800.plot_efficiency_freq_max()

if __name__ == '__main__':
    plot_eff_freq_narrow_920()
    plot_eff_freq_narrow_800()
    #plt.figure()
    #plot_eff_freq_narrow()
    #plt.figure()
    #plot_eff_freq_wide()
    #plt.figure()
    #plot_eff_ang_narrow()
    #plt.figure()
    #plot_eff_ang_wide()
    #plt.figure()
    #plot_eff_pwr_narrow()
    #plt.figure()
    #plot_eff_pwr_wide()
