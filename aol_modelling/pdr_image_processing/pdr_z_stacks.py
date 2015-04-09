import matplotlib.pyplot as plt
import numpy as np
from scipy import misc
from scipy import ndimage
from mpl_toolkits.mplot3d import Axes3D
from scipy.constants import pi

def plot_z_stack_thry(pdr):
    file_name = '.\\zstacks\\z%s_pdr%s_model.%s'
    powers = range(-2,3)
    points = [round(1./(n+0.5e-6), 3) for n in powers]

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    sf = 0.01 # scale factor
    for fl, pwr in zip(points, powers):
        thry = np.load(file_name % (fl, pdr, 'npy'))
        print np.max(thry)
        anglesx,anglesy = (lambda x: np.meshgrid(x, x))(np.linspace(-36, 36, np.shape(thry)[0]) * 1e-3 * 180/pi)
        ax.plot_surface(anglesx, anglesy, thry*sf+pwr, rstride=1, cstride=1, cmap=plt.cm.bone, \
                               linewidth=0, antialiased=False, vmax=sf+pwr)

    ax.set_xlim3d(-2, 2)
    ax.set_ylim3d(-2, 2)
    ax.set_zlim3d(-2, 2)

    ax.view_init(elev=10.)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.zlabel('z')
    plt.locator_params(nbins=5)
    plt.show()

def plot_z_stack_expt(pdr):
    file_name = 'C:\\Users\\Geoff\\Dropbox\\Expts\\PDR expts\\25 Feb 2015\\%s_%s\\Zstack Images\\GreenChannel_00%s.tif'

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    id_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15']
    normalised_zs = [-0.96, -0.8176,-0.7,-0.5231,-0.4,-0.2462,-0.1176,0,0.1173,0.2341,0.3563,0.4765,0.58,0.6941,0.795]
    abs_zs = np.array([140,120,100,80,60,40,20,0,-20,-40,-60,-80,-100,-120,-140]) * 4
    max_img = {0 : 1000, 1: 1160}
    powers = map(lambda norm_z: 4 * 18e-3 * (norm_z + 1e-9) / 15e-3, normalised_zs)
    rf = 4 #resolution factor
    sf = 0.01 # scale factor
    array3d = []
    for [id_str, pwr] in zip(id_list[5:10:1], abs_zs[5:10:1]):
        img_1 = misc.imread(file_name % (pdr, 1, id_str))
        img_2 = misc.imread(file_name % (pdr, 2, id_str))
        img_3 = misc.imread(file_name % (pdr, 3, id_str))
        img_mean = (img_1 + img_2 + img_3) / 3

        img_blur = ndimage.gaussian_filter(img_mean, 2 )
        img_blur -= np.min(img_blur)
        img_blur_norm = img_blur[rf/2::rf, rf/2::rf] * 1.0 / max_img[pdr]

        array3d.append(img_blur_norm)
        x,y = (lambda x: np.meshgrid(x, x))(np.linspace(-36, 36, np.shape(img_blur_norm)[0]) * 1e-3 * 9e3)
        ax.plot_surface(x, y, img_blur_norm*sf+pwr, rstride=1, cstride=1, cmap=plt.cm.bone, \
                               linewidth=0, antialiased=False, vmax=sf+pwr)

    x_max = 320
    ax.set_xlim3d(-x_max, x_max)
    ax.set_ylim3d(-x_max, x_max)
    ax.set_zlim3d(-160, 160)
    ax.xaxis.set_ticks(np.linspace(-x_max, x_max, 3))

    ax.yaxis.set_ticks(np.linspace(-x_max, x_max, 3))
    ax.set_yticklabels([-x_max, 0, x_max], verticalalignment='center', horizontalalignment='left')
    ax.zaxis.set_ticks(np.linspace(-160, 160, 3))
    ax.zaxis.set_ticklabels([-160, 0, 160], verticalalignment='bottom', horizontalalignment='left')

    ax.view_init(elev=10.)
    plt.xlabel('x / $\\mu$m')
    ax.xaxis._axinfo['label']['space_factor'] = 2.
    plt.ylabel('y / $\\mu$m')
    ax.yaxis._axinfo['label']['space_factor'] = 2.
    ax.set_zlabel('z / $\\mu$m')
    plt.show()
    print np.max(np.array(array3d))

def plot_multiple_z_eff():
    file_name = 'C:\\Users\\Geoff\\Dropbox\\Expts\\PDR expts\\25 Feb 2015\\%s_%s\\Zstack Images\\GreenChannel_00%s.tif'
    id_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15']
    normalised_zs = [-0.96, -0.8176,-0.7,-0.5231,-0.4,-0.2462,-0.1176,0,0.1173,0.2341,0.3563,0.4765,0.58,0.6941,0.795]
    pdr = 0
    plot_z_eff(file_name, pdr, id_list, normalised_zs)
    pdr = 1
    plot_z_eff(file_name, pdr, id_list, normalised_zs)

    file_name = 'C:\\Users\\Geoff\\Dropbox\\Expts\\PDR expts\\25 Feb 2015\\%s_%s\\Zstack Images\\GreenChannel_00%s.tif'
    id_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21']
    normalised_zs = [-0.3231,-0.2846,-0.2462,-0.2077,-0.1765,-0.1471,-0.1176,-0.0882,-0.0588,-0.0294,0,0.0294,0.0588,0.0882,0.1173,0.1462,0.1751,0.2042,0.2341,0.2641,0.294]
    pdr = '00'
    plot_z_eff(file_name, pdr, id_list, normalised_zs)

    file_name = 'C:\\Users\\Geoff\\Dropbox\\Expts\\PDR expts\\25 Feb 2015\\%s_%s\\Zstack Images\\GreenChannel_00%s.tif'
    id_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21']
    normalised_zs = [-0.0588,-0.0529,-0.0471,-0.0412,-0.0353,-0.0294,-0.0235,-0.0176,-0.0118,-0.0059,0,0.0059,0.0118,0.0176,0.0235,0.0294,0.0353,0.0412,0.0471,0.0529,0.0588]
    pdr = '000'
    plot_z_eff(file_name, pdr, id_list, normalised_zs)

def plot_z_eff(file_name, pdr, id_list, normalised_zs):

    powers = map(lambda norm_z: 4 * 18e-3 * (norm_z + 1e-9) / 15e-3, normalised_zs)

    maxes = []
    for [id_str, pwr] in zip(id_list, powers):
        img_1 = misc.imread(file_name % ('00', 1, id_str))
        img_2 = misc.imread(file_name % ('00', 2, id_str))
        img_3 = misc.imread(file_name % ('00', 3, id_str))
        img_mean = (img_1 + img_2 + img_3) / 3

        img_blur = ndimage.gaussian_filter(img_mean, 2 )
        img_blur -= np.min(img_blur)
        maxes.append(np.max(img_blur))

    labels = ["1/z / 1/m", "efficiency"]
    plt.plot(powers, np.array(maxes) * 1./max(maxes), 'o', label=labels, marker='x')
    plt.show()

if __name__ == '__main__':
    plot_z_stack_expt(1)
    plot_z_stack_expt(0)