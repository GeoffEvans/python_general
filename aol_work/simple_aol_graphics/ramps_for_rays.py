import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc
from matplotlib import rcParams
rcParams.update({'lines.linewidth': 5})
rcParams.update({'font.size': 20})
rcParams['svg.fonttype'] = 'none' # No text as paths. Assume font installed.
rcParams['font.serif'] = ['Times New Roman']
rcParams['font.sans-serif'] = ['Arial']
rcParams['font.family'] = 'sans-serif'

def get_freq_fun(t_list, a, b, c=0, d=0):
    period = 20
    t_mod = np.mod(np.array(t_list) + period/2, period) - period/2
    t_mod[np.logical_or(t_mod == period/2, t_mod == -period/2)] = 0
    freqs = a + b * t_mod + c * np.power(t_mod, 2.) + d * np.power(t_mod, 3.) 
    return freqs

t_range = np.linspace(-30,-10,1000)
freqs = get_freq_fun(t_range, 40, 1)
plt.plot(t_range, freqs, 'r')

t_range = np.linspace(-10,10,1000)
freqs = get_freq_fun(t_range, 40, 3)
plt.plot(t_range, freqs, 'b')

t_range = np.linspace(10,30,1000)
freqs = get_freq_fun(t_range, 40, 1, 0, 0.01)
plt.plot(t_range, freqs, 'g')

plt.xlabel(r'time ($\mu$s)')
plt.ylabel('frequency (MHz)')
plt.axis([-31, 31, 0, 80])
plt.xticks([-30,0,30])
plt.tick_params(direction='out')
plt.show()

