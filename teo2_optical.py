from numpy import array, diag, cos, sin, transpose

# Follow the calculation in Xu&St Section 1.3
# z axis is taken as direction of light propagation

principal_refractive_indices = array([2.2597 , 2.2597, 2.4119]) 
relative_impermeability_eigenvals = principal_refractive_indices**-2
activity_vector = 2.65e-05; #See Warner White Bonner, 87deg/mm
 
def calc_refractive_indices(angles):
    transverse_imperm_eigvals = find_transverse_imperm_eigvals(angles)
    eigenval1 = transverse_imperm_eigvals[:,0]
    eigenval2 = transverse_imperm_eigvals[:,1]     
    
    sqr_term = (eigenval1 - eigenval2)**2 + 4 * activity_vector**2
    eigensum = eigenval1 + eigenval2
    
    ext_recip_sqr = 0.5 * ( eigensum - sqr_term**0.5 ) # Xu&St (1.62)
    ord_recip_sqr = 0.5 * ( eigensum + sqr_term**0.5 )

    n_e = ext_recip_sqr ** (-0.5)
    n_o = ord_recip_sqr ** (-0.5)
    
    return (n_e,n_o)
    
def calc_polarisations(angles):
    transverse_imperm_eigvals = find_transverse_imperm_eigvals(angles)
    eigenval1 = transverse_imperm_eigvals[:,0]
    eigenval2 = transverse_imperm_eigvals[:,1]     
    
    sqr_term = (eigenval1 - eigenval2)**2 + 4 * activity_vector**2
    eigendiff = eigenval2 - eigenval1
    
    p_e = 0.5j / activity_vector * ( sqr_term**0.5 - eigendiff ) # Xu&St (1.62)
    p_o = -0.5j / activity_vector * ( sqr_term**0.5 + eigendiff )
    
    return (p_e,p_o)
    
def find_transverse_imperm_eigvals(angles):
    from numpy.linalg import eig
    relative_impermeability_matrix = find_relative_impermeability_matrix(angles) # Xu&St (1.59)
    return eig([x[0:2,0:2] for x in relative_impermeability_matrix])[0] # don't care about the third eigenvalue which is parallel to propagation

def find_relative_impermeability_matrix(angles):
    from similarity_transformation import rotate_matrix

    def get_yz_rotation_matrix(angles):
        num_angles = angles.size
        one = array([1] * num_angles)
        zero = array([0] * num_angles)
        elems = array([[one,    zero,          zero           ], \
                 [zero,    cos(angles), -sin(angles) ], \
                 [zero,    sin(angles), cos(angles)  ]])
        return transpose(elems, (2,0,1)); # permute indices to get [angle, row, col]

    principal_imperm = diag(relative_impermeability_eigenvals)    
    rotation_matrix = get_yz_rotation_matrix(angles)
    return rotate_matrix(rotation_matrix, principal_imperm)

def plot_refractive_index(): 
    from pylab import plot,xlabel,ylabel,title,grid,show
    from numpy import arange,pi
    
    angles = arange(-pi/2, pi/2, pi/360)
    n = calc_refractive_indices(angles)
    plot(angles, n[0])
    plot(angles, n[1])
    
    xlabel('angle / rad')
    ylabel('refractive index')
    title('Ordinary under Extraordinary')
    grid(True)
    show()
    
plot_refractive_index()