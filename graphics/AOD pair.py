import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc
rcParams.update({'font.size': 20})
rcParams.update({'figure.autolayout': True})


rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)

t_range = np.linspace(-50.01,50,1000) * 1e-6

period = 20.

def get_freq_fun(period, a, b, c=0, d=0):
    def freq(t):
        t_mod = t#np.mod(t + period/2, period) - period/2
        return a + b * t_mod + c * np.power(t_mod, 2.) + d * np.power(t_mod, 3.)
    
    return freq

ab = [[ 40e6, 40e6], [ -2.23672024e+11, -2.34855625e+11]]
#ab = [[ 36351190.47619048, 43648809.52380952 ], [ -2.23672024e+11, -2.34855625e+11]]
#ab = [[ 40e6, 47662500.], [ -2.23672024e+11, -2.34855625e+11]]
freq1 = lambda t: ab[0][0] + ab[1][0] * t
freq2 = lambda t: ab[0][1] + ab[1][1] * t

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

starts_x = np.linspace(-5,5,5) * 1e-3 #12mm
aod1_x = starts_x 
k, aod2_x = propagate_from_aod(freq1, 1, 0, aod1_x, 0, aod2_z-aod1_z)
k2, end_x = propagate_from_aod(freq2, -1, k, aod2_x, aod2_x[2], end_z-aod2_z)

sty = 'r:'
sty2 = 'r'
plt.plot([starts_z, aod1_z], [starts_x*1e3, aod1_x*1e3], sty)
plt.plot([aod1_z, aod2_z], [aod1_x*1e3, aod2_x*1e3], sty)
plt.plot([aod2_z, end_z], [aod2_x*1e3, end_x*1e3], sty)
plt.plot([starts_z, aod1_z], [starts_x[2]*1e3, aod1_x[2]*1e3], sty2)
plt.plot([aod1_z, aod2_z], [aod1_x[2]*1e3, aod2_x[2]*1e3], sty2)
plt.plot([aod2_z, end_z], [aod2_x[2]*1e3, end_x[2]*1e3], sty2)
plt.xlabel('z / m')
plt.ylabel('x / mm')
