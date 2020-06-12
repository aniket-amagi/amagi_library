#!/usr/bin/python3
# coding= utf-8
"""
This is a helper script to provide hash of data
"""
import hashlib


def calculate_md5sum(data, byte=False):
    """
    This method returns md5sum of any provided data
    :param byte: flag to tell if data is bytes
    :param data: Data for which md5 needs to be calculated
    :return:
    """
    m = hashlib.md5()
    if byte:
        m.update(data)
    else:
        m.update(str(data).encode())
    return m.hexdigest()
