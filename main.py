import os, sys, shutil, datetime
from PIL import Image
import picturegetter, aws
from PIL.ExifTags import TAGS
from django.utils import timezone
from django.core.files import File

# THIS IS HACKY AS SHIT AND YOU'LL NEED TO CHANGE IT FOR YOUR OWN PATHING PURPOSES
proj_path = "/home/pi/pbt-potd/potd"
#END HACKY AS SHIT PART


# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "potd.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from timelapse.models import Camera, Photo, TimeLapse

AWS_BUCKET_NAME            = "pbt-potd"

ORIGINAL_IMAGES_DIR     = "cameras/"
RESIZED_IMAGES_DIR         = "images/"
VIDEO_OUTPUT_DIR        = "video/"

t                         = datetime.date.today()
TODAY                     = str(t)

CAM_DIRECTORIES = ["002","003","006","008","016","017","018","021","027","029","030","031","034","036","037","038","039","040","041","042","048","050","055","056","062","063","064","065","132","232"]

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

def delete_dir(d):
    if os.path.exists(d):
        shutil.rmtree( d )
        print "Deleting directory %s" % (d)
    else:
        print "%s does not exists" % (d)

def is_non_zero_file(fpath):
    return True if os.path.isfile(fpath) and os.path.getsize(fpath) > 0 else False

def get_count_files_in_directory(path):
      list_dir = []
      list_dir = os.listdir(path)
      count = 0
      for file in list_dir:
          count += 1
      
      return count

#-----------------------------------------------------#
# Resizes and renames images in the @param d directory
# @param     d         string         Name of source directory containing images
# @param    name     string         Name of the new file, preceeding the extracted four_digits of original file
#-----------------------------------------------------#
def resize_images(d, name):
    try:
        src_path = ORIGINAL_IMAGES_DIR + d + "/"
        dest_path = RESIZED_IMAGES_DIR + d + "/" + TODAY + "/"
    
        make_dir(dest_path)
    
        dirs = os.listdir( src_path )
    
        total = 0
    
        print "\n"
        print "Resizing Images:"
        for file in dirs:
            if os.path.isfile( src_path + file ):
                if file.endswith('.JPG') or file.endswith('.jpg'): # only process jpgs.
                
                    four_digit = file[4:-4] # four digit string in file name
                    full_dest_path = dest_path + name + "_" + four_digit + ".jpg"
                
                    if os.path.exists(full_dest_path):
                        print "Already resized %s" % full_dest_path
                    else:
                        if is_non_zero_file( src_path + file ): # skip partially download files
                        
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
                        
                            exif = img.info['exif']
                        
                            img_resized = img_cropped.resize((1280,720), Image.ANTIALIAS)
                        
                            img_resized.save( full_dest_path , 'JPEG', quality=85, exif=exif)
                            print "%s%s -> %s" % (src_path, file, full_dest_path )
                            total += 1
                        
                            exdate = datetime.datetime.strptime(img._getexif()[36867], "%Y:%m:%d %H:%M:%S")
                            exdate = timezone.make_aware(exdate, timezone.get_current_timezone())
                            f = File(open(full_dest_path, 'r'))
                            try:
                                cam = Camera.objects.get(number=name)
                                pic = Photo(camera=cam, photo=f, photo_datetime=exdate)
                                pic.photo.save(full_dest_path,f)
                                pic.save()
                                print "Saved a photo into the backend"
                            except:
                                pass
    except:
        pass                    
    
    print "\n"
    print "-------------------------------------------------"
    print "%s images were resized successfully into %s" % (total, dest_path )
    print "-------------------------------------------------"
    print "\n"

