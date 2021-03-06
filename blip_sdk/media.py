#!/usr/bin/python3
# coding= utf-8
"""
This is a helper script for consuming Blip Media API
"""
import logging

try:
    from amagi_library.helper.http_requests import HTTPRequests
except ModuleNotFoundError:
    logging.info("Module called internally")
    from helper.http_requests import HTTPRequests


class Media(object):
    """
    Class for consuming Media API from Blip
    """

    # Class Variables
    account_id = "account_id"
    feed_id = "feed_id"
    feeds = "feeds"

    def __init__(self, **kwargs):

        # These variables are defined so that
        # codebase can be expanded based on new requirements
        self.customer = None
        self.token = None
        self.__dict__.update(kwargs)

        self.default_payload = {
            "token": self.token
        }
        self.http_requests_instance = HTTPRequests()

        logging.debug(f"Instance variables for Media : {self.__dict__}")

    def __del__(self):
        # Removing HTTP request session
        self.http_requests_instance.__del__()

    def get_all_media_details(self, **kwargs):
        """
        This method get media details for an asset id
        :return: call_get_requests
        """
        if Media.account_id or Media.feed_id in kwargs:
            url = f"https://{self.customer}.amagi.tv/v1/api/media"
            logging.info(f"GET url invoked to get details : {url}")
            kwargs.update(self.default_payload)
            return self.http_requests_instance.call_get_requests(url=url, params=kwargs,
                                                                 error_message="Error occurred when trying to "
                                                                               "access Blip for All Media Details : ")
        else:
            logging.error("Either account_id or feed_id is required to use this API")
            return None

    def get_media_details(self, asset_id: str, **kwargs):
        """
        This method get media details for an asset id
        :param asset_id: Asset ID
        :return: call_get_requests
        """
        if Media.account_id or Media.feed_id in kwargs and asset_id:
            format = "json"
            if "format" in kwargs:
                format = kwargs["format"]
            if "detailed" in kwargs and kwargs["detailed"]:
                kwargs["detailed"] = True
            url = f"https://{self.customer}.amagi.tv/v1/api/media/{asset_id}.{format}"
            logging.info(f"GET url invoked to get details : {url}")
            kwargs.update(self.default_payload)
            return self.http_requests_instance.call_get_requests(url=url, params=kwargs,
                                                                 error_message="Error occurred when trying to "
                                                                               "access Blip for Media Details : ")
        else:
            logging.error("Either (account_id or feed_id) and asset_id is required to use this API")
            return None

    def put_media_details(self, media_id: str, data=None, **kwargs):
        """
        This method to put media details
        :param media_id: Media ID
        :param data: data to be added for asset
        :return: call_put_requests
        """
        if media_id:
            url = f"https://{self.customer}.amagi.tv/v1/api/media/{media_id}.json"
            logging.info(f"PUT url invoked to put details : {url}")
            kwargs.update(self.default_payload)
            return self.http_requests_instance.call_put_requests(url=url, params=kwargs, data=data,
                                                                 headers={"Content-Type": "application/json"},
                                                                 error_message="Error occurred when trying to "
                                                                               "access Blip for "
                                                                               "putting Asset Details : ")
        else:
            logging.error("Id is required to use this API")
            return None

    def post_batch_meta_upload(self, files, **kwargs):
        """
        This method to put meta details
        :param files: file to be uploaded to blip
        :return: call_post_requests
        """
        if Media.account_id or Media.feed_id in kwargs and files:
            url = f"https://{self.customer}.amagi.tv/v1/api/media/meta_upload.json"
            logging.info(f"POST url invoked to get details : {url}")
            kwargs.update(self.default_payload)
            return self.http_requests_instance.call_post_requests(url=url, params=kwargs, files=files,
                                                                  error_message="Error occurred when trying to "
                                                                                "access Blip for "
                                                                                "Uploading meta details : ")
        else:
            logging.error("Either (account_id or feed_id) and files is required to use this API")
            return None

    def delete_media_asset(self, media_id: str, **kwargs):
        """
        This method deletes the asset from Blip
        :param media_id: media ID of assets
        :param kwargs: keyword arguments
        """
        if Media.account_id or Media.feed_id and Media.feeds in kwargs:
            url = f"https://{self.customer}.amagi.tv/v1/api/media/{media_id}"
            logging.info(f"DELETE url invoked to get details : {url}")
            kwargs.update(self.default_payload)
            return self.http_requests_instance.call_delete_requests(url=url, params=kwargs,
                                                                    error_message="Error occurred when trying to "
                                                                                  "access Blip for "
                                                                                  "Deleting Asset : ")
        else:
            logging.error("Either (account_id or feed_id) and feeds is required to use this API")
            return None

    def get_all_media_types(self, **kwargs):
        """
        This method is to get all media types available in Blip
        :param kwargs: keyword arguments
        """
        if Media.account_id or Media.feed_id in kwargs:
            url = f"https://{self.customer}.amagi.tv/v1/api/types"
            logging.info(f"GET url invoked to get details : {url}")
            kwargs.update(self.default_payload)
            return self.http_requests_instance.call_get_requests(url=url, params=kwargs,
                                                                 error_message="Error occurred when trying to "
                                                                               "access Blip for "
                                                                               "Media Types: ")
        else:
            logging.error("Either account_id or feed_id is required to use this API")
        return None


if __name__ == "__main__":
    try:
        from amagi_library.helper.deserializer import Deserializer
    except ModuleNotFoundError:
        logging.info("Module called internally")
        from helper.deserializer import Deserializer
    from pprint import pprint

    # LOGGING #
    logging_format = "%(asctime)s::%(funcName)s::%(levelname)s:: %(message)s"
    logging.basicConfig(format=logging_format, level=logging.INFO, datefmt="%Y/%m/%d %H:%M:%S:%Z(%z)")
    logger = logging.getLogger(__name__)
    media_instance = Media(customer="{to_be_filled}", token="{to_be_filled}")
    all_media_details_response = media_instance.get_all_media_details(account_id=1)
    pprint(Deserializer.json_deserializer(all_media_details_response.text, all_media_details_response.encoding))
