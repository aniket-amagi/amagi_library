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

    def __init__(self, **kwargs):
        self.url = None
        self.auth_key = None
        self.auth_secret = None
        self.x_hybrik_compliance = None
        self.oapi_key = None
        self.oapi_secret = None

        self.__dict__.update(kwargs)

        self.token, self.expiration_time = self.api_token()
        logging.debug(f"Instance variables for Hybrik : {str(self.__dict__)}")

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
        response = HTTPRequests().call_post_requests(url=url, headers=headers, params=payload, auth=auth)
        response_text = Deserializer.json_deserializer(response.text)
        return response_text["token"], response_text["expiration_time"]

    class Decorator:
        @staticmethod
        def refresh_token(decorated):
            """
            This method refreshes the token for hynix
            :param decorated: method call this decorator
            :return: inbuilt method
            """

            def wrapper(api, *args, **kwargs):
                if datetime.utcnow() > datetime.strptime(api.expiration_time, '%Y-%m-%dT%H:%M:%S.%fZ'):
                    api.api_token()
                return decorated(api, *args, **kwargs)

            return wrapper

    @Decorator.refresh_token
    def send_job(self, job_name, payload, schema="hybrik", **kwargs):
        payload = {
            'job_name': job_name,
            'payload': payload,
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
        response = HTTPRequests().call_post_requests(url=url, headers=headers, params=payload, auth=auth)
        return response


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
           oapi_secret="Pqs0ykiwkfSrXOXDCgbHGPhwwN7EeQ").send_job()
