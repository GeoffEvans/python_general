import matplotlib.pyplot as plt
import numpy as np
from scipy import misc
from scipy import ndimage
from mpl_toolkits.mplot3d import Axes3D
from scipy.constants import pi
from matplotlib import rcParams

rcParams.update({'lines.linewidth': 3})
rcParams.update({'font.size': 20})
rcParams['svg.fonttype'] = 'none' # No text as paths. Assume font installed.
rcParams['font.serif'] = ['Times New Roman']
rcParams['font.sans-serif'] = ['Arial']
rcParams['font.family'] = 'sans-serif'
rcParams.update({'figure.autolayout': True})

def plot_z_stack_expt(pdr):
    file_name = 'C:\\Users\\Geoff\\Desktop\\pdr_data\\%s_%s\\Zstack Images\\GreenChannel_00%s.tif'

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    id_list = ['08', '11', '14', '17', '20', '23', '26']
    abs_zs = np.array([-90,-60,-30,0,30,60,90]) * 4
    rf = 4 #resolution factor
    sf = 0.01 # scale factor
    array3d = []
    max_img = { 0.3 : 881, 5: 957, -2 : 878, -0.8 : 636, -0.5 : 785, -3 : 911}
    for [id_str, pwr] in zip(id_list, abs_zs):
        pdrn = str(pdr).replace('-', 'n')
        img_1 = misc.imread(file_name % (pdrn, 1, id_str))
        img_2 = misc.imread(file_name % (pdrn, 2, id_str))
        img_3 = misc.imread(file_name % (pdrn, 3, id_str))
        img_mean = (img_1 + img_2 + img_3) / 3

        img_blur = ndimage.gaussian_filter(img_mean, 2 )
        img_blur -= np.min(img_blur)
        img_blur_norm = img_blur[rf/2::rf, rf/2::rf] * 1.0 / max_img[pdr]

        array3d.append(img_blur_norm)
        x,y = (lambda x: np.meshgrid(x, x))(np.linspace(-36, 36, np.shape(img_blur_norm)[0]) * 1e-3 * 9e3)
        ax.plot_surface(x[10:40,10:40], y[10:40,10:40], img_blur_norm[10:40,10:40]*sf+pwr, rstride=1, cstride=1, cmap=plt.cm.bone, \
                               linewidth=0, antialiased=False, vmax=sf+pwr, rasterized=True)
        #ax.contour(x[10:40,10:40], y[10:40,10:40], img_blur_norm[10:40,10:40]*sf+pwr)

    x_max = 200
    z_max = 400
    ax.set_xlim3d(-x_max, x_max)
    ax.set_ylim3d(-x_max, x_max)
    ax.set_zlim3d(-z_max, z_max)
    ax.xaxis.set_ticks([])

    ax.yaxis.set_ticks([])
    ax.set_yticklabels([-x_max, 0, x_max], verticalalignment='center', horizontalalignment='left')
    ax.zaxis.set_ticks([])
    ax.zaxis.set_ticklabels([-z_max, 0, z_max], verticalalignment='bottom', horizontalalignment='left')

    ax.view_init(elev=10.)
    #plt.xlabel('$x_M / \\mu$m')
    #ax.xaxis._axinfo['label']['space_factor'] = 2.
    #plt.ylabel('$y_M / \\mu$m')
    #ax.yaxis._axinfo['label']['space_factor'] = 2.
    #ax.set_zlabel('$z_M / \\mu$m')
    plt.show()
    print np.max(np.array(array3d))

if __name__ == '__main__':
    plot_z_stack_expt(-2)
    plot_z_stack_expt(0.3)
    plot_z_stack_expt(5)