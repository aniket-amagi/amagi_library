#!/usr/bin/python3
# coding= utf-8
"""
This script is for chicane status manager
"""
import json
import logging
import re
import traceback
from copy import deepcopy
from datetime import datetime

from amagi_library.helper.http_requests import HTTPRequests
from workflows.transcode.status_manager.status_manager import StatusManager


class Chicane(StatusManager):
    history = {}
    last_updated_timestamp = None

    def __init__(self, **kwargs):
        cfg = kwargs["config"]["status_manager"]
        self.url = cfg["url"] if "url" in cfg else None
        self.request_body = cfg["body"] if "body" in cfg else None
        self.http_request = HTTPRequests()
        self.create_agent(cfg["get_agents_url"], self.request_body["id"])

    def create_agent(self, get_url, agent_name):
        request = {
            "name": agent_name,
            "code": agent_name
        }
        request_json = json.dumps(request)
        data = request_json.encode("utf-8")
        response = self.http_request.call_get_requests(get_url, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            agents_json = response.json()
            for agent in agents_json:
                if agent["name"] == agent_name:
                    logging.info(f"Agent {agent_name} present in Chicane..")
                    return
        response = self.http_request.call_post_requests(get_url, data=data,
                                                        headers={"Content-Type": "application/json"})
        if response.status_code == 201:
            logging.info(f"Agent {agent_name} successfully created")
            return True
        else:
            raise Exception(f"Error while creating agent; Chicane not initialized..")

    def get_last_status(self, asset_id):
        status_json = self.get_status()
        return status_json.get(asset_id) if status_json else None

    def publish_status(self, state, asset_id, **kwargs):
        request = deepcopy(self.request_body)
        params = {
            "complete": kwargs["complete"] if "complete" in kwargs else False
        }
        source_digest = kwargs["digest"] if "digest" in kwargs else None
        if source_digest:
            request["additional_info"] = {
                "digest": source_digest
            }
        request["id"] = f"{request['id']}"
        request["state"] = state
        request["asset-id"] = asset_id
        request["job-id"] = f"{request['type']}-{asset_id}"
        logging.info(f"Sending status update to chicane: {[request]}")
        data = json.dumps([request]).encode("utf-8")
        response = self.http_request.call_post_requests(self.url, data=data, params=params,
                                                        headers={"Content-Type": "application/json"})
        if response.status_code != 200:
            logging.warning(f"Chicane publish response: {response.status_code} {response.text}")

    def get_status(self, **kwargs):
        logging.info(f"Getting status from Chicane for {self.request_body}")
        current_ts = datetime.now()
        if Chicane.history and ((current_ts - Chicane.last_updated_timestamp).seconds < 360):
            logging.info("Recently retrieved history available")
            return Chicane.history
        response_data = self.http_request.call_get_requests(self.url)
        try:
            status_json = response_data.json()
            return self.parse_response(status_json)
        except Exception as e:
            logging.error(f"Error while parsing Chicane response {e} {traceback.format_exc}")

    def parse_response(self, status_json):
        if not status_json:
            logging.info("No previous message found..")
            return
        Chicane.last_updated_timestamp = datetime.now()
        job_type = self.request_body["type"]
        for status in status_json:
            if "history" in status and status["history"]:
                for hist in status["history"]:
                    job_id = hist["job-id"]
                    asset_id = re.search(f"{job_type}-(.*)", job_id)
                    if not asset_id:
                        continue
                    asset_id = asset_id.group(1)
                    digest = hist["additional_info"]["digest"] if "additional_info" in hist and "digest" in hist[
                        "additional_info"] else None
                    logging.info(f"Chicane history {asset_id} {digest}")
                    Chicane.history[asset_id] = {
                        "timestamp": hist["timestamp"],
                        "digest": digest
                    }
        return Chicane.history
