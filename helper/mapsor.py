#!/usr/bin/python3
# coding= utf-8
"""
This is a wrapper script for mapsor
Xref : https://mapsor.amagi.tv/docs/
"""
import json
import logging

from amagi_library.helper.http_requests import HTTPRequests


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

    def create_container_job(self, customer, cloud, region, job_id, **kwargs):
        """
        This method schedules a container job
        xref: https://mapsor.amagi.tv/docs/#operation/createContainerJob
        :param customer: customer
        :param cloud: cloud provider
        :param region: region
        :param job_id: job id 
        :param kwargs: optional arguments
        """
        payload_dict = {
            "cloud": cloud,
            "region": region,
            "id": job_id,
            "customer": customer
        }
        payload_dict.update(kwargs)
        payload = json.dumps(payload_dict)

        base_url = self.mapsor_details["mapsor_url"]
        url = f"{base_url}/submit"
        params = {"token": self.mapsor_details["mapsor_key"]}
        headers = {
            "Content-Type": "application/json",
            "Accept": "*/*",
        }

        response = self.http_requests_instance.call_post_requests(url, data=payload, headers=headers, params=params)
        logging.info(f"Response from Mapsor : {response.text}")

    def submitted_job_status(self, job_id):
        """
        This method schedules a container job
        xref: https://mapsor.amagi.tv/docs/#/paths/~1status~1{id}/get
        :param job_id: job id
        """

        base_url = self.mapsor_details["mapsor_url"]
        url = f"{base_url}/status/{job_id}"
        params = {"token": self.mapsor_details["mapsor_key"]}
        headers = {
            "Content-Type": "application/json",
            "Accept": "*/*",
        }

        response = self.http_requests_instance.call_get_requests(url, headers=headers, params=params)
        logging.info(f"Response from Mapsor : {response.text}")

    def cancel_submitted_job(self, job_id):
        """
        This method to cancel a submitted job
        xref: https://mapsor.amagi.tv/docs/#/paths/~1cancel~1{id}/get
        :param job_id: job id
        """

        base_url = self.mapsor_details["mapsor_url"]
        url = f"{base_url}/cancel/{job_id}"
        params = {"token": self.mapsor_details["mapsor_key"]}
        headers = {
            "Content-Type": "application/json",
            "Accept": "*/*",
        }

        response = self.http_requests_instance.call_get_requests(url, headers=headers, params=params)
        logging.info(f"Response from Mapsor : {response.text}")

    def retry_submitted_job(self, job_id):
        """
        This method to retry a submitted job
        xref: https://mapsor.amagi.tv/docs/#/paths/~1retry~1{id}/get
        :param job_id: job id
        """
        base_url = self.mapsor_details["mapsor_url"]
        url = f"{base_url}/retry/{job_id}"
        params = {"token": self.mapsor_details["mapsor_key"]}
        headers = {
            "Content-Type": "application/json",
            "Accept": "*/*",
        }

        response = self.http_requests_instance.call_get_requests(url, headers=headers, params=params)
        logging.info(f"Response from Mapsor : {response.text}")

    def return_job_logs(self, job_id):
        """
        This method to return job logs
        xref: https://mapsor.amagi.tv/docs/#/paths/~1logs~1{id}/get
        :param job_id: job id
        """
        base_url = self.mapsor_details["mapsor_url"]
        url = f"{base_url}/logs/{job_id}"
        params = {"token": self.mapsor_details["mapsor_key"]}
        headers = {
            "Content-Type": "application/json",
            "Accept": "*/*",
        }

        response = self.http_requests_instance.call_get_requests(url, headers=headers, params=params)
        logging.info(f"Response from Mapsor : {response.text}")
