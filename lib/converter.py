def rgb_to_hsv(rgb_lst): 

    """
    Convert the color specified as RGB value into HSV value used in genenric HSV model.
    
    Args:
        rgb_lst (list of integer): RGB value (ex. [r, g, b])
    
    Returns:
        list: a list with HSV value (ex. [h, s, v])
    """

    # R, G, B values are divided by 255 to change the range from 0...255 to 0...1: 
    r, g, b = rgb_lst[0] / 255.0, rgb_lst[1] / 255.0, rgb_lst[2] / 255.0
  
    # h, s, v = hue, saturation, value 
    cmax = max(r, g, b)    # maximum of r, g, b 
    cmin = min(r, g, b)    # minimum of r, g, b 
    diff = cmax - cmin       # diff of cmax and cmin. 
  
    # if cmax and cmax are equal then h = 0 
    if cmax == cmin:  
        h = 0
      
    # if cmax equal r then compute h 
    elif cmax == r:  
        h = (60 * ((g - b) / diff) + 360) % 360
  
    # if cmax equal g then compute h 
    elif cmax == g: 
        h = (60 * ((b - r) / diff) + 120) % 360
  
    # if cmax equal b then compute h 
    elif cmax == b: 
        h = (60 * ((r - g) / diff) + 240) % 360
  
    # if cmax equal zero 
    if cmax == 0: 
        s = 0
    else: 
        s = (diff / cmax) * 100
  
    # compute v 
    v = cmax * 100

    return [h, s, v]




def hsv_to_hsvOpenCV(hsv_lst):

    """
    Convert the color specified as HSV value into HSV value used in OpenCV function
    
    Args:
        hst_list (list of integer): hsv value (ex. [h, s, v])
    
    Returns:
        list: a list with HSV value used in OpenCV function (ex. [h', s', v'])
    """

    # transform the HSV in generic model into the value required by OpenCV
    H, S, V = hsv_lst[0], hsv_lst[1], hsv_lst[2]

    return [H/2, (S/100) * 255, (V/100) * 255]



