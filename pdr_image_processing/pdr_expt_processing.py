import numpy as np
from scipy import misc
from scipy import ndimage
import concat_images as cc
from PIL import Image
import pointing_efficiency as p

def process_pdr_list():
    for pdr in [0, 0.1, 0.2, 0.5, 1, 2, 5, -0.1, -0.2, -0.5, -2, -5]:
        expt = get_pdr_expt_images(pdr)
        np.save('.\\images\\pdr%s_expt.npy' % pdr, expt)        
        #p.plt.savefig(('.\\images\\pdr%s_exp_smooth.tif' % pdr).replace('-', 'n'), bbox_inches='tight')
        thry = p.plot_fov_surf(1e9, pdr)
        np.save('.\\images\\pdr%s_model.npy' % pdr, thry)
        scale = expt.shape[0] / thry.shape[0]
        thry_large = ndimage.gaussian_filter(np.kron(thry, np.ones((scale,scale))), 2)
        p.plt.savefig(('.\\images\\pdr%s_model.tif' % pdr).replace('-', 'n'), bbox_inches='tight')        
        description = 'Difference for PDR %s' % pdr 
        p.generate_plot(expt-thry_large, expt*0, description, colmap=p.plt.cm.cool)
        p.plt.savefig(('.\\images\\pdr%s_diff.tif' % pdr).replace('-', 'n'), bbox_inches='tight')     
        p.plt.close('all')

def post_process_pdr_list():
    for pdr in [0, 0.1, 0.2, 0.5, 1, 2, 5, -0.1, -0.2, -0.5, -2, -5]:
        get_pdr_expt_images(pdr)
        p.plt.savefig(('.\\images\\pdr%s_exp_smooth.svg' % pdr).replace('-', 'n'), bbox_inches='tight')
        thry = np.load('.\\images\\pdr%s_model.npy' % pdr)
        description = 'Model for PDR %s' % pdr
        p.generate_plot(thry, thry, description)
        p.plt.savefig(('.\\images\\pdr%s_model.svg' % pdr).replace('-', 'n'), bbox_inches='tight')        
        p.plt.close('all')

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
    post_process_pdr_list()
    create_line_of_e_vs_t_images()