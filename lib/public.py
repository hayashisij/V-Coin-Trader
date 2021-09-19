import sys
from datetime import date
import requests


class ApiError(Exception):
    pass


class ApiResponseError(ApiError):
    pass


class PublicAPI:
    def __init__(self):
        self.base_url = "https://api.bitflyer.com"

    def base_get(self, path: str = None, params: dict = None):
        url: str = self.base_url + path
        response = requests.get(url=url, params=params)

        if response is None:
            raise ApiResponseError("Response is Null")

        if response.status_code != 200:
            raise ApiResponseError(f"status code: {response.status_code}")

        return response

    # マーケットの一覧
    def get_markets(self):
        path: str = "/v1/getmarkets"
        return self.base_get(path=path)

    # 板情報
    def get_board(self, product_code: str = None):
        path: str = "/v1/getboard"
        params: dict = {"code": product_code}
        return self.base_get(path=path, params=params)

    # Ticker
    def get_ticker(self, product_code: str = None):
        path: str = "/v1/getticker"
        params: dict = {"code": product_code}
        return self.base_get(path=path, params=params)

    # 約定履歴
    def get_executions(self, product_code: str = None, count: int = 100, before: int = sys.maxsize,
                       after: int = -sys.maxsize):
        path: str = "/v1/getexecutions"
        params: dict = {"code": product_code, "count": count, "before": before, "after": after}
        return self.base_get(path=path, params=params)

    # 板の状態
    def get_board_state(self, product_code: str = None):
        path: str = "/v1/getboardstate"
        params: dict = {"code": product_code}
        return self.base_get(path=path, params=params)

    # 取引所の状態
    def get_health(self, product_code: str = None):
        path: str = "/v1/gethealth"
        params: dict = {"code": product_code}
        return self.base_get(path=path, params=params)

    # 法人アカウント最大レバレッジ
    def get_corporateleverage(self):
        path: str = "/v1/getcorporateleverage"
        return self.base_get(path=path)

    # チャット
    def get_chats(self, from_date: date):
        path: str = "/v1/getchats"
        params: dict = {"from_date": from_date.isoformat()}
        return self.base_get(path=path, params=params)
