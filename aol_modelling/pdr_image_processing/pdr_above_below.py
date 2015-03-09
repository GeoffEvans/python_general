import matplotlib.pyplot as plt
import numpy as np
from scipy import misc
from scipy import ndimage
import aol_model.pointing_efficiency as p

def save_figs_for_z_stack_model(pdr):
    save_name = '.\\above_below\\z%s_pdr%s_model.%s'
    norm_zs = [-0.25, 0.23]
    abs_z = [160, -160]
    points = map(lambda z: round(15e-3 / (4 * 18e-3 * z), 2), norm_zs)
    for fl, z in zip(points, abs_z):
        effs_norm = p.calc_fov_surf_data(fl, pdr)
        description = 'Model, PDR %s, z = %s' % (pdr, z)
        p.generate_plot(effs_norm, description)
        np.save(save_name % (fl, pdr, 'npy'), effs_norm)
        plt.savefig((save_name % (z, pdr, 'tif')).replace('-', 'n'), bbox_inches='tight')

def save_figs_for_z_stack_expt(pdr):
    file_name = 'C:\\Users\\Geoff\\Desktop\\PDR expts\\25 Feb 2015\\_%s_%s\\Zstack Images\\GreenChannel_00%s.tif'
    save_name = '.\\above_below\\z%s_pdr%s_expt.%s'
    id_list = ['06', '10']
    norm_zs = [-0.2462, 0.2341]
    abs_z = [160, -160]

    for id_str, z in zip(id_list, abs_z):
        img_1 = misc.imread(file_name % (pdr, 1, id_str))
        img_2 = misc.imread(file_name % (pdr, 2, id_str))
        img_3 = misc.imread(file_name % (pdr, 3, id_str))
        img_mean = (img_1 + img_2 + img_3) / 3

        img_blur = ndimage.gaussian_filter(img_mean, 3 )
        img_blur -= np.min(img_blur)
        img_blur_norm = img_blur * 1.0 / np.max(img_blur)

        np.save(save_name % (z, pdr, 'npy'), img_blur_norm)

        description = 'Expt, PDR %s, z = %s' % (pdr, z)
        p.generate_plot(img_blur_norm, description)
        plt.savefig((save_name % (z, pdr, 'tif')).replace('-', 'n'), bbox_inches='tight')

if __name__ == '__main__':
    save_figs_for_z_stack_expt(0)
    save_figs_for_z_stack_expt(1)
    save_figs_for_z_stack_model(0)
    save_figs_for_z_stack_model(1)