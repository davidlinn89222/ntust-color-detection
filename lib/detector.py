# import required module
import numpy as np
import cv2
import os
import re

def detector(path):
	# Read the image in # color model is BGR
	img = cv2.imread(path,  cv2.IMREAD_UNCHANGED) # arg 

	# Copy img
	original = img.copy() 
	original_t = img.copy()

	# Transform the BGR model to HSV model 
	img1 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	img2 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	# Calculate specific area 

	# Define the range of colour we wanna detect (red one)
	lower = np.array([1,0,0], dtype = "uint8")
	upper = np.array([108,255,255], dtype = "uint8")

	mask = cv2.inRange(img1, lower, upper)
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
	opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)

	cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if len(cnts) == 2 else cnts[1]

	desired_area = 0
	for c in cnts:
		desired_area += cv2.contourArea(c)
		cv2.drawContours(original, [c], 0, (0, 0, 0), 2)

	# Exclude white area and calculate total pixels 
	lower_w = np.array([0,255,0], dtype = "uint8")
	upper_w = np.array([179,255,255], dtype = "uint8")

	mask_w = cv2.inRange(img2, lower_w, upper_w)
	kernel_w = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
	opening_w = cv2.morphologyEx(mask_w, cv2.MORPH_OPEN, kernel_w, iterations=1)

	cnts_w = cv2.findContours(opening_w, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts_w = cnts_w[0] if len(cnts_w) == 2 else cnts_w[1]

	whole_area = 0
	for c in cnts_w:
		whole_area += cv2.contourArea(c)
		cv2.drawContours(original_t, [c], 0, (0, 0, 0), 2)


	# result to return 
	res = {}
	subfile_path = os.path.split(path)[1]
	num = re.search(r"\d+", subfile_path).group()

	res["section"] = int(num)
	res["desired_area"] = desired_area
	res["total_area"] = whole_area
	res["percentage"] = desired_area / whole_area

	print("\nImage name: {}".format(num))
	print("Fail area: {0:>7.0f} pixels".format(desired_area))
	print("Total area: {0:>7.0f} pixels".format(whole_area))
	print("Percentage: {}\n".format(desired_area/whole_area))

	return res

