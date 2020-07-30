#!/usr/bin/python3
# coding= utf-8
"""
This scripts provide wrapper over AWS Batch operations
"""
import logging
import traceback

try:
    from amagi_library.boto3_helper.client import Client
except ModuleNotFoundError:
    logging.info("Module called internally")
    from boto3_helper.client import Client


class SubmitBatchJob(object):
    """
    This Class handles firing batch job
    """

    def __init__(self, **kwargs):

        # Required variable to drive this Class, expected to be provided from parent Object
        self.aws_details = None
        self.__dict__.update(kwargs)

        self.batch_instance = Client(aws_details=self.aws_details).return_client(service_name="batch")
        logging.debug(f"Instance variables for submitBatchJob : {self.__dict__}")

    def submit_job(self, **kwargs):
        """
        This method is scrub of from old project to submit batch jobs without mapsor API
        :param kwargs: This parameter contains information from environment
        :return: submits a batch job
        """

        logging.info(f"Arguments for submit job: {kwargs}")

        response = None
        try:

            response = self.batch_instance.submit_job(
                jobName=kwargs["job_details"]["job_name"],
                jobQueue=kwargs["job_details"]["job_queue"],
                jobDefinition=kwargs["job_details"]["job_definition"],
                containerOverrides={
                    "vcpus": kwargs["job_details"]["vcpus"],
                    "memory": kwargs["job_details"]["memory"],
                    "command": kwargs["job_details"]["command"],
                    "environment": kwargs["job_details"]["environment"]

                },
                timeout=kwargs["job_details"]["timeout"]
            )

        except BaseException:
            logging.error(f"Uncaught exception in batch.py : {traceback.format_exc()}")
            raise BaseException("Problem in batch.py")
        finally:
            logging.info(f"Batch Job submission response: {response}")


if __name__ == "__main__":
    # LOGGING #
    logging_format = "%(asctime)s::%(funcName)s::%(levelname)s:: %(message)s"
    logging.basicConfig(format=logging_format, level=logging.INFO, datefmt="%Y/%m/%d:%H:%M:%S:%Z:%z")
    logger = logging.getLogger(__name__)
