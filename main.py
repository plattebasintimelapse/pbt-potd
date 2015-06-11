import os, sys, shutil
from PIL import Image

ORIGINAL_IMAGES_DIR 	= "images/originals/"
RESIZED_IMAGES_DIR 		= "images/resized/"
VIDEO_OUTPUT_DIR		= "video/"

def query_yes_no(question, default="yes"):
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        print question + prompt
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print "Please respond with 'yes' or 'no' (or 'y' or 'n')."

def prompt_break():
	print "\n"
	print "-------------------------------------------------"
	print "\n"

def get_string_from_user(prompt):
	print prompt

	n = None
	while n is None:
		a = raw_input("Enter a directory: ")
		n = str(a)
		return n

def make_dir(d):
	if not os.path.exists(d):
		os.makedirs(d)

#-----------------------------------------------------#
# Resizes and renames images in the @param d directory
# @param 	d 		string 		Name of source directory containing images
# @param	name 	string 		Name of the new file, preceeding the extracted four_digits of original file
#-----------------------------------------------------#
def resize_images(d, name):
	src_path = ORIGINAL_IMAGES_DIR + d + "/"
	dest_path = RESIZED_IMAGES_DIR + d + "/"

	make_dir(dest_path)

	dirs = os.listdir( src_path )

	total = 0

	print "\n"
	print "Resizing Images:"
	for file in dirs:
		if os.path.isfile( src_path + file ):
			if file.endswith('.JPG'):
				
				four_digit = file[4:-4]
				img = Image.open( src_path + file )

				width = img.size[0]
				height = img.size[1]
				half_the_width = width / 2
				half_the_height = height / 2

				ASPECT_RATIO = 1.7777777777777777777777777777777778

				half_the_computed_height = width / ASPECT_RATIO / 2

				# Crop from image center
				img_cropped = img.crop((
			        half_the_width - half_the_width,
			        half_the_height - int(half_the_computed_height),
			        half_the_width + half_the_width,
			        half_the_height + int(half_the_computed_height)
			    ))

				img_resized = img_cropped.resize((1280,720), Image.ANTIALIAS)

				img_resized.save(dest_path + name + "_" + four_digit + ".jpg" , 'JPEG', quality=100)
				print "%s%s -> %s%s_%s.jpg" % (src_path, file, dest_path, name, four_digit )
				total += 1

	print "\n"
	print "-------------------------------------------------"
	print "%s images were resized successfully into %s" % (total, dest_path )
	print "-------------------------------------------------"
	print "\n"

#-----------------------------------------------------#
# Creates several timelapse video files from the @param d directory
# Utiliztes ffmpeg command - more info here https://www.ffmpeg.org/
# @param 	d 		string 		Name of source directory containing resized images
# @param	name 	string 		Name of the file preceeding the extracted four_digits of original file
# @param	dest 	string 		Output directory for files
#-----------------------------------------------------#
def create_timelapse(d, name, dest):

	# TODO - COMPILE FFMPEG WITH OGG AND WEBM CODEC - DONE
	# In order to render out .OGG and .WebM for HTML5 video playback, ya gotta compile ffmpeg with --enabled-libtheora and --enabled-libvpx. Google FFMPEG complication guide and there's information there. It'll depend on the system we end up using. I installed with Homebrew on my OSX machine.

	# TODO - MOVE THESE SYSTEM COMMANDS TO SUBMODULES

	full_path = RESIZED_IMAGES_DIR + d + "/"

	os.system("ffmpeg -f image2 -framerate 10 -i " + full_path + name + "_%*.jpg -c:v libx264 -crf 28 -preset medium " + dest + "/" + name + ".mp4")

	os.system("ffmpeg -f image2 -framerate 10 -i " + full_path + name + "_%*.jpg -c:v theora -q:v 7 " + dest + "/" + name + ".ogg")

	os.system("ffmpeg -f image2 -framerate 10 -i " + full_path + name + "_%*.jpg -c:v libvpx -crf 6 -b:v 2M " + dest + "/" + name + ".webm")

	print "\n"
	print "Complete!"
	print "Your videos are located in %s" % (dest)
	print "\n"

	if query_yes_no("Do you want to delete the resized images located in " + full_path +"?", "no"):
		shutil.rmtree( full_path )
		print "Deleting directory %s" % (full_path)
		print "\n"

if __name__ == "__main__":

	print "\n"
	print "Greetings!"
	print "I'll help you make some timelapse videos!"
	print "First, you'll need to resize your images. And then you can use those images to create a video."
	print "\n"

	###################
	## Resize Images ##
	###################
	while query_yes_no("Do you need to resize images?", "no"):

		prompt_break()

		cam_num = get_string_from_user("What camera do you want to resize images for?")
		while not os.path.exists( ORIGINAL_IMAGES_DIR + cam_num + "/" ):
			print "I can't find that camera."
			cam_num = get_string_from_user("Use a valid camera number.")

		resize_images(cam_num, cam_num)


	###################
	## Timelapse Gen ##
	###################
	while query_yes_no("Do you want to create a timelapse video?", "no"):

		prompt_break()

		cam_num = get_string_from_user("What camera do you want to create a timelapse for?")
		while not os.path.exists( RESIZED_IMAGES_DIR + cam_num + "/" ):
			cam_num = get_string_from_user("Enter a valid camera number for images that have already been resized.")

		output_dir = raw_input("Output Folder: ")
		output_dir = VIDEO_OUTPUT_DIR + output_dir

		make_dir(output_dir)

		create_timelapse(cam_num, cam_num, output_dir)


	prompt_break()
	print "END"