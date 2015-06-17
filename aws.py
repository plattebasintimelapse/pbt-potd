import os
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import boto
from secrets import AWS_KEY, AWS_SECRET

CONN = S3Connection(AWS_KEY, AWS_SECRET)

def send_file_to_S3(file,bucket):
    k = Key(bucket)
    k.key = file
    k.set_contents_from_filename(file)
    k.set_acl('public-read')

def send_dir_to_S3(src_path,bucket):
    d = os.listdir( src_path )
    for file in d:
        if os.path.isfile( src_path + file ):
            file_path = src_path + file
            k = Key(bucket)
            k.key = file_path
            k.set_contents_from_filename(file_path)
            k.set_acl('public-read')

def delete_file_from_S3(file,bucket):
    k = Key(bucket)
    k.key = file
    bucket.delete_key(k)

def delete_bucket(bucket):
	for key in bucket.list():
		key.delete()

	CONN.delete_bucket(bucket)

def create_bucket(name):
    bucket = CONN.create_bucket(name)
    bucket.make_public()

def get_bucket(name):
    nonexistent = CONN.lookup(name)
    if nonexistent is None:
        print "No such bucket!"
        print "Creating bucket " + name
        create_bucket(name)
        bucket = CONN.get_bucket(name)
        return bucket
    else:
        bucket = CONN.get_bucket(name)
        return bucket