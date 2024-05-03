import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def mandelbrot(x, y, threshold):
    """Calculates whether the number c = x + i*y belongs to the 
    Mandelbrot set. In order to belong, the sequence z[i + 1] = z[i]**2 + c
    must not diverge after 'threshold' number of steps. The sequence diverges
    if the absolute value of z[i+1] is greater than 4.
    
    :param float x: the x component of the initial complex number
    :param float y: the y component of the initial complex number
    :param int threshold: the number of iterations to considered it converged
    """
    # initial conditions
    c = complex(x, y)
    z = complex(0, 0)
    
    for i in range(threshold):
        z = z**2 + c
        if abs(z) > 4.:  # it diverged
            return i
        
    return threshold - 1  # it didn't diverge

x_center, y_center = -0.5, 0  # center of the initial view
zoom_factor = 1  # initial zoom level
density_per_unit = 250  # how many pixels per unit

fig = plt.figure(figsize=(10, 10))  # instantiate a figure to draw
ax = plt.axes()  # create an axes object

def animate(i):
    ax.clear()  # clear axes object
    ax.set_xticks([], [])  # clear x-axis ticks
    ax.set_yticks([], [])  # clear y-axis ticks
    
    # Calculate new view parameters based on zoom
    x_start = x_center - 1.5 / zoom_factor
    y_start = y_center - 1.5 / zoom_factor
    width = 3 / zoom_factor
    height = 3 / zoom_factor
    
    re = np.linspace(x_start, x_start + width, int(width * density_per_unit))
    im = np.linspace(y_start, y_start + height, int(height * density_per_unit))

    X = np.empty((len(re), len(im)))  # re-initialize the array-like image
    threshold = round(1.15**(i + 1))  # calculate the current threshold
    
    # iterations for the current threshold
    for i in range(len(re)):
        for j in range(len(im)):
            X[i, j] = mandelbrot(re[i], im[j], threshold)
    X = np.rot90(X, k=4)
    
    # associate colors to the iterations with an interpolation
    img = ax.imshow(X.T, interpolation="bicubic", cmap='magma')
    return [img]

anim = animation.FuncAnimation(fig, animate, frames=15, interval=120, blit=True)
anim.save('mandelbrot.gif', writer='imagemagick')
