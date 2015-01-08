import pointing_efficiency as p
import convert_to_contour as c

for pdr in [0, 0.5, 1, 2, 5, -0.5, -2, -5]:
    #p.plot_fov_surf(1e9, pdr)
    #p.plt.savefig('pdr%s_model.png' % pdr, bbox_inches='tight')
    c.get_png(pdr)  
    c.plt.title(pdr)
    c.plt.savefig('pdr%s_exp.png' % pdr, bbox_inches='tight')