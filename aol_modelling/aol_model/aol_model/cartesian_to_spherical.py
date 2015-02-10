from numpy import arccos, arctan2, vstack, sin, cos, array
from numpy.linalg import norm

def cartesian_to_spherical(xyz):
    x = xyz[0,:]
    y = xyz[1,:]
    z = xyz[2,:]
    r = norm(xyz,axis=0) 
    theta = arccos(z/r)
    phi = arctan2(y, x)
    return vstack( (r, theta, phi) )

def spherical_to_cartesian(sph):
    r = sph[0,:]
    theta = sph[1,:]
    phi = sph[2,:]
    x = r * sin(theta) * cos(phi)
    y = r * sin(theta) * sin(phi)
    z = r * cos(theta)
    return vstack( (x, y, z) )

if __name__ == '__main__':
    from set_up_utils import set_up_aol
    aol = set_up_aol()
    orients = cartesian_to_spherical(array([a.normal for a in aol.aods]).T)
    print orients