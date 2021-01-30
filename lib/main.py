import sys
import re
import os
from lib import detector
import csv
import collections

def main(image_path, download_path):

	# create a list of filenames
	files = []
	walk_obj = os.walk(image_path)
	(dirpath, dirnames, filenames) = next(walk_obj)
	files.extend(filenames)

	# create a list of desired result from detector() function
	res_lst = []

	for file in files:
		res_lst.append( detector.detector(os.path.join(image_path, file)) ) # path+"/"+cfile

	# Order a list of dicts
	res_lst = sorted(res_lst, key = lambda k: k['section'])

	with open( os.path.join(download_path, "out.csv") , mode ="w+", encoding = 'utf8', newline = "" ) as output:
		fc = csv.DictWriter(output, fieldnames = res_lst[0].keys())
		fc.writeheader()
		fc.writerows(res_lst)
