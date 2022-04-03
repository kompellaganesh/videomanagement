import logging
import boto3
from botocore.exceptions import ClientError
import os
from config import  config

def uploadvideoservice(videoname,cast,video,thumbnail):
    return upload_file(video,config.configurations["aws"]["s3bucket"]) and upload_file(thumbnail,config.configurations["aws"]["s3bucket"])

def upload_file(video, bucket):
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_fileobj(video,bucket,video.filename)
        print(response)
    except ClientError as e:
        logging.error(e)
        return False
    return True

