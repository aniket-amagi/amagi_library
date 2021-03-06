#!/usr/bin/python3
# coding= utf-8
"""
This is a wrapper script for mapsor
Xref : https://mapsor.amagi.tv/docs/
"""
import json
import logging

try:
    from amagi_library.helper.http_requests import HTTPRequests
except ModuleNotFoundError:
    logging.info("Module called internally")
    from helper.http_requests import HTTPRequests


class Mapsor(object):
    """
        This class provides wrapper around mapsor
    """

    def __init__(self, **kwargs):
        self.mapsor_details = None

        self.__dict__.update(kwargs)
        self.http_requests_instance = HTTPRequests()

        logging.debug(f"Instance variables for Mapsor : {self.__dict__}")

    def __del__(self):
        # Removing HTTP request session
        self.http_requests_instance.__del__()

    def create_container_job(self, **kwargs):
        """
        This method schedules a container job
        xref: https://mapsor.amagi.tv/docs/#operation/createContainerJob
        :param kwargs: optional arguments
        """
        payload_dict = dict()
        required_list = ["cloud", "region", "id", "customer"]
        if all(required_key in kwargs for required_key in required_list):
            payload_dict.update(kwargs)
            payload = json.dumps(payload_dict)

            base_url = self.mapsor_details["url"]
            url = f"{base_url}/submit"
            params = {"token": self.mapsor_details["token"]}
            headers = {
                "Content-Type": "application/json",
                "Accept": "*/*",
            }

            response = self.http_requests_instance.call_post_requests(url, data=payload, headers=headers, params=params)
            logging.info(f"Status Code from Mapsor : {response.status_code}")
            logging.info(f"Response from Mapsor : {response.text}")
        else:
            logging.error("One of the required key(cloud, region, id, customer) is missing")

    def submitted_job_status(self, job_id: str):
        """
        This method schedules a container job
        xref: https://mapsor.amagi.tv/docs/#/paths/~1status~1{id}/get
        :param job_id: job id
        """

        base_url = self.mapsor_details["url"]
        url = f"{base_url}/status/{job_id}"
        params = {"token": self.mapsor_details["key"]}
        headers = {
            "Content-Type": "application/json",
            "Accept": "*/*",
        }

        response = self.http_requests_instance.call_get_requests(url, headers=headers, params=params)
        logging.info(f"Response from Mapsor : {response.text}")

    def cancel_submitted_job(self, job_id: str):
        """
        This method to cancel a submitted job
        xref: https://mapsor.amagi.tv/docs/#/paths/~1cancel~1{id}/get
        :param job_id: job id
        """

        base_url = self.mapsor_details["url"]
        url = f"{base_url}/cancel/{job_id}"
        params = {"token": self.mapsor_details["key"]}
        headers = {
            "Content-Type": "application/json",
            "Accept": "*/*",
        }

        response = self.http_requests_instance.call_get_requests(url, headers=headers, params=params)
        logging.info(f"Response from Mapsor : {response.text}")

    def retry_submitted_job(self, job_id: str):
        """
        This method to retry a submitted job
        xref: https://mapsor.amagi.tv/docs/#/paths/~1retry~1{id}/get
        :param job_id: job id
        """
        base_url = self.mapsor_details["url"]
        url = f"{base_url}/retry/{job_id}"
        params = {"token": self.mapsor_details["key"]}
        headers = {
            "Content-Type": "application/json",
            "Accept": "*/*",
        }

        response = self.http_requests_instance.call_get_requests(url, headers=headers, params=params)
        logging.info(f"Response from Mapsor : {response.text}")

    def return_job_logs(self, job_id: str):
        """
        This method to return job logs
        xref: https://mapsor.amagi.tv/docs/#/paths/~1logs~1{id}/get
        :param job_id: job id
        """
        base_url = self.mapsor_details["url"]
        url = f"{base_url}/logs/{job_id}"
        params = {"token": self.mapsor_details["key"]}
        headers = {
            "Content-Type": "application/json",
            "Accept": "*/*",
        }

        response = self.http_requests_instance.call_get_requests(url, headers=headers, params=params)
        logging.info(f"Response from Mapsor : {response.text}")


if __name__ == "__main__":
    # LOGGING #
    logging_format = "%(asctime)s::%(funcName)s::%(levelname)s:: %(message)s"
    logging.basicConfig(format=logging_format, level=logging.DEBUG, datefmt="%Y/%m/%d %H:%M:%S:%Z(%z)")
    logger = logging.getLogger(__name__)
