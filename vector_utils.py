from numpy import dot
from numpy.linalg import norm

def normalise(vector):
    return vector/norm(vector, axis=0)

def normalise_list(vectors):
    return (vectors.T/norm(vectors, axis=1)).T

def perpendicular_component(vector, unit_normal):
    return vector - dot(vector, unit_normal) * unit_normal