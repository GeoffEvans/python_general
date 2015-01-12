import pointing_efficiency as p
import convert_to_contour as c

z = [-1, 1e9, 1]
count = [5, 6, 7]

for n in range(3):
    p.plot_fov_surf(z[n], 0)
    p.plt.savefig('z%s_model.tif' % z[n], bbox_inches='tight')
    c.get_z_contour(count[n])  
    c.plt.savefig('z%s_exp.tif' % z[n], bbox_inches='tight')