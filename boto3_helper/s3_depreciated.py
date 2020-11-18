#!/usr/bin/python3
# coding=utf-8
"""
This scripts provides wrapper over AWS S3
"""
import logging
import traceback

from boto3.s3.transfer import TransferConfig

try:
    from amagi_library.boto3_helper.client import Client
except ModuleNotFoundError:
    logging.info("Module called internally")
    from boto3_helper.client import Client


class DisplayS3Object(object):
    """
    This class handles list of object data from S3
    """

    def __init__(self, **kwargs):
        # Required variable to drive this Class, expected to be provided from parent Object
        self.aws_details = None
        self.__dict__.update(kwargs)

        self.s3_client_instance = Client(aws_details=self.aws_details).return_client(
            service_name="s3")

        logging.debug(f"Instance variables for DisplayS3Object : {self.__dict__}")

    def object_content(self, **kwargs) -> bytes:
        """
        This method downloads file from local machine to s3 and then prints it
        """
        try:
            source = self.s3_client_instance.get_object(
                Bucket=kwargs["s3_details"]["bucket_name"],
                Key=kwargs["object_path"]
            )

            return source["Body"].read()

        except BaseException:
            logging.error(f"Uncaught exception in s3.py : {traceback.format_exc()}")


class CopyToS3(object):
    """
    This class provide interface to copy from local to S3
    """

    def __init__(self, **kwargs):
        # Required variable to drive this Class, expected to be provided from parent Object
        self.destination_aws_details = None
        self.__dict__.update(kwargs)

        self.destination_s3_client_instance = Client(aws_details=self.destination_aws_details).return_client(
            service_name="s3")

        logging.debug(f"Instance variables for CopytoS3 : {self.__dict__}")

    def copy_to_destination_s3(self, **kwargs):
        """
        This method downloads file from local machine to s3
        """
        try:
            self.destination_s3_client_instance.put_object(Body=kwargs["data"],
                                                           Bucket=kwargs["destination_s3_details"]["bucket_name"],
                                                           Key=kwargs["object_destination_path"])

        except BaseException:
            logging.error(f"Uncaught exception in s3.py : {traceback.format_exc()}")


class CopyFromURLtoS3(object):
    """
    This class provide interface to copy object from one s3 to another s3
    """
    maximum_part_size = 5 * 1024 ** 3

    def __init__(self, **kwargs):
        # Required variable to drive this Class, expected to be provided from parent Object
        self.destination_aws_details = None

        self.__dict__.update(kwargs)

        # DEFAULT CHUNK SIZE
        self.chunk_size = 256 * 1024 ** 2

        logging.debug(f"Instance variables for CopyFromURLtoS3 : {self.__dict__}")

    @staticmethod
    def read_in_chunks(file_object, chunk_size):
        """
        Lazy function (generator) to read a file piece by piece.
        Default chunk size: 1k.
        xref: https://dataroz.com/stream-large-files-between-s3-and-gcs-python/
        """
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data

    def copy_from_source_url_to_destination_s3(self, **kwargs):
        """
        This method downloads file from url to s3
        """
        pass


class CopyObjectFromS3ToS3(object):
    """
    This class provide interface to copy object from one s3 to another s3
    """

    def __init__(self, **kwargs):
        # Required variable to drive this Class, expected to be provided from parent Object
        self.source_aws_details = None
        self.destination_aws_details = None

        self.__dict__.update(kwargs)

        self.source_s3_client_instance = Client(aws_details=self.source_aws_details).return_client(service_name="s3")
        self.destination_s3_client_instance = Client(aws_details=self.destination_aws_details).return_client(
            service_name="s3")

        logging.debug(f"Instance variables for CopyObjectFromS3ToS3 : {self.__dict__}")

    def copy_from_source_to_destination_s3(self, **kwargs):
        """
        This method downloads file from one s3 to another s3
        """
        try:
            copy_source = self.source_s3_client_instance.get_object(
                Bucket=kwargs["source_s3_details"]["bucket_name"],
                Key=kwargs["object_original_path"]
            )

            # chunk of 250 Mb
            config = TransferConfig(multipart_threshold=1024 * 25, multipart_chunksize=1024 * 25)

            self.destination_s3_client_instance.upload_fileobj(copy_source["Body"],
                                                               kwargs["destination_s3_details"]["bucket_name"],
                                                               kwargs["object_destination_path"], Config=config)
        except BaseException:
            logging.error(f"Uncaught exception in s3.py : {traceback.format_exc()}")


class CopyObjectFromS3ToLocal(object):
    """
    This Class is to data handle from s3 to local
    """

    def __init__(self, **kwargs):
        # Required variable to drive this Class, expected to be provided from parent Object
        self.aws_details = None
        self.__dict__.update(kwargs)

        logging.debug(f"Instance variables for CopyObjectFromS3ToLocal : {self.__dict__}")

    def download_content(self, **kwargs):
        """
        This method downloads file from local machine to s3 and then prints it
        """
        pass


