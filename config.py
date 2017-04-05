# Install your AWS credentials using the AWS CLI
# http://boto3.readthedocs.io/en/latest/guide/quickstart.html
# See read me file


bucketName = "sekure-archive"
aws_cli_profile_name = "default"
# region = "us-east-1"


max_file_size = 100 * 1024   # Kilo Bytes
base_dir = ""  # Defaults to current driectory if ""
'''
#################  File Location ############################
restoreLocation=$(echo "${PWD}/files")
uploadDir=$(echo "${restoreLocation}/upload")
archivedDir=$(echo "${restoreLocation}/archived")
####################  AWS ###############################
bucketName="sekure-archive"
region="us-east-1"
sqsUrl="https://sqs.us-east-1.amazonaws.com/373886653085/"
sqsDownload="download"  #queue name
maxSize=90000  #Max size of file in bytes
ec2IP="https://52.2.133.118"
####################  AWS ###############################
'''
