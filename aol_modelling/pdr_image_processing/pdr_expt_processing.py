import matplotlib.pyplot as plt
import numpy as np
from scipy import misc
from scipy import ndimage
import concat_images as cc
from PIL import Image
import aol_model.pointing_efficiency as p
from scipy.constants import pi

pdr_list = [-5, -2, -0.5, -0.2, -0.1, 0, 0.1, 0.2, 0.5, 1, 2, 5]

def calc_and_save_data_for_pdr_list():
    file_name = '.\\images\\pdr%s_%s.%s'
    for pdr in pdr_list:
        expt = get_pdr_expt_image_data(pdr)
        np.save(file_name % (pdr, 'expt', 'npy'), expt)
        thry = p.calc_fov_surf_data(1e9, pdr)
        np.save(file_name % (pdr, 'model', 'npy'), thry)

def plot_and_save_images_for_pdr_list():
    for pdr in pdr_list:
        expt = np.load('.\\images\\pdr%s_expt.npy' % pdr)
        description = 'Expt for PDR %s' % pdr
        p.generate_plot(expt, description, pdr)
        plt.savefig(('.\\images\\pdr%s_exp_smooth.tif' % pdr).replace('-', 'n'), bbox_inches='tight')

        thry = np.load('.\\images\\pdr%s_model.npy' % pdr)
        description = 'Model for PDR %s' % pdr
        p.generate_plot(thry, description, pdr)
        plt.savefig(('.\\images\\pdr%s_model.tif' % pdr).replace('-', 'n'), bbox_inches='tight')

        #plt.close('all')

def get_pdr_expt_image_data(pdr):
    pdrn = str(pdr).replace('-', 'n')
    img = misc.imread('C:\\Users\\Geoff\\Desktop\\PDR expts\\26 Jan 15\\pdr%slambda920acc18.png' % pdrn)
    img_2 = misc.imread('C:\\Users\\Geoff\\Desktop\\PDR expts\\26 Jan 15\\pdr%slambda920acc18_2.png' % pdrn)
    img_3 = misc.imread('C:\\Users\\Geoff\\Desktop\\PDR expts\\26 Jan 15\\pdr%slambda920acc18_3.png' % pdrn)
    img_mean = (img + img_2 + img_3) / 3

    img_blur = ndimage.gaussian_filter(img_mean, 2 )
    img_blur -= np.min(img_blur)
    img_blur_norm = img_blur * 1. / np.max(img_blur)
    return img_blur_norm

def create_line_of_expt_images():

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
            image1 = Image.open(('.\\images\\pdr%s_exp_smooth.tif' % pdr).replace('-', 'n'))
            image2 = Image.open(('.\\images\\pdr%s_model.tif' % pdr).replace('-', 'n'))
            images.append(cc.join_vertically([image1, image2], image1.mode))

        vimg.append(cc.join_horizontally(images, image1.mode))
    result = cc.join_vertically(vimg, image1.mode)
    result.save('.\\images\\line_expt_vs_theory.tif')

if __name__ == '__main__':
    #calc_and_save_data_for_pdr_list()
    plot_and_save_images_for_pdr_list()
    #create_line_of_e_vs_t_images()
