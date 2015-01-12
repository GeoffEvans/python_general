from PIL import Image

def hconcat(images):       
    w = sum(i.size[0] for i in images)
    mh = max(i.size[1] for i in images)
    
    result = Image.new("RGBA", (w, mh))
    
    x = 0
    for i in images:
        result.paste(i, (x, 0))
        x += i.size[0]
        
    return result

def vconcat(pdr):
    images = []
    images.append(Image.open('C:\\Users\\Geoff\\Dropbox\\Writing\\PDR OptExp\\images\\results\\pdr%s_exp.tif' % pdr))
    images.append(Image.open('C:\\Users\\Geoff\\Dropbox\\Writing\\PDR OptExp\\images\\results\\pdr%s_model.tif' % pdr))
    
    w = sum(i.size[1] for i in images)
    mh = max(i.size[0] for i in images)
    
    result = Image.new("RGBA", (mh, w))
    
    x = 0
    for i in images:
        result.paste(i, (0, x))
        x += i.size[1]
        
    return result
    
pdr_list = [0.5, 1, 2, 5]

images = []    
for pdr in pdr_list:
    images.append(vconcat(pdr))
    
result = hconcat(images)
result.save('C:\\Users\\Geoff\\Dropbox\\Writing\\PDR OptExp\\images\\new2.tif')
