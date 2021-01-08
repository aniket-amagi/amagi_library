#!/usr/bin/python3
# coding= utf-8
"""
This script is for dynamodb based status maanger
"""
import logging
from datetime import datetime

from workflows.transcode.status_manager.status_manager import StatusManager

from amagi_library.boto3_helper.dynamo import DynamoAccessor


class DynamoDB(StatusManager):
    history = {}
    last_updated_timestamp = None

    def __init__(self, **kwargs):
        cfg = kwargs["config"]["status_manager"]
        aws_details = cfg["aws_details"] if "aws_details" in cfg else None
        self.dynamo = DynamoAccessor(aws_details=aws_details)
        self.table_name = cfg["table_name"] if "table_name" in cfg else None
        self.request_body = cfg["body"] if "body" in cfg else None
        self.primary_key = "id"
        if not (aws_details and self.table_name):
            raise Exception("Invalid Dynamodb configuration. Exiting..")
        self.create_agent()

    def create_agent(self):
        if self.dynamo.is_table_present(self.table_name):
            return
        table = self.dynamo.create_table(self.table_name, self.primary_key)
        if not table:
            logging.error("Error while creating dynamodb table. Exiting..")

    def get_last_status(self, asset_id):
        job_id = f"{self.request_body['type']}-{asset_id}"
        logging.info(f"Searching for {job_id}")
        response = self.dynamo.read_table_item(self.table_name, self.primary_key, job_id)
        item = response["Item"] if "Item" in response else None
        logging.info(f"Item found {item}")
        return item

    def publish_status(self, state, asset_id, **kwargs):
        job_id = f"{self.request_body['type']}-{asset_id}"
        digest = kwargs["digest"] if "digest" in kwargs else None
        complete = kwargs["complete"] if "complete" in kwargs else False
        item = {
            "id": job_id,
            "asset_id": asset_id,
            "complete": complete,
            "digest": digest,
            "state": state,
            "time_stamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        logging.info(f"Publishing status {item}")
        if "item_present" not in kwargs or not kwargs["item_present"]:
            try:
                self.dynamo.add_item(self.table_name, item)
            except BaseException:
                logging.error("Error while publishing status to dynamodb")
        else:
            update_dict = {
                "time_stamp": {
                    "short_key": ":t",
                    "new_value": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
                }
            }
            if digest:
                update_dict["digest"] = {
                    "short_key": ":d",
                    "new_value": digest
                }

            try:
                self.dynamo.update_item(self.table_name, "id", job_id, update_dict)
            except BaseException:
                logging.error("Error while publishing(Updating) status to dynamodb")

    def get_status(self, **kwargs):
        return
