#!/usr/bin/python3
# coding= utf-8
"""
This is a helper script for reading application_configuration
"""
import json
import logging

config = None


class AppConfig:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = read_json(self.config_file)

    def get(self):
        return self.config


def read_json(json_file):
    try:
        with open(json_file) as file:
            return json.load(file)
    except Exception as e:
        logging.exception("Exception... {} File {}".format(str(e), json_file))
    return None


if __name__ == "__main__":
    app_config = AppConfig("config/ammo.magnolia.config.json")
    print(json.dumps(app_config.get(), indent=4))
