#!/usr/bin/python3
# coding= utf-8
"""
This is a helper script for consuming Blip Playlist API
"""
import logging

from amagi_library.helper.http_requests import HTTPRequests


class Playlist(object):
    """
    Class for consuming Playlist API from Blip
    """

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

        logging.debug("Instance variables for Playlist : " + str(self.__dict__))

    def get_playlist_request(self, **kwargs):
        """
        This method does a GET call to Blip to get playlist.
        :return: Response object from Blip API
        """

        url = f"https://{self.customer}.amagi.tv/v1/api/playlist"
        logging.info("Base Playlist API url : " + url)
        kwargs.update(self.default_payload)
        return self.http_requests_instance.call_get_requests(url=url, params=kwargs,
                                                             error_message="Error occurred when trying to "
                                                                           "access Blip for Playlist : ")

    def get_missing_asset_per_feed_per_playlist(self, playlist_id, **kwargs):
        """
        This method gets all the missing item in playlist from blip
        :param playlist_id: Playlist ID
        :return: Response object from Blip API
        """

        url = f"https://{self.customer}.amagi.tv/v1/api/playlist/{playlist_id}/missing"
        logging.info("Missing list url invoked to get details: " + url)
        kwargs.update(self.default_payload)
        return self.http_requests_instance.call_get_requests(url=url, params=kwargs,
                                                             error_message="Error occurred when "
                                                                           "trying to "
                                                                           "access Blip for Missing assets : ")

    def get_asset_status_on_cloud_and_device(self, playlist_id, **kwargs):
        """
        This method get all the assets in a playlist and its details
        :param playlist_id: Playlist ID
        :return: Response object from Blip API
        """

        url = f"https://{self.customer}.amagi.tv/v1/api/playlist/{playlist_id}/assets.json"
        logging.info("Asset Status url invoked to get details: " + url)
        kwargs.update(self.default_payload)
        return self.http_requests_instance.call_get_requests(url=url, params=kwargs,
                                                             error_message="Error occurred when trying to "
                                                                           "access Blip for Asset Status on Cloud: ")

    def get_playlist_details(self, playlist_id, **kwargs):
        """
        This method get details about the playlist
        :param playlist_id: Playlist ID
        :param kwargs: Response object from Blip API
        :return:
        """

        if "feed_id" in kwargs:
            url = f"https://{self.customer}.amagi.tv/v1/api/playlist/{playlist_id}.json"
            logging.info("Playlist Details url invoked to get details: " + url)
            kwargs.update(self.default_payload)
            return self.http_requests_instance.call_get_requests(url=url, params=kwargs,
                                                                 error_message="Error occurred when trying to "
                                                                               "access Blip for Playlist Details: ")
        else:
            logging.error("feed_id is required to use this API")
            return None


if __name__ == "__main__":
    # LOGGING #
    logging_format = "%(asctime)s::%(funcName)s::%(levelname)s:: %(message)s"
    logging.basicConfig(format=logging_format, level=logging.INFO, datefmt="%Y/%m/%d:%H:%M:%S:%Z:%z")
    logger = logging.getLogger(__name__)
    playlist_instance = Playlist(customer=None, token=None)
