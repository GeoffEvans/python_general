from PIL import Image

def join_horizontally(image_list, mode):       
    width = sum(i.size[0] for i in image_list)
    height = max(i.size[1] for i in image_list)
    
    img = Image.new(mode, (width, height))
    
    position_from_left = 0
    for i in image_list:
        img.paste(i, (position_from_left, 0))
        img_width = i.size[0]
        position_from_left += img_width
        
    return img
    
def join_vertically(image_list, mode):       
    width = max(i.size[0] for i in image_list)
    height = sum(i.size[1] for i in image_list)
    
    img = Image.new(mode, (width, height))
    
    position_from_bottom = 0
    for i in image_list:
        img.paste(i, (0, position_from_bottom))
        img_height = i.size[1]
        position_from_bottom += img_height
        
    return img