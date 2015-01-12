import pointing_efficiency as p
import convert_to_contour as c

for pdr in [0, 0.5, 1, 2, 5, -0.5, -2, -5]:
    p.plot_fov_surf(1e9, pdr)
    p.plt.savefig(('pdr%s_model.tif' % pdr).replace('-', 'n'), bbox_inches='tight')
    c.get_pdr_contour(pdr)  
    c.plt.savefig(('pdr%s_exp.tif' % pdr).replace('-', 'n'), bbox_inches='tight')