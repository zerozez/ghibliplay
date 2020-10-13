"""
    Requests tools module contains additional function and classes to help
    working with requests
"""
import requests


def get_json(url):
    """ get_json help to receive data from url endpoint as an JSON object.

    Parameters:
        url (str) -- Url for data consuming

    Returns:
        requests.Response object

    """
    header = {
        "Content-Type": "application/json",
    }

    return requests.get(url, headers=header)


class InvalidResponse(Exception):
    """Exception raised for errors in the input.

    Attributes:
        code (int) -- status code of response
        raw (str) -- raw data of response
    """

    def __init__(self, code, raw):
        self.code = code
        self.raw = raw
