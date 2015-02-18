import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as anim 

class AnimatedEntity(object):
    
    def __init__(self):    
        self.artist = None
        self.animations = []
    
    def init_animations(self, axes):
        self.animations.sort(key=lambda tup: tup[0])
        return self.make_artist(axes)
    
    def update_animations(self, time, time_step):
        [self.animations.remove(ani) for ani in self.animations if ani[1] < time] # remove completed
        
        for ani in self.animations:
            if ani[0] < time:
                ani[2](ani[0], ani[1], time_step, ani[3])
            else: # rest waiting to begin
                break
        return self.update_artist()

class Square(AnimatedEntity):
    
    def __init__(self, side, centre):
        super(Square, self).__init__()
        self.side = side
        self.centre = centre
        
    def make_artist(self, axes):
        self.artist = plt.Rectangle( (self.centre[0], self.centre[1]), \
            width=self.side, height=self.side, facecolor='none')
        axes.add_patch(self.artist)
        return self.artist
        
    def update_artist(self):
        return self.artist
    
class TriangleRa(AnimatedEntity):

    def __init__(self, width, height, corner_ra, angle=0 ):
        super(TriangleRa, self).__init__()        
        self.width = width
        self.height = height
        self.corner_ra = corner_ra
        self.angle = angle
    
    def add_translation(self, start_time, end_time, displacement):
        self.animations.append( (start_time, end_time, self.translate, displacement) )

    def translate(self, start, end, time_step, displacement):
        frac = time_step / (end - start)
        fractional_disp = map(lambda x: x * frac, displacement)       
        self.corner_ra = map(lambda x,y: x+y, self.corner_ra, fractional_disp)

    def get_vertices(self):
        c = np.cos(np.deg2rad(self.angle))
        s = np.sin(np.deg2rad(self.angle))
        v0 = [0, 0]        
        v1 = [c * self.width, -s * self.width]
        v2 = [s * self.height, c * self.height]
        vertices = np.vstack( (v0, v1, v2) )        
        return vertices + self.corner_ra

    def make_artist(self, axes):
        vertices = self.get_vertices()
        self.artist = plt.Polygon(vertices, True)        
        axes.add_patch(self.artist)
        return self.artist
    
    def update_artist(self):
        vertices = self.get_vertices()
        self.artist.set_xy(vertices)
        return self.artist

def create_entities():
    sqr = Square(7, (0,0))
    t1 = TriangleRa(3, 4, (0,0), angle=0)
    t2 = TriangleRa(3, 4, (0,7), angle=90)
    t3 = TriangleRa(3, 4, (7,7), angle=180)
    t4 = TriangleRa(3, 4, (7,0), angle=270)
    ents = (sqr, t1, t2, t3, t4)    
    return ents, sqr, t1, t2, t3, t4
    
def animate_entities(t1, t2, t3):
    t3.add_translation(4., 5., (-4.,-3.))
    t2.add_translation(5., 6., (3.,0.))
    t2.add_translation(6., 7., (0.,-4.))
    
    t1.add_translation(7., 8., (0.,3.))
    t3.add_translation(7., 8., (0.,3.))
    
def update_anim(frame_count, entities):
    time_step = 0.1    
    time = frame_count * time_step
    new_artists = [ent.update_animations(time, time_step) for ent in entities]
    return new_artists

def make_animation():
    fig = plt.figure()    
    axes = plt.axes(xlim=(-3, 10), ylim=(-3, 10))
    plt.grid()
    
    entities, sqr, t1, t2, t3, t4 = create_entities()
    animate_entities(t1, t2, t3)
    
    def init_anim():
        artists = [ent.init_animations(axes) for ent in entities]
        return artists
    
    return anim.FuncAnimation(fig, update_anim, init_func=init_anim, frames=200, interval=10, fargs=(entities,))
    
if __name__ == "__main__":
    anim = make_animation()