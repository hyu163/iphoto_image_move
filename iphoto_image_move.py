import sys
import os.path
import subprocess
from datetime import datetime

from PIL import Image
from PIL.ExifTags import TAGS

def time_decode(time_string):
	#2014:09:27 12:11:06
	t = datetime.strptime(time_string, "%Y:%m:%d %H:%M:%S")
	return t.strftime("%Y%m%d_%H%M%S")

def new_file_name(full_path_name):
	ret = {}
	img = Image.open(full_path_name)
	exifinfo = img._getexif()
	for tag, value in exifinfo.items():
		decoded = TAGS.get(tag)
		ret[decoded] = value
	return ret
	
if __name__ == '__main__':

	file_list = sys.argv[1]
	path_to = sys.argv[2]
	
	f = open(file_list)
	files = f.readlines()
	f.close()

	time_list = {}
	
	for i in files:
		
		full_path_name = i.strip()
		ext_name = os.path.splitext(os.path.basename(full_path_name))[1]
		try:
			time_string = new_file_name(full_path_name)['DateTime']
			time_string = time_decode(time_string)
			
		except:
			time_string = os.path.splitext(os.path.basename(full_path_name))[0]
			
		#print(full_path_name, "Error!")
		#move to another location remain here
			
		if time_string in time_list.keys():
			time_list[time_string] = time_list[time_string] + 1
		else:
			time_list[time_string] = 0
				
		print(full_path_name, time_string,
			  time_string + 'x'*time_list[time_string] + ext_name)
		
