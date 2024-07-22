#!/bin/bash

# Set your AWS S3 bucket name and credentials
S3_BUCKET_NAME="llamagon"
AWS_ACCESS_KEY_ID="cam-phong"
AWS_SECRET_ACCESS_KEY="bEY1wc0#"

# Write the AWS credentials to a file
echo $AWS_ACCESS_KEY_ID:$AWS_SECRET_ACCESS_KEY > /etc/passwd-s3fs
chmod 600 /etc/passwd-s3fs

# Mount the S3 bucket
s3fs $S3_BUCKET_NAME /data -o passwd_file=/etc/passwd-s3fs -o url=https://s3.amazonaws.com

# Keep the container running
tail -f /dev/null
