from __future__ import division
import numpy as np

location = r'C:\Users\Geoff\Python\python_aol_work\aol_modelling\pdr_image_processing\images\pdr%s_expt.npy'
expt_1 = np.load(location % 1)
expt_2 = np.load(location % 0.5)

for val in map(lambda x: x/10, range(3,8)):
    count1 = np.where(expt_1 > val)[0].size
    count2 = np.where(expt_2 > val)[0].size
    improvement = count2 / count1 - 1
    print '%f\t%f' % (val, improvement)
