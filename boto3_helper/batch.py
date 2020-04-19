#!/usr/bin/python3
# coding= utf-8
"""
This scripts actually submit batch jobs
"""
import logging
import traceback

from amagi_library.boto3_helper.client import Client


class SubmitBatchJob(object):
    """
    This Class handles firing batch job
    """

    def __init__(self, **kwargs):

        # Required variable to drive this Class, expected to be provided from parent Object
        self.aws_details = None
        self.__dict__.update(kwargs)

        self.batch_instance = Client(aws_details=self.aws_details).return_client(service_name="batch")
        logging.debug("Instance variables for submitBatchJob : " + str(self.__dict__))

    def submit_job(self, **kwargs):
        """
        This method is scrub of from old project to submit batch jobs without MAPSOR API
        :param kwargs: This parameter contains information from environemnt
        :return: submits a batch job
        """

        logging.info("Arguments for submit job " + str(kwargs))

        response = None
        try:

            response = self.batch_instance.submit_job(
                jobName=kwargs["job_details"]["job_name"],
                jobQueue=kwargs["job_details"]['job_queue'],
                jobDefinition=kwargs["job_details"]['job_definition'],
                containerOverrides={
                    "vcpus": kwargs["job_details"]["vcpus"],
                    "memory": kwargs["job_details"]["memory"],
                    "command": kwargs["job_details"]["command"],
                    "environment": kwargs["job_details"]["environment"]

                },
                timeout=kwargs["job_details"]["timeout"]
            )

        except BaseException:
            logging.error("Uncaught exception in batch.py: " + traceback.format_exc())
            raise BaseException("Problem in batch.py")
        finally:
            logging.info("Batch Job submission response: {0}".format(response))


if __name__ == "__main__":
    # LOGGING #
    logging_format = "%(asctime)s::%(funcName)s::%(levelname)s:: %(message)s"
    logging.basicConfig(format=logging_format, level=logging.INFO, datefmt="%Y/%m/%d:%H:%M:%S:%Z:%z")
    logger = logging.getLogger(__name__)
