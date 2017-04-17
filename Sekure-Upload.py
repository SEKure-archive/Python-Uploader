import os
import datetime
import boto3
import magic
import config
import re
import json

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
    move_files(upload_dir, archived)
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
                print "Error: " + current_file
            else:
                upload(current_file, filename, root, file_size, base_folder)



# This Function uploads
def upload(file_path, filename, directory, file_size, base_folder):
    localdir = os.path.relpath(directory, base_folder )
    localdir = '/' + localdir
    hash_id = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    s3_path = filename + "-" + hash_id
    s3_path.replace(" ", "-")
    mime = magic.from_file(file_path, mime=True)

    # Json for lambda
    payload = {
        "folder": localdir,
        "name": filename,
        "mime": mime,
        "size": file_size,
        "created": time_stamp,
        "s3": s3_path
    }
    print "s3 path"
    print s3_path

    # Upload File to S3 as with encryption
    s3 = boto3.resource('s3')
    data = open(file_path, 'rb')
    s3.Bucket(config.bucketName).put_object(Key=s3_path, Body=data, ContentType=mime, ServerSideEncryption='AES256')


    client = boto3.client('lambda')
    response = client.invoke(
        FunctionName=config.lambdaUpload,
        InvocationType="RequestResponse",
        LogType='Tail',
        Payload=json.dumps(payload)
    )
    print(response)


main()
print "Upload complete"
