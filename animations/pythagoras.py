import matplotlib.pyplot as plt
import matplotlib.animation as anim
from animation_entities import TriangleRa, Square

def create_entities():
    sqr = Square(7, (3.5,3.5), facecolor='none')
    t1 = TriangleRa(3, 4, (0,0), angle=0.)
    t2 = TriangleRa(3, 4, (0,7), angle=90.)
    t3 = TriangleRa(3, 4, (7,7), angle=180.)
    t4 = TriangleRa(3, 4, (7,0), angle=270.)
    sqr_a = Square(3, (1.5,1.5), alpha=0, facecolor='red')
    sqr_b = Square(4, (5,5), alpha=0, facecolor='red')
    sqr_c = Square(5, (3.5,3.5), angle=36.87, facecolor='yellow')
    return (sqr, t1, t2, t3, t4, sqr_a, sqr_b, sqr_c)

def animate_entities(sqr, t1, t2, t3, t4, sqr_a, sqr_b, sqr_c):
    MV_SQR1 = 6
    MV_TRI = MV_SQR1 + 3
    AP_SQR = MV_TRI + 5
    MV_SQR2 = AP_SQR + 1

    sqr_c.add_translation(MV_SQR1, MV_SQR1 + 2, (10.,3.))

    t3.add_translation(MV_TRI, MV_TRI + 1, (-4.,-3.))
    t2.add_translation(MV_TRI + 1, MV_TRI + 2, (3.,0.))
    t2.add_translation(MV_TRI + 2, MV_TRI + 3., (0.,-4.))

    t1.add_translation(MV_TRI + 3, MV_TRI + 4, (0.,3.))
    t3.add_translation(MV_TRI + 3, MV_TRI + 4, (0.,3.))

    sqr_a.change_alpha(AP_SQR, 0.5)
    sqr_b.change_alpha(AP_SQR, 0.5)
    sqr_a.add_translation(MV_SQR2, MV_SQR2 + 2, (17.,3.))
    sqr_b.add_translation(MV_SQR2, MV_SQR2 + 2, (10.,-4.))

def update_anim(frame_count, entities):
    time_step = 0.1
    time = frame_count * time_step
    new_artists = [ent.update_animations(time, time_step) for ent in entities]
    return new_artists

def init_anim(axes, entities):
    artists = [ent.init_animations(axes) for ent in entities]
    return artists

def make_animation():
    fig = plt.figure()
    axes = plt.axes(xlim=(-1, 21), ylim=(-3, 10))
    axes.set_axis_off()
    axes.set_aspect('equal', adjustable='box')

    entities = create_entities()
    animate_entities(*entities)
    init_anim(axes, entities)

    return anim.FuncAnimation(fig, update_anim, frames=200, interval=40, fargs=(entities,))

if __name__ == "__main__":
    anim = make_animation()