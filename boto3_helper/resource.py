#!/usr/bin/python3
# coding= utf-8
"""
This scripts provides wrapper over AWS resource
"""
import logging
import traceback

import boto3

try:
    from amagi_library.boto3_helper.arn_session import assumed_role_session
except ModuleNotFoundError:
    logging.info("Module called internally")
    from boto3_helper.arn_session import assumed_role_session


class Resource(object):
    """
        This Class handles creation of dynamo DB resource
    """

    def __init__(self, **kwargs):
        self.aws_details = None
        self.__dict__.update(kwargs)

        logging.debug(f"Instance variables for Resource : {self.__dict__}")

    def return_resource(self, service_name):
        """
        This method creates AWS resource
        """

        resource = None

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

                    # Created resource from ARN session
                    resource = arn_session.resource(service_name)

                elif {"access_key", "secret_key", "region_name"}.issubset(set(self.aws_details.keys())):
                    # Created normal resource in case of no ARN
                    resource = boto3.Session(aws_access_key_id=self.aws_details["access_key"],
                                             aws_secret_access_key=self.aws_details["secret_key"],
                                             region_name=self.aws_details["region_name"]).resource(service_name)

                elif {"profile_name"}.issubset(set(self.aws_details.keys())):
                    # Created normal clients in case of no ARN using profile name
                    resource = boto3.Session(profile_name=self.aws_details["profile_name"]).resource(service_name)
            else:
                # Create normal resource if no credentials are provided
                resource = boto3.Session().resource(service_name)

        except BaseException:
            logging.error(f"Uncaught exception in resource.py: {traceback.format_exc()}")
            raise BaseException("Problem in resource.py")

        finally:
            return resource


if __name__ == "__main__":
    # LOGGING #
    logging_format = "%(asctime)s::%(funcName)s::%(levelname)s:: %(message)s"
    logging.basicConfig(format=logging_format, level=logging.INFO, datefmt="%Y/%m/%d:%H:%M:%S:%Z:%z")
    logger = logging.getLogger(__name__)