#-----------------------------------------------------#
# Creates several timelapse video files from the @param d directory
# Utiliztes ffmpeg command - more info here https://www.ffmpeg.org/
# @param     d         string         Name of source directory containing resized images
# @param    name     string         Name of the file preceeding the extracted four_digits of original file
#-----------------------------------------------------#
def create_timelapse(d, name):
    
    # TODO - COMPILE FFMPEG WITH OGG AND WEBM CODEC - DONE
    # In order to render out .OGG and .WebM for HTML5 video playback, ya gotta compile ffmpeg with --enabled-libtheora and --enabled-libvpx. Google FFMPEG complication guide and there's information there. It'll depend on the system we end up using. I installed with Homebrew on my OSX machine.
    
    # TODO - MOVE THESE SYSTEM COMMANDS TO SUBMODULES
    
    output_dir = VIDEO_OUTPUT_DIR + d + "/" + TODAY + "/"
    make_dir(output_dir)
    
    img_dir = RESIZED_IMAGES_DIR + d + "/" + TODAY + "/"
    
    num_of_images_in_dir = get_count_files_in_directory(img_dir)
    
    if ( 0 < num_of_images_in_dir <= 10 ):
        speed = str(2)
    elif ( 10 < num_of_images_in_dir <= 20 ):
        speed = str(4)
    elif ( 20 < num_of_images_in_dir <= 30 ):
        speed = str(8)
    else:
        speed = str(10)
    
    if (num_of_images_in_dir != 0 ):
        os.system("/usr/local/bin/ffmpeg -y -f image2 -framerate " + speed + " -i " + img_dir + name + "_%*.jpg -c:v libx264 -crf 28 -preset medium " + output_dir + name + ".mp4")
        #os.system("ffmpeg -y -f image2 -framerate " + speed + " -i " + img_dir + name + "_%*.jpg -c:v theora -q:v 7 " + output_dir + name + ".ogg")
        #os.system("ffmpeg -y -f image2 -framerate " + speed + " -i " + img_dir + name + "_%*.jpg -c:v libvpx -crf 6 -b:v 2M " + output_dir + name + ".webm")
        
        moviepath = output_dir + name + ".mp4"
        f = File(open(moviepath, 'r'))
        try:
            cam = Camera.objects.get(number=name)
            movietime = datetime.datetime.now()
            vid = TimeLapse(camera=cam, movie=f, movie_date=movietime)
            vid.movie.save(moviepath,f)
            vid.save()
            print "Timelapse movie for %s saved into the backend!" % cam
        except:
            pass
        
        print "\n"
        print "Complete!"
        print "Your videos are located in %s" % (output_dir)
        print "\n"

if __name__ == "__main__":
    
#    print "\n"
#    print "Greetings!"
#    print "I'll help you make some timelapse videos!"
#    print "First, you'll need to resize your images. And then you can use those images to create a video."
#    print "\n"
    
    ##################################
    ## Download Images from Dropbox ##
    ##        every 15 mins         ##
    ##################################
#    while query_yes_no("Do you want to download images from Dropbox? \nIt may take a long while.", "no"):
    picturegetter.download_images(ORIGINAL_IMAGES_DIR, CAM_DIRECTORIES)
    
    ##################################
    ## Delete Previous Weeks Images ##
    ##        each morning          ##
    ##################################
    
    ###################
    ## Resize Images ##
    ##   every hour  ##
    ###################
    for cam in CAM_DIRECTORIES:
        resize_images(cam, cam)
    
    ##########################
    ## Upload Images to AWS ##
    ##      every hour      ##
    ##########################
    # for cam in CAM_DIRECTORIES:
    #     aws.send_dir_to_S3( RESIZED_IMAGES_DIR + cam + "/" + TODAY + "/", aws.get_bucket(AWS_BUCKET_NAME) )
    
    ###################
    ## Timelapse Gen ##
    ##   each night  ##
    ###################
    now = datetime.datetime.now()
    if now.hour == 22:
        for cam in CAM_DIRECTORIES:
            create_timelapse(cam, cam)
    else:
        pass
    
    #############################
    ## Upload Timelapse to AWS ##
    ##        each night       ##
    #############################
    #for cam in CAM_DIRECTORIES:
    #    aws.send_dir_to_S3( VIDEO_OUTPUT_DIR + cam + "/" + TODAY + "/", aws.get_bucket(AWS_BUCKET_NAME) )
    
    prompt_break()
    print "END"
