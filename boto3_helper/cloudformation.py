#!/usr/bin/python3
# coding= utf-8
"""
This scripts actually creates cloud-formation stack
"""
import logging

from boto3_helper.client import Client


class CloudFormationCreateStack(object):
    """
    This Class creates cloud-formation stack
    """

    def __init__(self, **kwargs):
        # Required variable to drive this Class, expected to be provided from parent Object
        self.aws_details = None
        self.__dict__.update(kwargs)

        self.cloudformation_instance = Client(aws_details=self.aws_details).return_client(service_name="cloudformation")
        logging.debug("Instance variables for CloudFormationCreateStack : " + str(self.__dict__))

    def create_stack(self, **kwargs):
        """
        This method is scrub of from old project to submit batch jobs without MAPSOR API
        :param kwargs: This parameter contains information from environemnt
        :return: submits a batch job
        """
        pass


if __name__ == "__main__":
    # LOGGING #
    logging_format = "%(asctime)s::%(funcName)s::%(levelname)s:: %(message)s"
    logging.basicConfig(format=logging_format, level=logging.INFO, datefmt="%Y/%m/%d:%H:%M:%S:%Z:%z")
    logger = logging.getLogger(__name__)
