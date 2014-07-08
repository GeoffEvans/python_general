from numpy import array, diag, transpose, dot, atleast_1d, sqrt, arange, pi, abs,\
    power
from scipy.interpolate import splrep, splev 

# Follow the calculation in Xu&St Section 1.3
# z axis is taken as direction of the optical wavevector

principal_refractive_indices = array([2.2597 , 2.2597, 2.4119]) 
relative_impermeability_eigenvals = power(principal_refractive_indices, -2.)
activity_vector = 2.65e-05; #See Warner White Bonner, 87deg/mm

def get_imperm_properties(angles):
    angles = atleast_1d(angles)
    transverse_imperm_eigvals = find_transverse_imperm_eigvals(angles)
    eigenval1 = transverse_imperm_eigvals[:,0]
    eigenval2 = transverse_imperm_eigvals[:,1]     
    
    sqrt_term = sqrt( power(eigenval1 - eigenval2, 2.) + 4 * activity_vector**2)
    eigensum = eigenval1 + eigenval2
    eigendiff = eigenval2 - eigenval1
    
    return (sqrt_term,eigensum,eigendiff)

def find_transverse_imperm_eigvals(angles):
    relative_impermeability_matrix = find_relative_impermeability_matrix(angles) # Xu&St (1.59)
    return array([[x[0,0],x[1,1]] for x in relative_impermeability_matrix]) # eigenvals for transverse components
   
def find_relative_impermeability_matrix(angles):
    principal_imperm = diag(relative_impermeability_eigenvals)    
    rotation_matrix = get_yz_rotation_matrix(angles)
    return array([dot(dot(rot,principal_imperm),rot.T) for rot in rotation_matrix])

def get_yz_rotation_matrix(angles):
    from numpy import cos, sin
    num_angles = angles.size
    one = array([1] * num_angles)
    zero = array([0] * num_angles)
    elems = array([[one,    zero,          zero           ], \
             [zero,    cos(angles), -sin(angles) ], \
             [zero,    sin(angles), cos(angles)  ]])
    return transpose(elems, (2,0,1)); # permute indices to get [angle, row, col]

def calc_refractive_indices_slow(angles):
    (sqrt_term,eigensum,_) = get_imperm_properties(atleast_1d(angles))
    
    ext_recip_sqr = 0.5 * ( eigensum - sqrt_term ) # Xu&St (1.62)
    ord_recip_sqr = 0.5 * ( eigensum + sqrt_term )

    n_e = power(ext_recip_sqr, -0.5)
    n_o = power(ord_recip_sqr, -0.5)
    
    return (n_e,n_o)

def calc_polarisations_slow(angles):
    (sqrt_term,_,eigendiff) = get_imperm_properties(angles)
    
    p_e =  0.5j / activity_vector * ( sqrt_term - eigendiff ) # Xu&St (1.62)
    p_o = -0.5j / activity_vector * ( sqrt_term + eigendiff )
    
    return (p_e,p_o)

angles = arange(0, pi/2+1e-4, 1e-4)
n_e_spl = splrep(angles, calc_refractive_indices_slow(angles)[0])
n_o_spl = splrep(angles, calc_refractive_indices_slow(angles)[1])

def calc_refractive_indices(angles):  
    return (splev(abs(angles),n_e_spl),splev(abs(angles),n_o_spl))
    
def plot_refractive_index(): 
    from pylab import plot,xlabel,ylabel,title,grid,show
    
    angles = arange(-pi/2, pi/2, pi/360)
    n = calc_refractive_indices_slow(angles)
    m = calc_refractive_indices(angles)
    
    plot(angles, n[0])
    plot(angles, n[1])
    plot(angles, m[0])
    plot(angles, m[1])
    
    xlabel('angle / rad')
    ylabel('refractive index')
    title('Ordinary under Extraordinary')
    grid(True)
    show()

if __name__ == '__main__':
    plot_refractive_index()