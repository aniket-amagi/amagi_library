#!/usr/bin/python3
# coding= utf-8
"""
This script gets all the image related details
"""

import logging

from PIL import ImageFile


class ImageParser(object):
    """
        This class provides simple parsing of image objects using Pillow library
    """

    def __init__(self):
        self.image_parser = ImageFile.Parser()

        logging.debug(f"Instance variables for ImageParser : {self.__dict__}")

    def __del__(self):
        self.image_parser.close()

    def get_image_details(self, byte_data):
        """
        This method provides image detail based on the the byte data provided to it
        :param byte_data: Data in bytes
        """
        image_details = None
        self.image_parser.feed(byte_data)
        if self.image_parser.image:
            image_details = {
                "format": self.image_parser.image.format,
                "mode": self.image_parser.image.mode,
                "size": self.image_parser.image.size,
                "width": self.image_parser.image.width,
                "height": self.image_parser.image.height,
                "palette": self.image_parser.image.palette,
                "info": self.image_parser.image.info
            }
            logging.info(f"Image related details : {image_details}")

        else:
            logging.error("Unable to decode image from the url")
        return image_details


if __name__ == "__main__":
    from helper.http_requests import HTTPRequests

    # LOGGING #
    logging_format = "%(asctime)s::%(funcName)s::%(levelname)s:: %(message)s"
    logging.basicConfig(format=logging_format, level=logging.DEBUG, datefmt="%Y/%m/%d:%H:%M:%S:%Z:%z")
    logger = logging.getLogger(__name__)
    print(ImageParser().get_image_details(
        HTTPRequests().call_get_requests("https://homepages.cae.wisc.edu/~ece533/images/baboon.png").content))
