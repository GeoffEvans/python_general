import matplotlib.pyplot as plt
import numpy as np
from scipy import misc
from scipy import ndimage
from PIL import Image
from matplotlib import rcParams as r
r.update({'font.size': 24})

def calc_image_vol(pdr):
    pdrn = str(pdr).replace('-', 'n')
    path = 'C:\\Users\\Geoff\\Desktop\\pdr_data\\%s_%s\\Zstack Images\\GreenChannel_00%s.tif'
    stack = np.zeros((33,200,200), dtype=np.float)
    for num in range(1,34):
        imgnum = "%02d" % (num,)
        img_1 = misc.imread(path % (pdrn, 1, imgnum))
        img_2 = misc.imread(path % (pdrn, 2, imgnum))
        img_3 = misc.imread(path % (pdrn, 3, imgnum))
        stack[num-1] = ndimage.gaussian_filter((img_1 + img_2 + img_3) * 1.0 / 3, 1)

    stack_min = np.min(stack)
    stack -= stack_min
    stack_max = np.max(stack)
    print (pdr, stack_max, stack_min)
    stack_norm = stack * 1. / stack_max
    count = []
    for n in [6]:
        val = n*0.1
        count.append(np.where(stack_norm > val)[0].size)
    return count


if __name__ == '__main__':
    counts = []
    pdr_list = [5, 3, 2, 1, 0.5, 0.3, 0.1, 0, -0.2, -0.5, -0.8, -2, -3]
    for pdr in pdr_list:
        counts.append(calc_image_vol(pdr))

    vals = np.transpose(counts)
    max_val = np.max(vals)
    plt.figure()
    for n in range(1):
        plt.plot(pdr_list, vals[n]*1./max_val, 'ro', markersize=10)
    plt.grid()
    plt.xlabel('PDR')
    plt.ylabel('Normalised Imaging Volume')
    plt.grid()
