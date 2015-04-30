import matplotlib.pyplot as plt
import numpy as np
from scipy import misc
from scipy import ndimage
import aol_model.pointing_efficiency as p

aperture_width = 15e-3
acc_ang = 18e-3

def save_figs_for_z_stack_model(pdr):
    save_name = '.\\above_below\\z%s_pdr%s_model.%s'
    norm_zs = [-0.4, 1e-9, 0.4]
    abs_z = [-0.5, 0, 0.5]
    points = map(lambda z: round(aperture_width / (4 * acc_ang * z), 2), norm_zs)
    for fl, z in zip(points, abs_z):
#        effs_norm = p.calc_fov_surf_data(fl, pdr)
        effs_norm = np.load(save_name % (fl, pdr, 'npy'))
        pdr_desc = pdr if pdr is not None else 'min'
        description = 'Model, PDR %s, z=%s' % (pdr_desc, z)
        p.generate_plot(effs_norm, description)
        np.save(save_name % (fl, pdr, 'npy'), effs_norm)
        plt.savefig((save_name % (z, pdr, 'tif')).replace('-', 'n'), bbox_inches='tight')

def save_figs_for_z_stack_expt(pdr):
    file_name = 'C:\\Users\\Geoff\\Dropbox\\Writing\\1) Model and PDR Paper\\images\\panel6 - above & below\\expt\\GreenChannel_00%s_%s.tif'
    save_name = '.\\above_below\\z%s_pdr%s_expt.%s'
    id_list = ['11', '17', '24']
    abs_z = [-0.5, 0, 0.5]

    for id_str, z in zip(id_list, abs_z):
        img_1 = misc.imread(file_name % (id_str, 1))
        img_2 = misc.imread(file_name % (id_str, 2))
        img_3 = misc.imread(file_name % (id_str, 3))
        img_mean = (img_1 + img_2 + img_3) / 3

        img_blur = ndimage.gaussian_filter(img_mean, 0)
        img_blur -= np.min(img_blur)
        ind = np.argmax(img_blur)
        img_blur_norm = img_blur * 1.0 / np.mean(img_blur.flatten()[(ind-7):(ind+8)])

        np.save(save_name % (z, pdr, 'npy'), img_blur_norm)

        pdr_desc = pdr if pdr is not None else 'min'
        description = 'Expt, PDR %s, z=%s' % (pdr_desc, z)
        p.generate_plot(img_blur_norm, description)
        plt.savefig((save_name % (z, pdr, 'tif')).replace('-', 'n'), bbox_inches='tight')

if __name__ == '__main__':
    save_figs_for_z_stack_expt(0.3)
    save_figs_for_z_stack_model(0.3)

    #focal_lengths = map(lambda z: round(15e-3 / (4 * 18e-3 * z), 2), [-0.4, 1e-9, 0.4])
    #print focal_lengths
    #p.plot_peak(focal_lengths)