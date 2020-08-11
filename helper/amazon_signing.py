#!/usr/bin/python3
# coding= utf-8
"""
This scripts actually sign requests for Amazon API call
xref : https://docs.amazonaws.cn/en_us/general/latest/gr/sigv4-signed-request-examples.html
"""

import hashlib
import hmac
import logging

import boto3
from botocore.config import Config


def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()


def get_signature_key(key, date_stamp, region_name, service_name):
    k_date = sign(('AWS4' + key).encode(), date_stamp)
    k_region = sign(k_date, region_name)
    k_service = sign(k_region, service_name)
    k_signing = sign(k_service, 'aws4_request')
    return k_signing


def get_signed_url(expires_in, bucket, obj, access_key=None, secret_key=None, region='us-east-1'):
    """
    Generate a signed URL
    :param region:      AWS Region
    :param secret_key:  S3 Secret Key
    :param access_key:  S3 Access Key
    :param expires_in:  URL Expiration time in seconds
    :param bucket:      S3 Bucket
    :param obj:         S3 Key name
    :return:            Signed URL
    """
    s3_cli = boto3.client("s3", aws_access_key_id=access_key,
                          aws_secret_access_key=secret_key,
                          region_name=region, config=Config(signature_version='s3v4',
                                                            s3={'addressing_style': 'virtual'}))
    return s3_cli.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': obj},
                                         ExpiresIn=expires_in)


if __name__ == "__main__":
    # LOGGING #
    logging_format = "%(asctime)s::%(funcName)s::%(levelname)s:: %(message)s"
    logging.basicConfig(format=logging_format, level=logging.INFO, datefmt="%Y/%m/%d:%H:%M:%S:%Z:%z")
    logger = logging.getLogger(__name__)
