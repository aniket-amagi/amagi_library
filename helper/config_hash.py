#!/usr/bin/python3
# coding= utf-8
"""
This is a helper script to encrypt and decrypt environment variables
"""
import base64
import json
import logging
import zlib


def decode_config(hash):
    """
    Decode base64 hash message to normal messages
    :param hash: base64 hash message
    :return: normal message
    """
    encoded = hash.encode()
    decoded = base64.b64decode(encoded)
    decompressed = zlib.decompress(decoded)
    config_text = decompressed.decode()
    config = json.loads(config_text)
    return config


def encode_config(message):
    """
    Encode normal message to base64 hash messages
    :param message: normal message
    :return: encoded base64 hash message
    """
    config_text = json.dumps(message)
    encoded = config_text.encode()
    compressed = zlib.compress(encoded)
    encoded = base64.b64encode(compressed)
    result = encoded.decode()
    return result


if __name__ == "__main__":
    # LOGGING #
    logging_format = "%(asctime)s::%(funcName)s::%(levelname)s:: %(message)s"
    logging.basicConfig(format=logging_format, level=logging.INFO, datefmt="%Y/%m/%d:%H:%M:%S:%Z:%z")
    logger = logging.getLogger(__name__)
    with open("config.prod.json") as file:
        config = json.load(file)
    encoded = encode_config(config)
    config_decoded = decode_config(encoded)
    with open("config_decoded.json", "w") as file2:
        json.dump(config_decoded, file2, indent=4)
