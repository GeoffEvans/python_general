import matplotlib.pyplot as plt
import numpy as np
from scipy import misc
from scipy import ndimage
from scipy.constants import pi

img = misc.imread('C:\Users\Geoff\Desktop\PDR expts\\0\GreenChannel_0007.jpg')
#plt.figure()
#plt.imshow(img, cmap=plt.cm.gray)

img_blur = ndimage.gaussian_filter(img, sigma=3)
#plt.figure()
#plt.imshow(img_blur, cmap=plt.cm.gray)

plt.figure()
angles = np.linspace(-68, 68, np.shape(img_blur)[0]) * 1e-3 * 180/pi
img_blur_norm = img_blur * 1. / np.max(img_blur)
cset = plt.contour(angles, angles, img_blur_norm, np.arange(0,1,0.1),linewidths=1)
plt.clabel(cset, inline=True, fmt='%1.1f', fontsize=10)    
plt.show()           

 