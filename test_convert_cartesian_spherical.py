from numpy import zeros, arccos, arctan2, vstack, sin, cos
from numpy.linalg import norm

def cartesian_to_spherical(xyz):
    x = xyz[0,:]
    y = xyz[1,:]
    z = xyz[2,:]
    r = norm(xyz,axis=0) 
    theta = arccos(z/r)
    phi = arctan2(y/x)
    return vstack(r, theta, phi)

def spherical_to_cartesian(sph):
    r = sph[0,:]
    theta = sph[1,:]
    phi = sph[2,:]
    x = r * sin(theta) * cos(phi)
    y = r * sin(theta) * sin(phi)
    z = r * cos(theta)
    return vstack(x, y, z)