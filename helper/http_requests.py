#!/usr/bin/python3
# coding= utf-8
"""
This is a helper script for sending HTTP Requests
"""
import logging

import requests


class HTTPRequests(object):
    """
        This method defines http requests call and handle error condition based on that
    """

    def __init__(self):
        # Created Requests session for Blip API
        self.session = requests.Session()

        logging.debug(f"Instance variables for HTTPRequests : {self.__dict__}")

    def __del__(self):
        """
        Explicitly closed session object
        """
        self.session.close()

    def call_get_requests(self, url, headers=None, params=None, stream=False, error_message="Error in GET Request : "):
        """
        Static method to call requests to get response using GET calls
        :param headers: Headers for get call
        :param stream: If data to be streamed ?
        :param url:  URL for get call
        :param params:  Parameters for the call
        :param error_message: Error message to be printed in case of exception
        :return: Response from the requests call
        """
        response = None
        logging.info(f"Url for HTTP request : {url}")
        logging.info(f"Parameters for HTTP request : {params}")
        logging.info(f"Headers for HTTP request : {headers}")
        logging.info(f"Request Stream (True/False)? : {stream}")
        try:
            response = self.session.get(url, headers=headers, params=params, stream=stream)
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            logging.error(error_message + str(error))
        finally:
            if response:
                logging.debug(f"Status Code : {response.status_code}")
                logging.debug(f"Total Time taken : {response.elapsed}")
                logging.debug(f"Encoding : {response.encoding}")
                logging.debug(f"Response Headers : {response.headers}")
                logging.debug(f"Request Headers : {response.request.headers}")
                if response.encoding or response.text:
                    logging.debug(f"Response Text : {response.text}")
            else:
                logging.critical("No response!!")
            return response

    def call_put_requests(self, url, headers=None, params=None, data=None, error_message="Error in PUT Request : "):
        """
        Static method to call requests to get response using PUT calls
        :param data: Adding data for put call
        :param headers: Header for put call
        :param url:  URL for get call
        :param params:  Parameters for the call
        :param error_message: Error message to be printed in case of exception
        :return: Response from the requests call
        """
        response = None
        logging.info(f"Url for HTTP request : {url}")
        logging.info(f"Parameters for HTTP request : {params}")
        logging.info(f"Headers for HTTP request : {headers}")
        logging.info(f"Data for HTTP request : {data}")
        try:
            response = self.session.put(url, headers=headers, params=params, data=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            logging.error(error_message + str(error))
        finally:
            if response:
                logging.debug(f"Status Code : {response.status_code}")
                logging.debug(f"Total Time taken : {response.elapsed}")
                logging.debug(f"Encoding : {response.encoding}")
                logging.debug(f"Response Headers : {response.headers}")
                logging.debug(f"Request Headers : {response.request.headers}")
                if response.encoding or response.text:
                    logging.debug(f"Response Text : {response.text}")
            else:
                logging.critical("No response!!")
            return response

    def call_post_requests(self, url, data=None, headers=None, params=None, files=None,
                           auth=None, error_message="Error in POST Request : "):
        """
        Static method to call requests to get response using POST calls
        :param data: data for post call
        :param files: files for post call
        :param headers: Header for post call
        :param url:  URL for post call
        :param params:  Parameters for the call
        :param error_message: Error message to be printed in case of exception
        :param auth: Authorization for the call
        :return: Response from the requests call
        """
        response = None
        logging.info(f"Url for HTTP request : {url}")
        logging.info(f"Parameters for HTTP request : {params}")
        logging.info(f"Headers for HTTP request : {headers}")
        logging.info(f"Data for HTTP request : {data}")
        logging.info(f"Files for HTTP request : {files}")
        logging.info(f"Auth for HTTP request : {auth}")
        try:
            response = self.session.post(url, headers=headers, params=params, files=files, data=data, auth=auth)
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            logging.error(error_message + str(error))
        finally:
            if response:
                logging.debug(f"Status Code : {response.status_code}")
                logging.debug(f"Total Time taken : {response.elapsed}")
                logging.debug(f"Encoding : {response.encoding}")
                logging.debug(f"Response Headers : {response.headers}")
                logging.debug(f"Request Headers : {response.request.headers}")
                if response.encoding or response.text:
                    logging.debug(f"Response Text : {response.text}")
            else:
                logging.critical("No response!!")
            return response

    def call_delete_requests(self, url, params=None, error_message="Error in DELETE Request : "):
        """
        Static method to call requests to get response using GET calls
        :param url:  URL for get call
        :param params:  Parameters for the call
        :param error_message: Error message to be printed in case of exception
        :return: Response from the requests call
        """
        response = None
        logging.info(f"Url for HTTP request : {url}")
        logging.info(f"Parameters for HTTP request : {params}")
        try:
            response = self.session.delete(url, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            logging.error(error_message + str(error))
        finally:
            if response:
                logging.debug(f"Status Code : {response.status_code}")
                logging.debug(f"Total Time taken : {response.elapsed}")
                logging.debug(f"Encoding : {response.encoding}")
                logging.debug(f"Response Headers : {response.headers}")
                logging.debug(f"Request Headers : {response.request.headers}")
                if response.encoding or response.text:
                    logging.debug(f"Response Text : {response.text}")
            else:
                logging.critical("No response!!")
            return response

    def call_head_requests(self, url, error_message="Error in HEAD Request : "):
        """
        Static method to call requests to get response using HEAD calls
        :param url:  URL for get call
        :param error_message: Error message to be printed in case of exception
        :return: Response from the requests call
        """
        response = None
        logging.info(f"Url for HTTP request : {url}")
        try:
            response = self.session.head(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            logging.error(error_message + str(error))
        finally:
            if response:
                logging.debug(f"Status Code : {response.status_code}")
                logging.debug(f"Total Time taken : {response.elapsed}")
                logging.debug(f"Encoding : {response.encoding}")
                logging.debug(f"Response Headers : {response.headers}")
                logging.debug(f"Request Headers : {response.request.headers}")
                if response.encoding or response.text:
                    logging.debug(f"Response Text : {response.text}")
            else:
                logging.critical("No response!!")
            return response


if __name__ == "__main__":
    # LOGGING #
    logging_format = "%(asctime)s::%(funcName)s::%(levelname)s:: %(message)s"
    logging.basicConfig(format=logging_format, level=logging.DEBUG, datefmt="%Y/%m/%d:%H:%M:%S:%Z:%z")
    logger = logging.getLogger(__name__)
    HTTPRequests().call_get_requests("https://aniket-dev.s3.us-east-1.amazonaws.com/test.xml")
