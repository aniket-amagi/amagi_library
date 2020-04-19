#!/usr/bin/python3
# coding= utf-8
"""
This scripts creates an S3 Client Instance
"""
import logging
import traceback

import boto3

from amagi_library.boto3_helper.arn_session import assumed_role_session


class Client(object):
    """
        This Class handles creation s3 client
    """

    def __init__(self, **kwargs):
        self.aws_details = None
        self.__dict__.update(kwargs)

        logging.debug("Instance variables for s3Client : " + str(self.__dict__))

    def return_client(self, service_name):
        """
        This method creates s3 clients
        """
        client = None

        try:
            if self.aws_details:
                # Checking if assigned_role_arn is provided or not
                if {"assigned_role_arn", "access_key", "secret_key", "region_name"}.issubset(
                        set(self.aws_details.keys())):

                    # Created base session
                    base_session = boto3.session.Session(
                        aws_access_key_id=self.aws_details["access_key"],
                        aws_secret_access_key=self.aws_details["secret_key"],
                        region_name=self.aws_details["region_name"])

                    # Created ARN session ( This is a boto3 session )
                    arn_session = assumed_role_session(role_arn=self.aws_details["assigned_role_arn"],
                                                       base_session=base_session._session)

                    # Created client from ARN session
                    client = arn_session.client(service_name)

                elif {"access_key", "secret_key", "region_name"}.issubset(set(self.aws_details.keys())):
                    # Created normal clients in case of no ARN
                    client = boto3.client(service_name, aws_access_key_id=self.aws_details["access_key"],
                                          aws_secret_access_key=self.aws_details["secret_key"],
                                          region_name=self.aws_details["region_name"])
            else:
                # Create normal client if no credentials are provided
                client = boto3.client(service_name)

        except BaseException:
            logging.error("Uncaught exception in client.py: " + traceback.format_exc())
            raise BaseException("Problem in client.py")
        finally:
            return client


if __name__ == "__main__":
    # LOGGING #
    logging_format = "%(asctime)s::%(funcName)s::%(levelname)s:: %(message)s"
    logging.basicConfig(format=logging_format, level=logging.INFO, datefmt="%Y/%m/%d:%H:%M:%S:%Z:%z")
    logger = logging.getLogger(__name__)
