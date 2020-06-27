#!/usr/bin/python3
# coding= utf-8
"""
This scripts actually queries Hybrik
"""
import logging
from datetime import datetime

from requests.auth import HTTPBasicAuth

from amagi_library.helper.deserializer import Deserializer

try:
    from amagi_library.helper.http_requests import HTTPRequests
except ModuleNotFoundError:
    logging.info("Module called internally")
    from helper.http_requests import HTTPRequests


class Hybrik(object):
    """
    Class for calling Hybrik APIs
    """
    def __init__(self, **kwargs):
        self.url = None
        self.auth_key = None
        self.auth_secret = None
        self.x_hybrik_compliance = None
        self.oapi_key = None
        self.oapi_secret = None
        self.hybrik_session = HTTPRequests()

        self.__dict__.update(kwargs)

        self.token, self.expiration_time = self.api_token()
        logging.debug(f"Instance variables for Hybrik : {str(self.__dict__)}")

    def __del__(self):
        self.hybrik_session.__del__()

    def api_token(self):
        """
            This method creates api token for Hybrik
        :return:
        """
        payload = {
            'auth_key': self.auth_key,
            'auth_secret': self.auth_secret
        }
        headers = {
            'Content-Type': 'application/json',
            'X-Hybrik-Compliance': self.x_hybrik_compliance,
        }
        auth = HTTPBasicAuth(self.oapi_key, self.oapi_secret)
        url = f"{self.url}/v1/login"
        response = self.hybrik_session.call_post_requests(url=url, headers=headers, params=payload, auth=auth)
        response_text = Deserializer.json_deserializer(response.text)
        return response_text["token"], response_text["expiration_time"]

    class Decorator:
        """
        Decorator class for refreshing token
        """

        @staticmethod
        def refresh_token(decorated):
            """
            This method refreshes the token for hynix
            :param decorated: method call this decorator
            :return: inbuilt method
            """

            def wrapper(api, *args, **kwargs):
                """
                Wrapper method for refresh token
                :param api: api
                :param args: arguments of called method
                :param kwargs: keyword arguments of called method
                :return:
                """
                if datetime.utcnow() > datetime.strptime(api.expiration_time, '%Y-%m-%dT%H:%M:%S.%fZ'):
                    api.api_token()
                return decorated(api, *args, **kwargs)

            return wrapper

    @Decorator.refresh_token
    def send_job(self, data, schema="hybrik", **kwargs):
        """
        This method send jobs to Hybrik API
        :param data: json data to be sent
        :param schema: schema of data
        :param kwargs: extra keyword arguments
        :return: response acquired from Hybrik
        """
        payload = {
            'schema': schema
        }
        payload.update(kwargs)
        headers = {
            'Content-Type': 'application/json',
            'X-Hybrik-Compliance': self.x_hybrik_compliance,
            'X-Hybrik-Sapiauth': self.token
        }
        auth = HTTPBasicAuth(self.oapi_key, self.oapi_secret)
        url = f"{self.url}/v1/jobs"
        response = self.hybrik_session.call_post_requests(url=url, headers=headers, params=payload, data=data,
                                                          auth=auth)
        return response

    @Decorator.refresh_token
    def check_job(self, **kwargs):
        pass


if __name__ == "__main__":
    # LOGGING #
    logging_format = "%(asctime)s::%(funcName)s::%(levelname)s:: %(message)s"
    logging.basicConfig(format=logging_format, level=logging.DEBUG, datefmt="%Y/%m/%d:%H:%M:%S:%Z:%z")
    logger = logging.getLogger(__name__)
    Hybrik(url="https://api-demo.hybrik.com",
           auth_key="arpitm@amagi.com",
           auth_secret="Amagi@560076",
           x_hybrik_compliance="20191031",
           oapi_key="QyNU5XYeV3C64PiuF08@accnt.oapi.hybrik",
           oapi_secret="Pqs0ykiwkfSrXOXDCgbHGPhwwN7EeQ").send_job(data=open('test.json').read())
