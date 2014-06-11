from numpy import dot
from numpy.linalg import norm

def normalise(vectors):
    return vectors/norm(vectors, axis=0)

def perpendicular_component(vector, unit_normal):
    return vector - dot(vector, unit_normal) * unit_normal