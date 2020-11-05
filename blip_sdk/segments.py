#!/usr/bin/python3
# coding= utf-8
"""
This is a helper script for consuming Blip Segments API
"""
import logging

try:
    from amagi_library.helper.http_requests import HTTPRequests
except ModuleNotFoundError:
    logging.info("Module called internally")
    from helper.http_requests import HTTPRequests


class Segments(object):
    """
    Class for consuming Segments API from Blip
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

        logging.debug(f"Instance variables for Playlist : {self.__dict__}")

    def __del__(self):
        # Removing HTTP request session
        self.http_requests_instance.__del__()

    def post_segment_information(self, media_id: str, **kwargs):
        """
        This method to put media details
        :param media_id: Media ID
        :return: call_put_requests
        """
        if media_id and ("feed_id" and "duration") in kwargs:
            url = f"https://{self.customer}.amagi.tv/v1/api/media/{media_id}/segments.json"
            logging.info(f"POST url invoked to put segment details : {url}")
            kwargs.update(self.default_payload)
            return self.http_requests_instance.call_post_requests(url=url, params=kwargs,
                                                                  error_message="Error occurred when trying "
                                                                                "to access Blip"
                                                                                " for putting Media Segment Details : ")
        else:
            logging.error("Media ID , Feed ID and duration is required to use this API")
            return None


if __name__ == "__main__":
    # LOGGING #
    logging_format = "%(asctime)s::%(funcName)s::%(levelname)s:: %(message)s"
    logging.basicConfig(format=logging_format, level=logging.DEBUG, datefmt="%Y/%m/%d %H:%M:%S:%Z(%z)")
    logger = logging.getLogger(__name__)
    segments_instance = Segments(customer=None, token=None)
