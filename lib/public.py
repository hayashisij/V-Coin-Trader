import sys
import requests
from requests import Response


class ApiError(Exception):
    def ApiRequestError(self, res: response = response):
        if res is None:
            print(f"status code: null")
        else:
            print(f"status code: {res.status_code}")


class PublicAPI:
    def __init__(self):
        self.base_url = "https://api.bitflyer.com"

    def base_get(self, path: str = None, params: dict = None):
        url: str = self.base_url + path
        response = requests.get(url=url, params=params)

        if response is None:
            raise ApiRequestError(response)

        if response.status_code != 200:
            raise ApiError.ApiRequestError(response)

        return response

    # マーケットの一覧
    def get_markets(self):
        path: str = "/v1/getmarkets"
        return self.base_get(path=path)
