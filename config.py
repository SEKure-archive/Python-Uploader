# Install your AWS credentials using the AWS CLI
# http://boto3.readthedocs.io/en/latest/guide/quickstart.html
# See read me file


bucketName = "sekure-archive"
lambdaUpload = "upload-lambda"
sqsDownload = "download"
aws_cli_profile_name = "default"
# region = "us-east-1"
max_file_size = 100 * 1024   # Kilo Bytes
base_dir = ""  # Defaults to current driectory if ""
