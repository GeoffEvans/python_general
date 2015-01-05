import matplotlib.pyplot as plt
import numpy as np
from scipy import misc
from scipy import ndimage

img = misc.imread('C:\Users\Geoff\Desktop\PDR expts\\0\GreenChannel_0006.jpg')
plt.imshow(img, cmap=plt.cm.gray)

img_blur = ndimage.gaussian_filter(img, sigma=3)
plt.imshow(img_blur, cmap=plt.cm.gray)

plt.figure()
angles = np.linspace(-34, 34, np.shape(img_blur)[0])
cset = plt.contour(angles, angles, img_blur, np.arange(0,200,25),linewidths=1)
plt.clabel(cset, inline=True, fmt='%1.1f', fontsize=10)    
plt.show()           

 