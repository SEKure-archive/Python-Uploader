import os
import datetime
import boto3
import magic
import config
import re

'''
Step 1:  Run 'yum update -y'

Step 2: System Requirements: Install PIP for Python using their repo


Step 3: sudo pip install boto3
Then install boto3: AWS plugin
https://github.com/boto/boto3


Step 4: sudo pip install python-magic
Mime is controled by the 'magic' plugin
https://github.com/ahupp/python-magic


Step 5:  Make a 'config.py' file with aws creds
config.py
    aws_id=''
    aws_secret=''
    aws_s3=''
'''

#  AWS Creds
id = config.aws_id
secret = config.aws_secret
bucketName = config.aws_s3
max_file_size = 100 * 1024   # Kilo Bytes


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
            if os.path.getsize(current_file) > max_file_size:
                print "File too large to upload"
                print "Check Max upload size"
                break

            # No folder structure
            time_stamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            aws_path = filename + "-" + time_stamp

            # Keeps folder structure
            # aws_path = current_file + "-" + time_stamp
            # aws_path = re.sub(upload_dir, "", aws_path)
            upload(current_file, aws_path)



# This Function uploads
def upload(file_path, aws_path):
    mime = magic.from_file(file_path, mime=True)

    s3 = boto3.resource('s3',
                        aws_access_key_id=id,
                        aws_secret_access_key=secret)

    data = open(file_path, 'rb')
    s3.Bucket(bucketName).put_object(Key=aws_path, Body=data, ContentType=mime,
                                     ServerSideEncryption='AES256')
    print "Upload complete"
    print "File path: " + file_path
    print "AWS path: " + aws_path
    print "MIME: " + mime
    print ""


def main():
#  Variables
    real_path = os.path.realpath(__file__)  # Gets Current File
    current_dir = os.path.dirname(real_path)  # Gets Current Directory
    upload_dir = current_dir + "/upload/"
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    archived = current_dir + "/archived" + "-" + time_stamp + "/"


    check_folder(upload_dir)
    recurse(upload_dir)
    move_files(upload_dir, archived)
    check_folder(upload_dir)

main()

