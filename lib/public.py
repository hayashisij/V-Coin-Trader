import sys
import requests

from requests import Response
from datetime import date, datetime
from crypt import Crypt

class BitFlyerError(Exception):
    pass


class ApiRequestError(BitFlyerError):
    pass


class RequestParamError(BitFlyerError):
    pass


class PublicAPI:
    def __init__(self):
        self.url = "https://api.bitflyer.com"
