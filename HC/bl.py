import numpy as np
import matplotlib.pyplot as plt
import numpy.random as rnd

def propagator(num_paths, time_steps, time_increment, x_vals, t):
    propagator_unnormalised = [path_integral(num_paths, time_steps, time_increment, x, 0, x, t) for x in x_vals]
    return np.array(propagator_unnormalised) / np.sum(propagator_unnormalised) * (max(x_vals) - min(x_vals)) / len(x_vals)

def path_integral(num_paths, time_steps, time_increment, start_x, start_t, stop_x, stop_t):
    paths = get_random_paths(num_paths, time_steps, start_x, stop_x)
    phasors_for_paths = [phasor(p, time_increment) for p in paths]
    return np.sum(phasors_for_paths)

def get_random_paths(num_paths, time_steps, start_x, stop_x):
    paths = (rnd.random((num_paths, time_steps)) - 0.5) * 4
    paths[:,0] = start_x
    paths[:,-1] = stop_x
    return paths
    
def phasor(path, time_increment):
    energy = energy_of_path(path, time_increment)
    exp = np.exp(- time_increment * energy)
    return exp
  
def energy_of_path(path, time_increment):
    path_ahead = path[1:]
    path = path[:-1]
    energies = [step_energy(p,pa) for (p,pa) in zip(path, path_ahead)]
    return np.sum(energies)
    
def step_energy(p1, p2):
    return 0.5 / time_increment**2 * (p2 - p1)**2 + 0.5 * (0.5 * (p2 + p1))**2
 
if __name__ == '__main__':
    num_paths = 80000
    time_steps = 7    
    t = 4.
    time_increment = t/time_steps
    x_vals = np.linspace(-2, 2, 15)
    
    plt.plot(x_vals, propagator(num_paths, time_steps, time_increment, x_vals, t))
    plt.show()