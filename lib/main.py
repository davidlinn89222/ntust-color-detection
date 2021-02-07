import sys
import re
import os
from lib import detector
import csv
import collections

def main(color_spec_rgb_dicts, image_path, download_path):
	"""
    create the desired results using detector() function
    
    Args:
        color_spec_rgb_dicts (dict): color and its corresponding lower bound and upper bound 
        image_path (str): path of the image directory
        download_path (str): path of directory used to store the desired results 
    
    Returns:
        No return value. Instead, creating a .csv file containing the desired results
    """

	# create a list of filenames
	files = []
	walk_obj = os.walk(image_path)
	dirpath, dirnames, filenames = next(walk_obj)
	files.extend(filenames)

	# create a list of desired result from detector() function
	res_lst = []

	for file in files:
		res_lst.append( detector.detector(os.path.join(image_path, file), color_spec_rgb_dicts) ) 

	# Order a list of dicts
	res_lst = sorted(res_lst, key = lambda k: k['section'])

	with open( os.path.join(download_path, "out.csv") , mode ="w+", encoding = 'utf8', newline = "" ) as output:
		fc = csv.DictWriter(output, fieldnames = res_lst[0].keys())
		fc.writeheader()
		fc.writerows(res_lst)
