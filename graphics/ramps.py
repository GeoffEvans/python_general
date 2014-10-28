import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc
rcParams.update({'font.size': 20})
rcParams.update({'figure.autolayout': True})


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
plt.plot(t_range, freq1(t_range),'r')
plt.plot(t_range, freq2(t_range),'b:')
plt.plot(t_range, freq3(t_range),'g--')
plt.xlabel(r'time / $\mu$s')
plt.ylabel('frequency / MHz')
plt.axis([-50, 50, 0, 80])