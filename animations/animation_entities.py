import matplotlib.pyplot as plt
import numpy as np

class AnimatedEntity(object):

    def __init__(self):
        self.artist = None
        self.animations = []

    def init_animations(self, axes):
        self.animations.sort(key=lambda tup: tup[0])
        return self.make_artist(axes)

    def update_animations(self, time, time_step):
        completed = []
        for ani in self.animations:
            if ani[1] < time:  # remove completed when end time exceeds current time
                completed.append(ani)
            if ani[0] < time: # execute animation when start time exceeds current time
                ani[2](ani[0], ani[1], time_step, ani[3])
            else: # rest have yet to begin so skip the rest
                break

        [self.animations.remove(ani) for ani in completed] # by removing after, single-time events are guaranteed to execute
        return self.update_artist()

    def add_translation(self, start_time, end_time, displacement):
        self.animations.append( (start_time, end_time, self.translate, displacement) )

    def translate(self, start, end, time_step, displacement):
        num_calls = np.floor( (end - start) / time_step ) + 1 # not the same as ceil at edge case
        fractional_disp = map(lambda x: x * 1. / num_calls, displacement)
        self.xy = map(lambda x,y: x+y, self.xy, fractional_disp)

class AnimatedShape(AnimatedEntity):

    def __init__(self, angle=0, alpha=0.5, facecolor=None):
        super(AnimatedShape, self).__init__()
        self.angle = angle
        self.alpha = alpha
        self.facecolor = facecolor

    def get_patch_kwargs(self):
        d = {}
        d['alpha'] = self.alpha
        d['facecolor'] = self.facecolor
        return d

    def change_alpha(self, event_time, new_alpha):
        self.animations.append( (event_time, event_time, self.set_alpha, new_alpha) )

    def set_alpha(self, start, end, step, alpha):
        self.alpha = alpha

class Square(AnimatedShape):

    def __init__(self, side, centre, **kwargs):
        super(Square, self).__init__(**kwargs)
        self.side = side
        self.centre = centre

    @property
    def xy(self):
        return self.centre
    @xy.setter
    def xy(self, centre):
        self.centre = centre

    def make_artist(self, axes):
        self.artist = plt.Rectangle( self.get_corner(), width=self.side, \
            height=self.side, angle=self.angle, **self.get_patch_kwargs())
        axes.add_patch(self.artist)
        return self.artist

    def update_artist(self):
        corner = self.get_corner()
        self.artist.set_xy(corner)
        self.artist.set_alpha(self.alpha)
        return self.artist

    def get_corner(self):
        dist = self.side / np.sqrt(2)
        ang = np.deg2rad(225 + self.angle)
        corner_x = self.centre[0] + dist * np.cos(ang)
        corner_y = self.centre[1] + dist * np.sin(ang)
        return (corner_x, corner_y)

class TriangleRa(AnimatedShape):

    def __init__(self, width, height, corner_ra, **kwargs):
        super(TriangleRa, self).__init__(**kwargs)
        self.width = width
        self.height = height
        self.corner_ra = corner_ra

    @property
    def xy(self):
        return self.corner_ra
    @xy.setter
    def xy(self, corn):
        self.corner_ra = corn

    def make_artist(self, axes):
        vertices = self.get_vertices()
        self.artist = plt.Polygon(vertices, True, **self.get_patch_kwargs())
        axes.add_patch(self.artist)
        return self.artist

    def update_artist(self):
        vertices = self.get_vertices()
        self.artist.set_xy(vertices)
        return self.artist

    def get_vertices(self):
        c = np.cos(np.deg2rad(self.angle))
        s = np.sin(np.deg2rad(self.angle))
        v0 = [0, 0]
        v1 = [c * self.width, -s * self.width]
        v2 = [s * self.height, c * self.height]
        vertices = np.vstack( (v0, v1, v2) )
        return vertices + self.corner_ra
