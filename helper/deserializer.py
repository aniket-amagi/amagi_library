#!/usr/bin/python3
# coding= utf-8
"""
This is a helper script to deserialize data
"""
import csv
import json
import logging
import traceback
from io import StringIO
from json import JSONDecodeError

import yaml
from idna import unicode


class Deserializer(object):
    """
        This method defines http requests call and handle error condition based on that
    """

    @staticmethod
    def json_deserializer(text: str, encoding='utf-8'):
        """
        This method deserializes the data received in json format
        :param encoding: Encoding of text (Generally assumed utf-8)
        :param text: text to be deserialized from json
        :return:
        """
        data_dict = None
        try:
            if not encoding == 'utf-8':
                encoding_handled_text = unicode(text.encode(encoding), 'utf-8')
            else:
                encoding_handled_text = text
            data_dict = json.loads(encoding_handled_text)
        except JSONDecodeError:
            logging.error(f"Problem decoding Json : {traceback.format_exc()}")
        except AttributeError:
            logging.error("Text provided is empty")
        return data_dict

    @staticmethod
    def csv_deserializer(text: str, encoding='utf-8'):
        data_dict = None
        try:
            if not encoding == 'utf-8':
                encoding_handled_text = unicode(text.encode(encoding), 'utf-8')
            else:
                encoding_handled_text = text
            dialect = csv.Sniffer().sniff(encoding_handled_text)
            data_dict = csv.DictReader(StringIO(encoding_handled_text), delimiter=dialect.delimiter,
                                       quotechar=dialect.quotechar)
        except BaseException:
            logging.error(f"Problem decoding csv : {traceback.format_exc()}")
        return data_dict

    @staticmethod
    def yaml_deserializer(text: str, encoding='utf-8'):
        data_dict = None
        try:
            if not encoding == 'utf-8':
                encoding_handled_text = unicode(text.encode(encoding), 'utf-8')
            else:
                encoding_handled_text = text
            data_dict = yaml.load(encoding_handled_text)
        except BaseException:
            logging.error(f"Problem decoding yaml : {traceback.format_exc()}")
        return data_dict


if __name__ == "__main__":
    # LOGGING #
    logging_format = "%(asctime)s::%(funcName)s::%(levelname)s:: %(message)s"
    logging.basicConfig(format=logging_format, level=logging.DEBUG, datefmt="%Y/%m/%d %H:%M:%S:%Z(%z)")
    logger = logging.getLogger(__name__)
