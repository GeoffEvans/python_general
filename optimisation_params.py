from traits.api import HasTraits, Tuple, Float
from numpy.linalg import norm
from numpy import arctan2, array, pi, cos, sin, sqrt, append

class OptParams(HasTraits):
    xy_start_deg = Tuple(Float(), Float())
    xy_end_deg = Tuple(Float(), Float())
    
    def create_line(self):
        start = array(self.xy_start_deg) * pi/180
        end = array(self.xy_end_deg) * pi/180
        min_val = 0
        fixed = start
        diff = end - start
        max_val = norm(diff)
        ang = arctan2(diff[1], diff[0])
        return (min_val, max_val, ang, fixed)
    
    def min_val(self):
        return self.create_line()[0]
    def max_val(self):
        return self.create_line()[1]
    def ang(self):
        return self.create_line()[2]
    def fixed(self):
        return self.create_line()[3]
    
    def get_normal(self, variable):
        (_, _, ang, fixed) = self.create_line()
        xy_normal = fixed + variable * array([cos(ang), sin(ang)])
        return append(xy_normal, sqrt(1 - norm(xy_normal)**2))