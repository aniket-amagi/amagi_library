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
        logging.exception("Exception... [%s] File [%s]".format(str(e), json_file))
    return None

if __name__ == "__main__":
    app_config = AppConfig("config/config.dev.json")
    print(json.dumps(app_config.get(), indent=4))