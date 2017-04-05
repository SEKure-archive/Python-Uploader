import os
import datetime
import boto3
import magic
import config
import re

def main():
#  Variables
    if (config.base_dir == ""):
        real_dir = os.path.realpath(__file__)
        current_dir = os.path.dirname(real_dir) # Where files archived/ restoreLocation
        base_dir = current_dir + "/files"
    else:
        base_dir = config.base_dir
    upload_dir = base_dir + "/upload/"
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    archived = base_dir + "/archived" + "-" + time_stamp + "/"

    check_folder(base_dir)
    check_folder(upload_dir)
    recurse(upload_dir)
    # move_files(upload_dir, archived)
    check_folder(upload_dir)


def check_folder(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def move_files(file_path,  new_name):
    new_path = re.sub(file_path, new_name, file_path)
    print new_path
    os.rename(file_path, new_path)

def recurse(base_folder):
    for root, directories, filenames in os.walk(base_folder):
        for directory in directories:
            os.path.join(root, directory)

        for filename in filenames:
            current_file = os.path.join(root, filename)
            file_size = os.path.getsize(current_file)
            if file_size > config.max_file_size:
                print "File too large to upload"
                print "Check Max upload size"
                break
            else:
                upload(current_file, s3_path, file_size)



# This Function uploads
def upload(file_path, aws_path, file_size):
    hash_id = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    s3_path = filename + "-" + hash_id
    mime = magic.from_file(file_path, mime=True)

    # Upload File to S3 as with encryption
    s3 = boto3.resource('s3')
    data = open(file_path, 'rb')
    s3.Bucket(config.bucketName).put_object(Key=aws_path, Body=data, ContentType=mime, ServerSideEncryption='AES256')


    print "Upload complete"
    print "File path: " + file_path
    print "AWS path: " + aws_path
    print "MIME: " + mime
    print ""
main()