class S3DeleteObject(object):
    """
        This class provide wrapper to delete S3 objects
    """

    def __init__(self, **kwargs):

        # Required variables to drive this Object
        self.aws_details = None

        self.__dict__.update(kwargs)

        # Variable received later when method called
        self.s3_details = None

        # S3 Client instance to use
        self.s3_instance = Client(aws_details=self.aws_details).return_client(service_name="s3")

        logging.debug(f"Instance variables for S3DeleteObject : {self.__dict__}")

    @staticmethod
    def aws_api_response_handler(response):
        """
        This method recursively add data into object Dictionary
        :param response: list_objects_response from boto3 s3 client
        """

        if response["ResponseMetadata"]["HTTPStatusCode"] == 204:
            logging.info("Deleted successfully")
        logging.error(f"Response from delete : {response['ResponseMetadata']}")

    def delete_from_s3(self, **kwargs):
        """
        Driving method which will get contents of all the objects in s3
        :return: Returns object dict containing details about s3
        """
        self.s3_details = kwargs["s3_details"]

        try:
            # Required parameter to call list_objects_v2
            S3DeleteObject.aws_api_response_handler(
                self.s3_instance.delete_object(Bucket=self.s3_details["bucket_name"],
                                               Key=kwargs["object_path"]))
        except BaseException:
            logging.error(f"Uncaught exception in s3.py : {traceback.format_exc()}")


class MoveObjectFromS3ToS3(object):
    """
    This class handles all the s3 object move
    """

    def __init__(self, **kwargs):
        # Required variable to drive this Class, expected to be provided from parent Object
        self.source_aws_details = None
        self.destination_aws_details = None

        self.__dict__.update(kwargs)

        logging.debug(f"Instance variables for MoveObjectFromS3ToS3 : {self.__dict__}")

    def move_from_source_to_destination_s3(self, **kwargs):
        """
        This method downloads file from one s3 to another s3
        """
        try:
            CopyObjectFromS3ToS3(source_aws_details=self.source_aws_details,
                                 destination_aws_details=self.destination_aws_details). \
                copy_from_source_to_destination_s3(
                source_s3_details=kwargs["source_s3_details"],
                object_original_path=kwargs["object_original_path"],
                destination_s3_details=kwargs["destination_s3_details"],
                object_destination_path=kwargs["object_destination_path"])

            S3DeleteObject(aws_details=self.source_aws_details). \
                delete_from_s3(s3_details=kwargs["source_s3_details"],
                               Key=kwargs["object_original_path"])
        except BaseException:
            logging.error(f"Uncaught exception in s3.py: {traceback.format_exc()}")


class S3ObjectList(object):
    """
        This class creates dict of s3 objects with some basic filter
    """

    def __init__(self, **kwargs):

        # Required variables to drive this Object
        self.aws_details = None

        self.__dict__.update(kwargs)

        # Variable received later when method called
        self.s3_details = None
        self.s3_object_filter = None
        self.folder_to_check = ""

        # S3 Client instance to use
        self.s3_instance = Client(aws_details=self.aws_details).return_client(service_name="s3")

        # Object dictionary
        self.object_dict = None

        logging.debug(f"Instance variables for s3ObjectList : {self.__dict__}")

    def __object_filter(self, item: dict) -> bool:
        """
        This method filter based on the input provided in self.object_filter
        :param item: s3 item which needs to be checked
        :return: Boolean condition based on whether item passed the filter or not
        """
        # Default filter of checking whether the size is greater than 0B or not
        if item["Size"] > 0:
            if self.s3_object_filter:
                for key in self.s3_object_filter.keys():
                    if item[key] != self.s3_object_filter[key]:
                        return False
                return True
            else:
                logging.debug("S3 object Filter not found in configuration")
                return True
        else:
            return False

    def __add_details_to_object_dict(self, list_objects_response: dict):
        """
        This method recursively add data into object Dictionary
        :param list_objects_response: list_objects_response from boto3 s3 client
        """

        if list_objects_response["ResponseMetadata"]["HTTPStatusCode"] == 200 and \
                "Contents" in list_objects_response.keys():

            for item in list_objects_response["Contents"]:
                if self.__object_filter(item):
                    object_name = item["Key"]
                    logging.debug(f"Object available in s3 in folder {self.folder_to_check} : {object_name}")
                    self.object_dict.update({object_name: item})

            # This check if the response received was truncated or not
            # If truncated then recursively call and update dictionary
            if list_objects_response["IsTruncated"]:
                self.__add_details_to_object_dict(
                    self.s3_instance.list_objects_v2(
                        Bucket=self.s3_details["bucket_name"],
                        Prefix=self.folder_to_check,
                        ContinuationToken=list_objects_response["NextContinuationToken"]))
        else:
            logging.error(
                f"Response from list_objects_v2 : {list_objects_response['ResponseMetadata']}")

    def check_contents_of_s3(self, **kwargs) -> dict:
        """
        Driving method which will get contents of all the objects in s3
        :return: Returns object dict containing details about s3
        """

        if "folder_to_check" in kwargs:
            self.folder_to_check = kwargs["folder_to_check"]
        if "s3_object_filter" in kwargs:
            self.s3_object_filter = kwargs["s3_object_filter"]

        self.s3_details = kwargs["s3_details"]

        try:
            self.object_dict = dict()

            # Required parameter to call list_objects_v2
            self.__add_details_to_object_dict(self.s3_instance.list_objects_v2(Bucket=self.s3_details["bucket_name"],
                                                                               Prefix=self.folder_to_check))

            logging.debug(f"Objects matching filter criteria : {self.object_dict}")

            logging.info(f"Total No of Objects in S3 in folder {self.folder_to_check} : {len(self.object_dict)}")

        except BaseException:
            logging.error(f"Uncaught exception in s3.py : {traceback.format_exc()}")

        return self.object_dict


if __name__ == "__main__":
    # LOGGING #
    logging_format = "%(asctime)s::%(funcName)s::%(levelname)s:: %(message)s"
    logging.basicConfig(format=logging_format, level=logging.DEBUG, datefmt="%Y/%m/%d %H:%M:%S:%Z(%z)")
    logger = logging.getLogger(__name__)
