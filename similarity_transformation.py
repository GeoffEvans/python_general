from numpy import dot

def rotate_matrix(rotations, matrix):
    return [dot(dot(rot,matrix),rot.T) for rot in rotations]
