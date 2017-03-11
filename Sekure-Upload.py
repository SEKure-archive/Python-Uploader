import os
import datetime
import boto3
import config
import re


# Run 'yum update -y'
# System Requirments: Install PIP for Python using their repo
# Then install boto3: AWS plugin
# sudo pip install boto3
#  https://github.com/boto/boto3


#  Requires:  Make a 'config.py' file with aws creds
# aws_id=
# aws_secret_access_key=
# aws_s3=

id = config.aws_id
secret = config.aws_secret_access_key
bucketName = config.aws_s3


#  Variables
real_path = os.path.realpath(__file__)  # Gets Current File
current_dir = os.path.dirname(real_path)  # Gets Current Directory
upload_dir = current_dir + "/upload/"
time_stamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
archived = current_dir + "/archived" + "-" + time_stamp + "/"



def check_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def move_files(file_path,  new_name):
    new_path = re.sub(file_path, new_name, file_path)
    print new_path
    os.rename(file_path, new_path)

def recurse(base_folder):
    for root, directories, filenames in os.walk(base_folder):
        for directory in directories:
            dir = os.path.join(root, directory)
            # print dir

        for filename in filenames:
            current_file = os.path.join(root, filename)
            aws_path = current_file + "-" +time_stamp
            aws_path = re.sub(upload_dir, "", aws_path)
            print current_file
            print aws_path
            upload(current_file, aws_path)

# This Function uploads
def upload(file_path, aws_path):
    s3 = boto3.resource('s3',
                        aws_access_key_id=id,
                        aws_secret_access_key=secret)
    data = open(file_path, 'rb')
    s3.Bucket(bucketName).put_object(Key=aws_path, Body=data, ContentType='text/plain',
                                     ServerSideEncryption='AES256')


check_folder(upload_dir)
recurse(upload_dir)
move_files(upload_dir, archived)
check_folder(upload_dir)



