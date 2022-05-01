import boto3
from flask import Flask, jsonify, request, Response, stream_with_context
from werkzeug.datastructures import Headers
import re
from config import  config


bucket_name = config.configurations["aws"]["s3bucket"]
service = Flask(__name__)

content_type="video/mp4"
def streamvideo():
    args = request.args
    print(args)
    key = args.get("video")
    print(key)
    key=key.replace(config.configurations['aws']['cdnlink']+"/","")
    print(key)
    storage = boto3.client('s3')
    media_stream = storage.get_object(Bucket=bucket_name, Key=key)
    full_content = media_stream['ContentLength']
    headers = Headers()
    status = 200
    range_header = request.headers.get('Range', None)
    if range_header:
        byte_start, byte_end, length = get_byte_range(range_header)

    headers.add('Content-Type', content_type)
    headers.add('Content-Length', media_stream['ContentLength'])
    response = Response(
        stream_with_context(media_stream['Body'].iter_chunks()),
        mimetype=content_type,
        content_type=content_type,
        headers=headers,
        status=status
        )
    return response


def get_byte_range(range_header):
    g = re.search('(\d+)-(\d*)', range_header).groups()
    byte1, byte2, length = 0, None, None
    if g[0]:
        byte1 = int(g[0])
    if g[1]:
        byte2 = int(g[1])
        length = byte2 + 1 - byte1

    return byte1, byte2, length