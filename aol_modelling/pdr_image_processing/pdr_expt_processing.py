import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy import misc
from scipy.constants import pi
from scipy import ndimage
import concat_images as cc
from PIL import Image
import aol_model.pointing_efficiency as p

def process_pdr_list():
    file_name = '.\\images\\pdr%s_%s.%s'
    for pdr in [0, 0.1, 0.2, 0.5, 1, 2, 5, -0.1, -0.2, -0.5, -2, -5]:
        expt = get_pdr_expt_images(pdr)
        np.save(file_name % (pdr, 'expt', 'npy'), expt)
        #plt.savefig((file_name % (pdr, 'expt_smooth', 'tif')).replace('-', 'n'), bbox_inches='tight')
        thry = p.plot_fov_surf(1e9, pdr)
        np.save(file_name % (pdr, 'model', 'npy'), thry)
        plt.savefig((file_name % (pdr, 'model', 'tif')).replace('-', 'n'), bbox_inches='tight')
        plt.close('all')

def model_z_stack(pdr):
    file_name = '.\\zstacks\\z%s_pdr%s_model.%s'
    points = [round(2./(n+1e-6), 3) for n in range(-4,6)]
    plt.figure()
    p.plot_peak(points)
    for fl in points:
        thry = p.plot_fov_surf(fl, pdr)
        np.save(file_name % (fl, pdr, 'npy'), thry)
        plt.savefig((file_name % (fl, pdr, 'tif')).replace('-', 'n'), bbox_inches='tight')

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
    plt.locator_params(nbins=5)
    plt.show()

def plot_z_stack_expt(pdr):
    file_name = 'C:\\Users\\Geoff\\Desktop\\PDR expts\\25 Feb 2015\\%s_%s\\Zstack Images\\GreenChannel_00%s.tif'

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    id_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15']
    normalised_zs = [-0.96, -0.8176,-0.7,-0.5231,-0.4,-0.2462,-0.1176,0,0.1173,0.2341,0.3563,0.4765,0.58,0.6941,0.795]
    powers = map(lambda norm_z: 4 * 18e-3 * (norm_z + 1e-9) / 15e-3, normalised_zs)
    rf = 4 #resolution factor
    sf = 0.01 # scale factor
    for [id_str, pwr] in zip(id_list[1:15:2], powers[1:15:2]):
        img_1 = misc.imread(file_name % (pdr, 1, id_str))
        img_2 = misc.imread(file_name % (pdr, 2, id_str))
        img_3 = misc.imread(file_name % (pdr, 3, id_str))
        img_mean = (img_1 + img_2 + img_3) / 3

        img_blur = ndimage.gaussian_filter(img_mean, 2 )
        img_blur -= np.min(img_blur)
        img_blur_norm = img_blur[rf/2::rf, rf/2::rf] * 1.0 / 1160

        print np.max(img_blur)
        anglesx,anglesy = (lambda x: np.meshgrid(x, x))(np.linspace(-36, 36, np.shape(img_blur_norm)[0]) * 1e-3 * 180/pi)
        ax.plot_surface(anglesx, anglesy, img_blur_norm*sf+pwr, rstride=1, cstride=1, cmap=plt.cm.bone, \
                               linewidth=0, antialiased=False, vmax=sf+pwr)

    ax.set_xlim3d(-2, 2)
    ax.set_ylim3d(-2, 2)
    ax.set_zlim3d(-2, 2)

    ax.view_init(elev=10.)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.locator_params(nbins=5)
    plt.show()

def plot_z_eff(pdr):
    file_name = 'C:\\Users\\Geoff\\Desktop\\PDR expts\\25 Feb 2015\\%s_%s\\Zstack Images\\GreenChannel_00%s.tif'

    id_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15']
    normalised_zs = [-0.96, -0.8176,-0.7,-0.5231,-0.4,-0.2462,-0.1176,0,0.1173,0.2341,0.3563,0.4765,0.58,0.6941,0.795]
    powers = map(lambda norm_z: 4 * 18e-3 * (norm_z + 1e-9) / 15e-3, normalised_zs)

    maxes = []
    for [id_str, pwr] in zip(id_list, powers):
        img_1 = misc.imread(file_name % (pdr, 1, id_str))
        img_2 = misc.imread(file_name % (pdr, 2, id_str))
        img_3 = misc.imread(file_name % (pdr, 3, id_str))
        img_mean = (img_1 + img_2 + img_3) / 3

        img_blur = ndimage.gaussian_filter(img_mean, 2 )
        img_blur -= np.min(img_blur)
        maxes.append(np.max(img_blur))

    labels = ["1/z / 1/m", "efficiency"]
    plt.plot(powers, np.array(maxes) * 1./max(maxes), 'o', label=labels, marker='x')
    plt.show()

def plot_z_eff_near1():
    file_name = 'C:\\Users\\Geoff\\Desktop\\PDR expts\\25 Feb 2015\\%s_%s\\Zstack Images\\GreenChannel_00%s.tif'

    id_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21']
    normalised_zs = [-0.3231,-0.2846,-0.2462,-0.2077,-0.1765,-0.1471,-0.1176,-0.0882,-0.0588,-0.0294,0,0.0294,0.0588,0.0882,0.1173,0.1462,0.1751,0.2042,0.2341,0.2641,0.294]
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

