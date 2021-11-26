import logging
import os
import random
import sys
from time import sleep

import boto3
import botocore

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

##############
## Vars init #
##############
# Object storage
access_key = os.environ['AWS_ACCESS_KEY_ID']
secret_key = os.environ['AWS_SECRET_ACCESS_KEY']
service_point = os.environ['SERVICE_POINT']

# Buckets
bucket_source_name = os.environ['BUCKET_SOURCE']
bucket_destination_name = os.environ['BUCKET_BASE_NAME']


# Delay between images
seconds_wait = float(os.environ['SECONDS_WAIT'])

# Resources
ssl_verify = os.environ['STORAGE_SSL_VERIFY']

s3 = None
    
if ssl_verify == True:
  s3 = boto3.client('s3',
              endpoint_url = service_point,
              aws_access_key_id = aws_access_key_id,
              aws_secret_access_key = aws_secret_access_key,
              region_name = region_name,
              config=botocore.client.Config(signature_version = 's3'))
else:
  s3 = boto3.client('s3',
              endpoint_url = service_point,
              aws_access_key_id = aws_access_key_id,
              aws_secret_access_key = aws_secret_access_key,
              region_name = region_name,
              verify = False,
              config=botocore.client.Config(signature_version = 's3'))

########
# Code #
########
def copy_file(source_bucket_name, source_image_key, destination_bucket, destination_image_name):
  """Copies an object from a URL source to a destination bucket."""

  copy_source = {
    'Bucket': source_bucket_name,
    'Key': source_image_key
  }
  s3.copy(copy_source, destination_bucket, destination_image_name)


# Populate source images lists
pneumonia_images=[]
for item in s3.list_objects_v2(Bucket=bucket_source_name, Prefix='PNEUMONIA/')['Contents']:
    pneumonia_images.append(item['Key'])
logging.info(f"List created: PNEUMONIA images.")    
normal_images=[]
for item in s3.list_objects_v2(Bucket=bucket_source_name, Prefix='NORMAL/')['Contents']:
    normal_images.append(item['Key'])
logging.info(f"List created: NORMAL images.")    
# Main loop
while seconds_wait != 0: #This allows the container to keep running but not send any image if parameter is set to 0
    logging.info(f"Random select image to copy")
    rand_type = random.randint(1,10)
    if rand_type <= 8: # 80% of time, choose a normal image
        image_key = normal_images[random.randint(0,len(normal_images)-1)]
    else:
        image_key = pneumonia_images[random.randint(0,len(pneumonia_images)-1)]
    image_name = image_key.split('/')[-1]
    copy_file(bucket_source_name, image_key, bucket_destination_name, image_name)
    logging.info(f"Image {image_key} copied to destination")
    sleep(seconds_wait)

# Dirty hack to keep container running even when no images are to be copied
os.system("tail -f /dev/null")
