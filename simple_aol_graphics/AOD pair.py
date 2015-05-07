import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
rcParams.update({'lines.linewidth': 3})
rcParams.update({'font.size': 20})
rcParams['svg.fonttype'] = 'none' # No text as paths. Assume font installed.
rcParams['font.serif'] = ['Times New Roman']
rcParams['font.sans-serif'] = ['Arial']
rcParams['font.family'] = 'sans-serif'

t_range = np.linspace(-50.01,50,1000) * 1e-6

period = 20.

def get_freq_fun(period, a, b, c=0, d=0):
    def freq(t):
        t_mod = t#np.mod(t + period/2, period) - period/2
        return a + b * t_mod + c * np.power(t_mod, 2.) + d * np.power(t_mod, 3.)

    return freq

ab1 = [[ 40e6, 40e6], [ -2.23672024e+11, -2.34855625e+11]]
ab2 = [[ 36351190.47619048, 43648809.52380952 ], [ -2.23672024e+11, -2.34855625e+11]]
ab3 = [[ 40e6, 47662500.], [ -2.23672024e+11, -2.34855625e+11]]

V = 613
op_wav = 800e-9

def propagate_from_aod(f, K, k_in, x_in, x_offset, z):
    k_out = k_in - K * op_wav * f(-K * (x_in - x_offset) / V) / V
    x_out = x_in + z * k_out
    return (k_out, x_out)

starts_z = -0.2
aod1_z = -0.1
aod2_z = 0
end_z = 1

def shift_x(x):
    return map(lambda q: q*1e3 + 5.2, x)

for ab in zip([ab3, ab2, ab1], ['g', 'b', 'r']):

    freq1 = lambda t: ab[0][0][0] + ab[0][1][0] * t
    freq2 = lambda t: ab[0][0][1] + ab[0][1][1] * t

    starts_x = np.linspace(-5,5,5) * 1e-3 #12mm
    aod1_x = starts_x
    k, aod2_x = propagate_from_aod(freq1, 1, 0, aod1_x, 0, aod2_z-aod1_z)
    k2, end_x = propagate_from_aod(freq2, -1, k, aod2_x, aod2_x[2], end_z-aod2_z)

    sty = ab[1] + ':'
    sty2 = ab[1]
    plt.plot([starts_z, aod1_z], shift_x([starts_x, aod1_x]), sty)
    plt.plot([aod1_z, aod2_z], shift_x([aod1_x, aod2_x]), sty)
    plt.plot([aod2_z, end_z], shift_x([aod2_x, end_x]), sty)
    plt.plot([starts_z, aod1_z], shift_x([starts_x[2], aod1_x[2]]), sty2)
    plt.plot([aod1_z, aod2_z], shift_x([aod1_x[2], aod2_x[2]]), sty2)
    plt.plot([aod2_z, end_z], shift_x([aod2_x[2], end_x[2]]), sty2)

plt.xlabel('z (m)')
plt.ylabel('x (mm)')
plt.tick_params(direction='out')
plt.xticks([0,0.5,1])
plt.yticks([-5,0,5,10])