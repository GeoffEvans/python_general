import matplotlib.pyplot as plt
import numpy as np
from scipy import misc
from scipy import ndimage
from scipy.constants import pi

def get_pdr_contour(pdr):
    img = misc.imread('C:\Users\Geoff\Desktop\PDR expts\\%s\\Zstack Images\\GreenChannel_0007.tif' % pdr)
    get_contour(img)    

def get_z_contour(z):
    img = misc.imread('C:\Users\Geoff\Desktop\PDR expts\\0\\Zstack Images\\GreenChannel_000%d.tif' % z)
    get_contour(img)    
    
def get_contour(img):
    #plt.figure()
    #plt.imshow(img, cmap=plt.cm.gray)
    
    img_blur = ndimage.gaussian_filter(img, 2 )
    img_blur -= np.min(img_blur)
    #plt.figure()
    #plt.imshow(img_blur, cmap=plt.cm.gray)
    
    plt.figure()
    angles = np.linspace(-68, 68, np.shape(img_blur)[0]) * 1e-3 * 180/pi
    img_blur_norm = img_blur * 1. / np.max(img_blur)
    
    plt.pcolormesh(angles, angles, img, cmap=plt.cm.bone)
    cset = plt.contour(angles, angles, img_blur_norm, np.arange(0.1,1,0.1),linewidths=1, cmap=plt.cm.coolwarm)
    plt.clabel(cset, inline=True, fmt='%1.1f', fontsize=10)    
    plt.show()           

if __name__ == '__main__':
    get_contour(0)