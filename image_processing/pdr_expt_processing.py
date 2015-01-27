import numpy as np
from scipy import misc
from scipy import ndimage
import concat_images as cc
from PIL import Image
import pointing_efficiency as p

def process_pdr_list():
    for pdr in [0, 0.1, 0.2, 0.5, 1, 2, 5, -0.1, -0.2, -0.5, -2, -5]:
        #get_pdr_expt_images(pdr)
        #plt.savefig(('.\\images\\pdr%s_exp.tif' % pdr).replace('-', 'n'), bbox_inches='tight')
        p.plot_fov_surf(1e9, pdr)
        p.plt.savefig(('.\\images\\pdr%s_model.tif' % pdr).replace('-', 'n'), bbox_inches='tight')        

def get_pdr_expt_images(pdr):
    pdrn = str(pdr).replace('-', 'n')
    img = misc.imread('C:\\Users\\Geoff\\Desktop\\PDR expts\\26 Jan 15\\pdr%slambda920acc18.png' % pdrn)
    img_2 = misc.imread('C:\\Users\\Geoff\\Desktop\\PDR expts\\26 Jan 15\\pdr%slambda920acc18_2.png' % pdrn)
    img_3 = misc.imread('C:\\Users\\Geoff\\Desktop\\PDR expts\\26 Jan 15\\pdr%slambda920acc18_3.png' % pdrn)
    img_mean = (img + img_2 + img_3) / 3     

    img_blur = ndimage.gaussian_filter(img_mean, 2 )
    img_blur -= np.min(img_blur)
    img_blur_norm = img_blur * 1. / np.max(img_blur)           

    description = 'Experiment for PDR %s' % pdr
    p.generate_plot(img, img_blur_norm, description)

def create_line_of_expt_images():
    pdr_list = [-5, -2, -0.5, -0.2, -0.1, 0, 0.1, 0.2, 0.5, 1, 2, 5]
        
    image_list = []    
    for pdr in pdr_list:
        img = Image.open(('C:\\Users\\Geoff\\Desktop\\PDR expts\\26 Jan 15\\pdr%slambda920acc18.png' % pdr).replace('-', 'n'))
        image_list.append(img)
        
    result = cc.join_horizontally(image_list, img.mode)
    result.save('C:\\Users\\Geoff\\Desktop\\PDR expts\\26 Jan 15\\line_expt.tif')
    
def create_line_of_e_vs_t_images():
    pdr_list = [0.5, 2, 5]
    
    images = []    
    for pdr in pdr_list:
        image1 = Image.open(('C:\\Users\\Geoff\\Desktop\\PDR expts\\26 Jan 15\\pdr%slambda920acc18.tif' % pdr).replace('-', 'n'))
        image2 = Image.open(('C:\\Users\\Geoff\\Desktop\\PDR expts\\26 Jan 15\\pdrn%slambda920acc18.tif' % pdr).replace('-', 'n'))
        images.append(cc.join_vertically([image1, image2], image1.mode))
        assert false # need to fix image1 and image2 paths
    result = cc.join_horizontally(images, image1.mode)
    result.save('C:\\Users\\Geoff\\Desktop\\PDR expts\\26 Jan 15\\line_expt_vs_theory.tif')
    
if __name__ == '__main__':
    process_pdr_list()