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

def get_freq_fun(a, b, c=0, d=0):
    period = 20e-6
    a = a/1e6    
    b = b/1e6
    def freq(t):
        t_mod = np.mod(t + period/2, period) - period/2
        return a + b * t_mod + c * np.power(t_mod, 2.) + d * np.power(t_mod, 3.)
    
    return freq

linesty = ['b:', 'r', 'g--', 'k-.']

a_x0_z1 = [ 40000000.,  40000000.,  40000000.,  40000000.]
b_x0_z1 = [ -2.16134196e+11,  -2.25588528e+11,  -2.25588528e+11, -2.35907816e+11]

a_x0o01_z1_pdr1 = [ 36474156.6765482,  40000000.       ,  43525843.3234518,  40000000.       ]
b_x0o01_z1_pdr1 = [ -2.16134196e+11,  -2.25588528e+11,  -2.25588528e+11, -2.35907816e+11]

a_x0o01_z1_pdr0 = [ 40000000. ,  40000000. , 47360147.73635266, 40000000.]
b_x0o01_z1_pdr0 = [ -2.16134196e+11, -2.25588528e+11, -2.25588528e+11, -2.35907816e+11]

freqs = map(get_freq_fun, a_x0o01_z1_pdr0, b_x0o01_z1_pdr0)

plt.figure()
for pair in zip(freqs, linesty):
    plt.plot(t_range, pair[0](t_range/1e6), pair[1])

plt.xlabel(r'time / $\mu$s')
plt.ylabel('frequency / MHz')
plt.axis([-50, 50, 30, 50])
plt.show()
