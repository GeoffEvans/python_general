import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc
from matplotlib import rcParams as r
r.update({'font.size': 30})
r.update({'figure.autolayout': True})
r.update({'lines.linewidth': 3})

rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)

t_range = np.linspace(-50.01,50,1000)

period = 20.

def get_freq_fun(period, a, b, c=0, d=0):
    def freq(t):
        t_mod = np.mod(t + period/2, period) - period/2
        return a + b * t_mod + c * np.power(t_mod, 2.) + d * np.power(t_mod, 3.)
    
    return freq

freq1 = get_freq_fun(period, 40, 1)
freq2 = get_freq_fun(period, 40, 3, 0)
freq3 = get_freq_fun(period, 40, 1, 0, 0.01)

for item in zip([freq1, freq2, freq3],['r', 'b', 'g']):
    
    plt.figure()
    x_range = np.linspace(-6,6,10) * 1e-3 #12mm
    V = 613 
    op_wav = 800e-3
    f = item[0]
    styl = item[1]    
    
    starts_x = x_range * 1000
    starts_z = -0.1
    
    mid_x = x_range * 1000
    mid_z = 0
    
    end_z = 0.5
    end_x = (x_range + op_wav * f(-x_range/V * 1e6) / V * end_z) * 1000
    
    plt.plot([starts_z, mid_z], [starts_x, mid_x], styl)
    plt.plot([mid_z, end_z], [mid_x, end_x], styl)
    plt.xlabel('z / m')
    plt.ylabel('x / mm')
