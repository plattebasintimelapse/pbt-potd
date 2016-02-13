import os, string
import time
import dropbox
from secrets import DROPBOX_TOKEN


def download_images(root, directories):
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
