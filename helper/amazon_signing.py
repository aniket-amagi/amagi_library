#!/usr/bin/python3
# coding= utf-8
"""
This scripts actually sign requests for Amazon API call
xref : https://docs.amazonaws.cn/en_us/general/latest/gr/sigv4-signed-request-examples.html
"""

import hashlib
import hmac
import logging
import sys
from datetime import datetime

import boto3
from botocore.config import Config


def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def get_signature_key(key, date_stamp, region_name, service_name):
    k_date = sign(("AWS4" + key).encode(), date_stamp)
    k_region = sign(k_date, region_name)
    k_service = sign(k_region, service_name)
    k_signing = sign(k_service, "aws4_request")
    return k_signing


def get_signed_url(expires_in, bucket, obj, access_key=None, secret_key=None, region="us-east-1"):
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
                          region_name=region, config=Config(signature_version="s3v4",
                                                            s3={"addressing_style": "virtual"}))
    return s3_cli.generate_presigned_url("get_object", Params={"Bucket": bucket, "Key": obj},
                                         ExpiresIn=expires_in)


def get_signed_url_from_cloudfront_url(access_key, secret_key, host, endpoint, canonical_uri, region="us-east-1",
                                       service="s3", method="GET"):
    """
    Generate a signed URL
    # ************* REQUEST VALUES *************
    # method = "GET"
    # service = "s3"
    # host = "s3_bucket.s3-us-west-1.amazonaws.com"
    # region = "us-west-1"
    # endpoint = "https://s3_bucket.s3-us-west-1.amazonaws.com/path1/file1.mp4"
    # canonical_uri = "/path1/file1.mp4"

    :param access_key: S3 Access Key
    :param secret_key: S3 Secret Key
    :param host: Host basename
    :param endpoint: Full URL
    :param canonical_uri: Canonical URI
    :param region: AWS Region
    :param service: AWS Service
    :param method: HTTP Method
    """

    request_parameters = ""

    # Read AWS access key from env. variables or configuration file. Best practice is NOT
    # to embed credentials in code.
    if access_key is None or secret_key is None:
        logging.error("No access key is available.")
        sys.exit()

    # Create a date for headers and the credential string
    t = datetime.utcnow()
    amzdate = t.strftime("%Y%m%dT%H%M%SZ")
    datestamp = t.strftime("%Y%m%d")  # Date w/o time, used in credential scope

    # ************* TASK 1: CREATE A CANONICAL REQUEST *************
    # http://docs.aws.amazon.com/general/latest/gr/sigv4-create-canonical-request.html

    # Step 1 is to define the verb (GET, POST, etc.)--already done.

    # Step 2: Create canonical URI--the part of the URI from domain to query
    # string (use "/" if no path)
    if not canonical_uri:
        canonical_uri = "/"

    # Step 3: Create the canonical query string. In this example (a GET request),
    # request parameters are in the query string. Query string values must
    # be URL-encoded (space=%20). The parameters must be sorted by name.
    # For this example, the query string is pre-formatted in the request_parameters variable.
    canonical_querystring = request_parameters

    # Step 4: Create the canonical headers and signed headers. Header names
    # must be trimmed and lowercase, and sorted in code point order from
    # low to high. Note that there is a trailing \n.

    payload_hash = hashlib.sha256("".encode("utf-8")).hexdigest()

    canonical_headers = "host:" + host + "\n" + "x-amz-content-sha256:" + payload_hash + "\n" +\
                        "x-amz-date:" + amzdate + "\n"

    # Step 5: Create the list of signed headers. This lists the headers
    # in the canonical_headers list, delimited with ";" and in alpha order.
    # Note: The request can include any headers; canonical_headers and
    # signed_headers lists those that you want to be included in the
    # hash of the request. "Host" and "x-amz-date" are always required.
    signed_headers = "host;x-amz-content-sha256;x-amz-date"

    # Step 6: Create payload hash (hash of the request body content). For GET
    # requests, the payload is an empty string ("").

    # Step 7: Combine elements to create canonical request
    canonical_request = method + "\n" + canonical_uri + "\n" + canonical_querystring + "\n" + canonical_headers +\
                        "\n" + signed_headers + "\n" + payload_hash

    # ************* TASK 2: CREATE THE STRING TO SIGN*************
    # Match the algorithm to the hashing algorithm you use, either SHA-1 or
    # SHA-256 (recommended)
    algorithm = "AWS4-HMAC-SHA256"
    credential_scope = datestamp + "/" + region + "/" + service + "/" + "aws4_request"
    string_to_sign = algorithm + "\n" + amzdate + "\n" + credential_scope + "\n" + hashlib.sha256(
        canonical_request.encode("utf-8")).hexdigest()

    # ************* TASK 3: CALCULATE THE SIGNATURE *************
    # Create the signing key using the function defined above.
    signing_key = get_signature_key(secret_key, datestamp, region, service)

    # Sign the string_to_sign using the signing_key
    signature = hmac.new(signing_key, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

    # ************* TASK 4: ADD SIGNING INFORMATION TO THE REQUEST *************
    # The signing information can be either in a query string value or in
    # a header named Authorization. This code shows how to use a header.
    # Create authorization header and add to request headers
    authorization_header = algorithm + " " + "Credential=" + access_key + "/" + credential_scope + ", " + \
                           "SignedHeaders=" + signed_headers + ", " + "Signature=" + signature

    # The request can include any headers, but MUST include "host", "x-amz-date",
    # and (for this scenario) "Authorization". "host" and "x-amz-date" must
    # be included in the canonical_headers and signed_headers, as noted
    # earlier. Order here is not significant.
    # Python note: The "host" header is added automatically by the Python "requests" library.
    headers = {"x-amz-date": amzdate, "Authorization": authorization_header, "x-amz-content-sha256": payload_hash}

    # ************* SEND THE REQUEST *************
    return endpoint, headers
