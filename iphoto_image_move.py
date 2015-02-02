import sys
import os.path
import subprocess
from datetime import datetime
import shutil

from PIL import Image
from PIL.ExifTags import TAGS

def time_decode(time_string):
	#2014:09:27 12:11:06
	t = datetime.strptime(time_string, "%Y:%m:%d %H:%M:%S")
	return t.strftime("%Y%m%d_%H%M%S")

def new_file_name(full_path_name):
	ret = {}
	ext_name = os.path.splitext(full_path_name)[1]
	ext_name = ext_name.upper()
	if ext_name == ".JPG":
		img = Image.open(full_path_name)
		exifinfo = img._getexif()
		for tag, value in exifinfo.items():
			decoded = TAGS.get(tag)
			ret[decoded] = value
		return time_decode(ret['DateTime'])

	elif ext_name in [".MOV", ".MP4"]:
		dt = subprocess.check_output('exiftool -s3 -createdate -d "%Y%m%d_%H%M%S" ' + '"%s"' % full_path_name, shell=True)
		return dt.decode().strip()
	elif ext_name in [".MPG", ".PNG", ".GIF"]:
		dt = subprocess.check_output('exiftool -s3 -FileModifyDate -d "%Y%m%d_%H%M%S_%Z" ' + '"%s"' % full_path_name, shell=True)
		return dt.decode().strip()

	
if __name__ == '__main__':

	command = sys.argv[1]
	file_list = sys.argv[2]
	path_to = sys.argv[3]
	
	f = open(file_list)
	files = f.readlines()
	f.close()

	time_list = {}

	count = 0
	
	for i in files:
		count = count + 1
		full_path_name = i.strip()
		ext_name = os.path.splitext(os.path.basename(full_path_name))[1]
		try:
			time_string = new_file_name(full_path_name)
			
		except:
			
			time_string = os.path.splitext(os.path.basename(full_path_name))[0]
			
		#print(full_path_name, "Error!")
		#move to another location remain here
			
		if time_string in time_list.keys():
			time_list[time_string] = time_list[time_string] + 1
		else:
			time_list[time_string] = 0

		if time_list[time_string] == 0:
			final_name = time_string + ext_name
		else:
			final_name = time_string + '-%d' % time_list[time_string] + ext_name

		print("[%.2f]" % (100*count/len(files)),  full_path_name, '->',  final_name)

		if command == "move":
			shutil.move(full_path_name, os.path.join(path_to, final_name))
		
