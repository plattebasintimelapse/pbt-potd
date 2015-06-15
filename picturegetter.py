import os, string
import time
import dropbox
from picturegetter_settings import token

#First get logged into DropBox

client = dropbox.client.DropboxClient(token)

#Now let's make sure all the directories we need are there.

directories = ["cameras/002","cameras/003","cameras/006","cameras/008","cameras/016","cameras/017","cameras/018","cameras/021","cameras/027", "cameras/029","cameras/030","cameras/031","cameras/034","cameras/036","cameras/037","cameras/038","cameras/039","cameras/040","cameras/041","cameras/042","cameras/048","cameras/050","cameras/051","cameras/055","cameras/132","cameras/232"]

for direc in directories:
    if not os.path.exists(direc):
        os.makedirs(direc)

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
            print "Downloading %s" % picfile
            f, metadata = client.get_file_and_metadata(pic)
            out = open(picfile, 'a')
            out.write(f.read())
            out.close()
            time.sleep(2)