def plot_z_eff_near2():
    file_name = 'C:\\Users\\Geoff\\Desktop\\PDR expts\\25 Feb 2015\\%s_%s\\Zstack Images\\GreenChannel_00%s.tif'

    id_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21']
    normalised_zs = [-0.0588,-0.0529,-0.0471,-0.0412,-0.0353,-0.0294,-0.0235,-0.0176,-0.0118,-0.0059,0,0.0059,0.0118,0.0176,0.0235,0.0294,0.0353,0.0412,0.0471,0.0529,0.0588]
    powers = map(lambda norm_z: 4 * 18e-3 * (norm_z + 1e-9) / 15e-3, normalised_zs)

    maxes = []
    for [id_str, pwr] in zip(id_list, powers):
        img_1 = misc.imread(file_name % ('000', 1, id_str))
        img_2 = misc.imread(file_name % ('000', 2, id_str))
        img_3 = misc.imread(file_name % ('000', 3, id_str))
        img_mean = (img_1 + img_2 + img_3) / 3

        img_blur = ndimage.gaussian_filter(img_mean, 2 )
        img_blur -= np.min(img_blur)
        maxes.append(np.max(img_blur))

    labels = ["1/z / 1/m", "efficiency"]
    plt.plot(powers, np.array(maxes) * 1./max(maxes), 'o', label=labels, marker='x')
    plt.show()

def post_process_pdr_list():
    for pdr in [0, 0.1, 0.2, 0.5, 1, 2, 5, -0.1, -0.2, -0.5, -2, -5]:
        get_pdr_expt_images(pdr)
        plt.savefig(('.\\images\\pdr%s_exp_smooth.svg' % pdr).replace('-', 'n'), bbox_inches='tight')
        thry = np.load('.\\images\\pdr%s_model.npy' % pdr)
        description = 'Model for PDR %s' % pdr
        p.generate_plot(thry, thry, description)
        plt.savefig(('.\\images\\pdr%s_model.svg' % pdr).replace('-', 'n'), bbox_inches='tight')
        plt.close('all')

def get_pdr_expt_images(pdr):
    pdrn = str(pdr).replace('-', 'n')
    img = misc.imread('C:\\Users\\Geoff\\Desktop\\PDR expts\\26 Jan 15\\pdr%slambda920acc18.png' % pdrn)
    img_2 = misc.imread('C:\\Users\\Geoff\\Desktop\\PDR expts\\26 Jan 15\\pdr%slambda920acc18_2.png' % pdrn)
    img_3 = misc.imread('C:\\Users\\Geoff\\Desktop\\PDR expts\\26 Jan 15\\pdr%slambda920acc18_3.png' % pdrn)
    img_mean = (img + img_2 + img_3) / 3

    img_blur = ndimage.gaussian_filter(img_mean, 2 )
    img_blur -= np.min(img_blur)
    img_blur_norm = img_blur * 1. / np.max(img_blur)

    description = 'Expt for PDR %s' % pdr
    p.generate_plot(img_blur, img_blur_norm, description)
    return img_blur_norm

def create_line_of_expt_images():
    pdr_list = [-5, -2, -0.5, -0.2, -0.1, 0, 0.1, 0.2, 0.5, 1, 2, 5]

    image_list = []
    for pdr in pdr_list:
        img = Image.open(('C:\\Users\\Geoff\\Desktop\\PDR expts\\26 Jan 15\\pdr%slambda920acc18.png' % pdr).replace('-', 'n'))
        image_list.append(img)

    result = cc.join_horizontally(image_list, img.mode)
    result.save('C:\\Users\\Geoff\\Desktop\\PDR expts\\26 Jan 15\\line_expt.tif')

def create_line_of_e_vs_t_images():
    pdr_groups = [[5, 2, 1, 0.5], [0, -0.5, -2, -5]]

    vimg= []
    for pdr_list in pdr_groups:
        images = []
        for pdr in pdr_list:
            image1 = Image.open(('C:\\Users\\Geoff\\eclipse\\python_aol_model\\image_processing\\images\\pdr%s_exp_smooth.svg' % pdr).replace('-', 'n'))
            image2 = Image.open(('C:\\Users\\Geoff\\eclipse\\python_aol_model\\image_processing\\images\\pdr%s_model.svg' % pdr).replace('-', 'n'))
            images.append(cc.join_vertically([image1, image2], image1.mode))

        vimg.append(cc.join_horizontally(images, image1.mode))
    result = cc.join_vertically(vimg, image1.mode)
    result.save('C:\\Users\\Geoff\\eclipse\\python_aol_model\\image_processing\\images\\line_expt_vs_theory.svg')

if __name__ == '__main__':
    #post_process_pdr_list()
    #create_line_of_e_vs_t_images()
    #plot_z_stack_thry(1)
    #plot_z_stack_expt(1)
    #plot_z_stack_expt(0)
    plot_z_eff(1)
    plot_z_eff(0)
    p.plot_peak(-1./np.linspace(-4,5))
    plot_z_eff_near1()
    plot_z_eff_near2()