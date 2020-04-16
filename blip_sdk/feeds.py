#!/usr/bin/python3
# coding= utf-8
"""
This is a helper script for consuming Blip Feed API
"""
import logging

from helper.http_requests import HTTPRequests


class Feeds(object):
    """
    Class for absorbing Feeds API from blip
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
        logging.debug("Instance variables for Feeds : " + str(self.__dict__))

    def get_feed_id_request(self):
        """
        This method does a GET call to Blip to get feed list
        :return: response object from Blip
        """
        url = f"https://{self.customer}.amagi.tv/v1/api/feeds"
        logging.info("Feed url invoked to get details : " + url)
        return self.http_requests_instance.call_get_requests(url=url, params=self.default_payload,
                                                             error_message="Error occurred when trying "
                                                                           "to access Blip for Feed : ")


if __name__ == "__main__":
    from helper.deserializer import Deserializer
    from pprint import pprint

    # LOGGING #
    logging_format = "%(asctime)s::%(funcName)s::%(levelname)s:: %(message)s"
    logging.basicConfig(format=logging_format, level=logging.INFO, datefmt="%Y/%m/%d:%H:%M:%S:%Z:%z")
    logger = logging.getLogger(__name__)
    feed_instance = Feeds(customer="{to_be_filled}", token="{to_be_filled}")
    feed_id_response = feed_instance.get_feed_id_request()
    pprint(Deserializer.json_deserializer(feed_id_response.text, feed_id_response.encoding))
