#!/usr/bin/python3
# coding= utf-8
"""
This is a helper script for storing K8s secrets
"""
import json
import logging
import os
import traceback

try:
    from amagi_library.boto3_helper.client import Client
except ModuleNotFoundError:
    logging.info("Module called internally")
    from boto3_helper.client import Client
try:
    from amagi_library.boto3_helper.s3 import DisplayS3Object
except ModuleNotFoundError:
    logging.info("Module called internally")
    from boto3_helper.s3 import DisplayS3Object


class K8SSecretConfig(object):
    """
        Retrieves configuration from S3 using AWS creds from K8S secrets available as env variable
    """

    @staticmethod
    def aws_api_response_handler(response):
        """
        This method recursively add data into object Dictionary
        :param response: list_objects_response from boto3 s3 client
        """
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            logging.info("Sent successfully")
        else:
            logging.error(f"Response from AWS : {response['ResponseMetadata']}")

    @staticmethod
    def read_from_s3(**kwargs):
        """
        Driving method which will get contents of all the objects in s3
        :return: Returns object dict containing details about s3
        """
        data = None
        try:
            aws_details_str = os.environ["AWS_DETAILS"] if "AWS_DETAILS" in os.environ else None
            aws_details_obj = json.loads(aws_details_str)
            string_data = DisplayS3Object(aws_details=aws_details_obj).object_content(s3_details=kwargs["s3_details"],
                                                                                      object_path=kwargs["s3_details"]
                                                                                      ["object_path"])
            if string_data:
                data = json.loads(string_data)
        except BaseException:
            logging.error(f"Uncaught exception in secret_config.py : {traceback.format_exc()}")
        finally:
            return data

    @staticmethod
    def read_raw_from_s3(**kwargs):
        """
        Driving method which will get contents of all the objects in s3
        :return: Returns object dict containing details about s3
        """
        string_data = None
        try:
            aws_details_str = os.environ["AWS_DETAILS"] if "AWS_DETAILS" in os.environ else None
            aws_details_obj = json.loads(aws_details_str)
            string_data = DisplayS3Object(aws_details=aws_details_obj).object_content(s3_details=kwargs["s3_details"],
                                                                                      object_path=kwargs["s3_details"]
                                                                                      ["object_path"])
        except BaseException:
            logging.error(f"Uncaught exception in secret_config.py : {traceback.format_exc()}")
        finally:
            return string_data