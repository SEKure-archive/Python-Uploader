import os
import datetime
import boto3
import magic
import config
import re
import json


def main():
    if (config.base_dir == ""):
        real_dir = os.path.realpath(__file__)
        current_dir = os.path.dirname(real_dir)  # Where files archived/ restoreLocation
        base_dir = current_dir + "/files"
    else:
        base_dir = config.base_dir
    restoreDir = base_dir + "/restored"
    hash_id = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    restoreDir = restoreDir + '/restored-' + hash_id
    # check_folder(restoreDir)


    # conn = boto.sqs.connect_to_region(
    #     "us-east-1",
    #     aws_access_key_id = '<aws access key>',
    #     aws_secret_access_key = '<aws secret key>')

    s3 = boto3.client('s3')
    sqs = boto3.resource('sqs')
    q = sqs.get_queue_by_name(QueueName=config.sqsDownload)
    print "Connecting to AWS..."
    print "Checking for files...."
    print "This will take a minute...."

    while True:
        messages_to_delete = []
        for message in q.receive_messages(MessageAttributeNames=['filename', 'directory', 's3path']):
            # process message body
            if message.message_attributes is not None:
                name = message.message_attributes.get('filename').get('StringValue')
                location = message.message_attributes.get('directory').get('StringValue')
                s3path = message.message_attributes.get('s3path').get('StringValue')

                if location[0] == "/":
                    r_dir = restoreDir + location
                else:
                    r_dir =  restoreDir + "/" + location

                check_folder(r_dir)

                if name[0] == "/":
                    r_path = r_dir + name
                else:
                    r_path = r_dir + "/" + name

                # r_path = os.path.join(r_dir, name)

                print "Restoring File: " + name
                with open(r_path, 'wb') as data:
                    s3.download_fileobj(config.bucketName, s3path, data)
                    # message.delete()

            messages_to_delete.append({
                'Id': message.message_id,
                'ReceiptHandle': message.receipt_handle
            })

        # if you don't receive any notifications the
        # messages_to_delete list will be empty
        if len(messages_to_delete) <= 0:
            break
        # delete messages to remove them from SQS queue
        # handle any errors
        else:
            delete_response = q.delete_messages(
                Entries=messages_to_delete)


def check_folder(dir, ):
    if not os.path.exists(dir):
        os.makedirs(dir)


main()
