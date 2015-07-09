from django.core.management.base import BaseCommand, CommandError
from timelapse.models import Camera, Photos, TimeLapse
import os, sys, shutil, datetime, string, time, dropbox
from secrets import DROPBOX_TOKEN
from PIL import Image

CAM_DIRECTORIES = ["002","003","006","008","016","017","018","021","027","029","030","031","034","036","037","038","039","040","041","042","048","050","051","055","056","132","232"]

ORIGINAL_IMAGES_DIR     = "cameras/"
RESIZED_IMAGES_DIR         = "images/"
VIDEO_OUTPUT_DIR        = "video/"

t                         = datetime.date.today()
TODAY                     = str(t)

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        #First get logged into DropBox

        client = dropbox.client.DropboxClient(DROPBOX_TOKEN)

        for direc in directories:
            if not os.path.exists(root + direc):
                os.makedirs(root + direc)

        #Now let's download some files.

        folder_metadata = client.metadata('/cameras/')

        for object in folder_metadata['contents']:
            path = object['path']
            picture_metadata = client.metadata(path)
            for picture in picture_metadata['contents']:
                pic = picture['path']
                picfile = pic[1:]
                if os.path.exists(picfile):
                    print "Skipping %s" % picfile
                else:
                    try:
                        print "Downloading %s" % picfile
                        f, metadata = client.get_file_and_metadata(pic)
                        out = open(picfile, 'a')
                        out.write(f.read())
                        
                        
                        
                        
                        out.close()
                        time.sleep(2)
                    except IOError:
                        print "Error when downloading %s" % picfile
                        pass
        
        
        
        def resize_images(d, name):
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
                        
                                img_resized = img_cropped.resize((1280,720), Image.ANTIALIAS, exif=exif)
                        
                                img_resized.save( full_dest_path , 'JPEG', quality=100)
                                print "%s%s -> %s" % (src_path, file, full_dest_path )
                                total += 1
    
            print "\n"
            print "-------------------------------------------------"
            print "%s images were resized successfully into %s" % (total, dest_path )
            print "-------------------------------------------------"
            print "\n"