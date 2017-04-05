'''
Step 1:  Run 'yum update -y'

Step 2: System Requirements: Install PIP for Python using their repo


Step 3: sudo pip install boto3
Then install boto3: AWS plugin
https://github.com/boto/boto3


Step 4: sudo pip install python-magic
Mime is controled by the 'magic' plugin
https://github.com/ahupp/python-magic


Step 5:  Install AWS CLI and place your aws credentials there
# Install your AWS credentials using the AWS CLI
# http://boto3.readthedocs.io/en/latest/guide/quickstart.html
--- .aws/config ---
[default]
output = json

[profile myprofile]
region = REGION_NAME
s3=
  signature_version = s3
#  addressing_style = path

--- .aws/credentials ---
[myprofile]
aws_access_key_id = <access-key>
aws_secret_access_key = <secret-key>