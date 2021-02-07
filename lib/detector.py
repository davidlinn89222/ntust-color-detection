# import required module
import numpy as np
import cv2
import os
import re
from lib import converter

def detector(path, color_spec_rgb_dicts):
    """
   	using OpenCV to detect the area of specific color in an image 
    
    Args:
        path (string): the path of image directory
        color_spec_rgb_dicts (dict): color and its corresponding lower bound and upper bound 
    
    Returns:
        list: a list containing the desired result such as fail area and percetage, etc.
    """

    # Read the image in # color model is BGR
    img = cv2.imread(path,  cv2.IMREAD_UNCHANGED) # arg

    # Transform the RGB model to HSV model 
    # img1 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # img2 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # img3 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    color_ranges_RGB = []
    for key, value in color_spec_rgb_dicts.items():
    	color_ranges_RGB.append(value)

    # convert the desired RGB value to HSV value
    color_ranges_HSV = [[converter.hsv_to_hsvOpenCV(converter.rgb_to_hsv(y)) for y in x] for x in color_ranges_RGB]

    undesired_area = 0
    # Calculate the total pixels for each desired color, then sum them up
    for color_range_HSV in color_ranges_HSV:

    	# Transform the RGB model to HSV model
    	img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    	mask = cv2.inRange(img_HSV, np.array(color_range_HSV[0], dtype = "uint8"), np.array(color_range_HSV[1], dtype = "uint8"))
    	undesired_area += cv2.countNonZero(mask)

    # define the area 
    # red_lower = np.array(red_hsv[0], dtype = "uint8")
    # red_upper = np.array(red_hsv[1], dtype = "uint8")

    # mask_red = cv2.inRange(img1, red_lower, red_upper)
    # kernel_red = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    # opening_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel_red, iterations = 1)

    # red_area = cv2.countNonZero(mask_red)

    # red_cnts = cv2.findContours(opening_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # red_cnts = red_cnts[0] if len(red_cnts) == 2 else red_cnts[1]

    # red_area = 0
    # for c in red_cnts:
    #    red_area += cv2.contourArea(c)
    #    cv2.drawContours(original1, [c], 0, (0, 0, 0), 2)

    # detect the blue area 
    # blue_lower = np.array([120, 255, 255], dtype = "uint8")
    # blue_upper = np.array([120.70588235294117, 255, 255], dtype = "uint8")

    # mask_blue = cv2.inRange(img2, blue_lower, blue_upper)
    # kernel_blue = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    # opening_blue = cv2.morphologyEx(mask_blue, cv2.MORPH_OPEN, kernel_blue, iterations = 1)

    # blue_area = cv2.countNonZero(mask_blue)

    # blue_cnts = cv2.findContours(opening_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # blue_cnts = blue_cnts[0] if len(blue_cnts) == 2 else blue_cnts[1]

    # blue_area = 0
    # for c in blue_cnts:
    #    blue_area += cv2.contourArea(c)
    #    cv2.drawContours(original2, [c], 0, (0, 0, 0), 2)
        
    # cv2.imshow('mask', mask_blue)
    # cv2.imshow('original', original2)
    # cv2.waitKey(0)

    # print(blue_area + red_area)

    # Exclude white area and calculate total pixels 
    img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    nonWhite_lower = np.array([0, 255, 0], dtype = "uint8")
    nonWhite_upper = np.array([179, 255, 255], dtype = "uint8")

    mask_nonWhite = cv2.inRange(img_HSV, nonWhite_lower, nonWhite_upper)
    # kernel_nonWhite = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    # opening_nonWhite = cv2.morphologyEx(mask_nonWhite, cv2.MORPH_OPEN, kernel_nonWhite, iterations = 1)

    whole_area = cv2.countNonZero(mask_nonWhite)
    
    # nonWhite_cnts = cv2.findContours(opening_nonWhite, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # nonWhite_cnts = nonWhite_cnts[0] if len(nonWhite_cnts) == 2 else nonWhite_cnts[1]

    # whole_area = 0
    # for c in nonWhite_cnts:
    #    whole_area += cv2.contourArea(c)
    #    cv2.drawContours(original3, [c], 0, (0, 0, 0), 2)
        
    # cv2.imshow('mask', mask_nonWhite)
    # cv2.imshow('original', original3)
    # cv2.waitKey(0)
    
    # list-structured result to be returned 
    res = {}

    subfile_path = os.path.split(path)[1]
    num = re.search(r"\d+", subfile_path).group()

    desired_area = whole_area - undesired_area

    res["section"] = int(num)
    res["undesired_area"] = undesired_area
    res["total_area"] = whole_area
    res["percentage"] = desired_area / whole_area

    print("\nImage name: {}".format(num))
    print("Fail area: {0:>7.0f} pixels".format(desired_area))
    print("Total area: {0:>7.0f} pixels".format(whole_area))
    print("Percentage: {}\n".format(desired_area/whole_area))

    return res



