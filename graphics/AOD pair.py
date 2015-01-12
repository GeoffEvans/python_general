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

freq1 = get_freq_fun(period, 40, 0.23)
freq2 = get_freq_fun(period, 40, 0.23, 0)


figure()
x_range = np.linspace(-6,6,11) * 1e-3 #12mm
V = 613 
op_wav = 800e-3

starts_x = x_range * 1000
starts_z = -0.1

mid1_x = x_range * 1000
mid1_z = -0.05

mid2_z = 0
mid2_x = (x_range + op_wav * freq1(-x_range/V * 1e6) / V * -mid1_z) * 1000

end_z = 1.1
end_x = (x_range + op_wav * freq1(-x_range/V * 1e6) / V * (end_z - mid1_z) - op_wav * freq2(x_range/V * 1e6) / V * end_z) * 1000

plt.plot([starts_z, mid1_z], [starts_x, mid1_x], 'r')
plt.plot([mid1_z, mid2_z], [mid1_x, mid2_x], 'r')
plt.plot([mid2_z, end_z], [mid2_x, end_x], 'r')
plt.plot([starts_z, mid1_z], [starts_x[5], mid1_x[5]], 'b')
plt.plot([mid1_z, mid2_z], [mid1_x[5], mid2_x[5]], 'b')
plt.plot([mid2_z, end_z], [mid2_x[5], end_x[5]], 'b')
plt.xlabel('z / m')
plt.ylabel('x / mm')
