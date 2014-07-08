from numpy import meshgrid, vectorize
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
    
def generic_plot_surface(x_array, y_array, z_func, labels):
    (x, y) = meshgrid(x_array, y_array)
    z_func_vec = vectorize(z_func)
    z = z_func_vec(x, y) 
    generic_plot_surface_vals(x, y, z, labels)

def generic_plot_surface_vals(x, y, z, labels):
    fig = plt.figure()
    ax = fig.gca()               
    cs = ax.pcolor(x, y, z)   
    
    def onclick(event):
        print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
            event.button, event.x, event.y, event.xdata, event.ydata)
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    
    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])
    cb = plt.colorbar(cs, orientation = 'vertical') 
    cb.set_label(labels[2]) 

    plt.grid() 
    plt.show()

def generic_plot_vals(x, y, labels, limits=0):
    fig = plt.figure()
    ax = fig.gca()               
    cs = ax.plot(x, y)   
    
    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])
    
    if not limits == 0:
        plt.axis(limits)
    plt.grid()
    plt.show()
    
def generic_plot(x, y_func, labels, limits=0):
    y_func_vec = vectorize(y_func)
    y = y_func_vec(x) 
    generic_plot_vals(x, y, labels, limits)
    
def multi_line_plot(x, y_func_many, labels, lgnd, limits=0):
    fig = plt.figure()
    ax = fig.gca() 
    
    for y_func in y_func_many:
        y_func_vec = vectorize(y_func)
        y = y_func_vec(x) 
        plt.plot(x, y)   
    
    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])
    
    if not limits == 0:
        plt.axis(limits)
    plt.legend(lgnd, loc='upper left')
    plt.grid()
    plt.show()
    
def multi_line_plot_vals(x, y_many, labels, lgnd, limits=0):
    fig = plt.figure()
    ax = fig.gca() 
    
    for y in y_many:
        plt.plot(x, y)   
    
    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])
    
    if not limits == 0:
        plt.axis(limits)
    plt.legend(lgnd, loc='upper left')
    plt.grid()
    plt.show()
    