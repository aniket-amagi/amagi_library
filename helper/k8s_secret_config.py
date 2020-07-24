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
            logging.error("Response from get : " + str(response["ResponseMetadata"]))

    def read_from_s3(self, **kwargs):
        """
        Driving method which will get contents of all the objects in s3
        :return: Returns object dict containing details about s3
        """
        self.s3_details = kwargs["s3_details"]
        aws_details_str = os.environ['AWS_DETAILS'] if "AWS_DETAILS" in os.environ else None
        if not aws_details_str:
            return None
        aws_details_obj = None
        try:
            aws_details_obj = json.loads(aws_details_str)
            obj = DisplayS3Object(aws_details=aws_details_obj)
            data = obj.object_content(s3_details=kwargs['s3_details'], object_path=kwargs['s3_details']['object_path'])
            if data:
                return json.loads(data)
        except BaseException:
            logging.error("Uncaught exception in secret_config.py " + traceback.format_exc())
        finally:
            raise BaseException("Problem in secret_config.py" + aws_details_obj)
