import sys

from requests import Response
import requests
from datetime import date, datetime


class BitFlyerError(Exception):
    pass


class ApiRequestError(BitFlyerError):
    pass


class RequestParamError(BitFlyerError):
    pass


class BitFlyer:
    def __init__(self):
        self.base_url: str = "https://api.bitflyer.com"
        API_KEY: str = ""
        API_SECRET_KEY: str = ""
        # TODO: 暗号化してあるAPI_KEYを復号してTupleで返すメソッドを作る
        API_KEY, API_SECRET_KEY = decryption_api_keys()
        timestamp: datetime = datetime.now()
        self.header: dict = {
            'ACCESS-KEY': API_KEY,
            'ACCESS-TIMESTAMP': timestamp,
            'ACCESS-SIGN': API_SECRET_KEY,
            'Content-Type': 'application/json'
        }

    def do_request(self, method: str, endpoint: str, params: dict = None, data: dict = None) -> Response:
        url: str = self.base_url + endpoint
        response: Response
        if method == "GET":
            if params is None:
                raise RequestParamError("GET method require 'params' as dict")
            response: Response = requests.get(url=url, params=params)
        elif method == "POST":
            if params is not None:
                response: Response = requests.post(url=url, params=params)
            elif data is not None:
                response: Response = requests.post(url=url, data=data)
            else:
                raise RequestParamError("POST method require 'params' as dict or 'data' as dict")
        else:
            # PUT
            response = requests.put(url=url, params=params)

        if response is not None:
            if response.status_code != 200:
                raise ApiRequestError(f"status code: {response.status_code}")
        return response

    # HTTP Public APIのエンドポイント
    def get_markets(self) -> Response:
        endpoint: str = "/v1/getmarkets"
        method: str = "GET"
        return self.do_request(method=method, endpoint=endpoint)

    def get_board(self, cryptocurrency_code: str) -> Response:
        endpoint: str = "/v1/getboard"
        method: str = "GET"
        payload: dict = {"product_code": cryptocurrency_code}
        return self.do_request(method=method, endpoint=endpoint, params=payload)

    def get_ticker(self,  cryptocurrency_code: str) -> Response:
        endpoint: str = "/v1/getticker"
        method: str = "GET"
        payload: dict = {"product_code": cryptocurrency_code}
        return self.do_request(method=method, endpoint=endpoint, params=payload)

    def get_executions(self, cryptocurrency_code: str, count: int = 100, before: int = sys.maxsize , after: int = -sys.maxsize):
        endpoint: str = "/v1/getexecutions"
        method: str = "GET"
        payload: dict = {"product_code": cryptocurrency_code, "count": count, "before": before, "after": after}
        return self.do_request(method=method, endpoint=endpoint, params=payload)

    def get_boardstate(self,  cryptocurrency_code: str) -> Response:
        endpoint: str = "/v1/getboardstate"
        method: str = "GET"
        payload: dict = {"product_code": cryptocurrency_code}
        return self.do_request(method=method, endpoint=endpoint, params=payload)

    def get_health(self,  cryptocurrency_code: str) -> Response:
        endpoint: str = "/v1/gethealth"
        method: str = "GET"
        payload: dict = {"product_code": cryptocurrency_code}
        return self.do_request(method=method, endpoint=endpoint, params=payload)

    def get_corporateleverage(self) -> Response:
        endpoint: str = "/v1/getcorporateleverage"
        method: str = "GET"
        return self.do_request(method=method, endpoint=endpoint)

    def get_chats(self,  from_date: date) -> Response:
        endpoint: str = "/v1/getchats"
        method: str = "GET"
        payload: dict = {"from_date": from_date.strftime('%Y-%m-%d')}
        return self.do_request(method=method, endpoint=endpoint, params=payload)

    # HTTP Private APIのエンドポイント
    def get_permissions(self) -> Response:
        endpoint: str = "/v1/me/getpermissions"
        method: str = "GET"
        return self.do_request(method=method, endpoint=endpoint)

    def get_balance(self) -> Response:
        endpoint: str = "/v1/me/getbalance"
        method: str = "GET"
        return self.do_request(method=method, endpoint=endpoint)

    def get_collateral(self) -> Response:
        endpoint: str = "/v1/me/getcollateral"
        method: str = "GET"
        return self.do_request(method=method, endpoint=endpoint)

    def get_collateralaccounts(self) -> Response:
        endpoint: str = "/v1/me/getcollateralaccounts"
        method: str = "GET"
        return self.do_request(method=method, endpoint=endpoint)

    def get_addresses(self) -> Response:
        endpoint: str = "/v1/me/getaddresses"
        method: str = "GET"
        return self.do_request(method=method, endpoint=endpoint)

    def get_coinins(self, count: int = 100, before: int = sys.maxsize , after: int = -sys.maxsize):
        endpoint: str = "/v1/me/getcoinins"
        method: str = "GET"
        payload: dict = {"count": count, "before": before, "after": after}
        return self.do_request(method=method, endpoint=endpoint, params=payload)

    def get_coinouts(self, count: int = 100, before: int = sys.maxsize , after: int = -sys.maxsize):
        endpoint: str = "/v1/me/getcoinouts"
        method: str = "GET"
        payload: dict = {"count": count, "before": before, "after": after}
        return self.do_request(method=method, endpoint=endpoint, params=payload)

    def get_bankaccounts(self) -> Response:
        endpoint: str = "/v1/me/getbankaccounts"
        method: str = "GET"
        return self.do_request(method=method, endpoint=endpoint)

    def get_deposits(self, count: int = 100, before: int = sys.maxsize, after: int = -sys.maxsize):
        endpoint: str = "/v1/me/getdeposits"
        method: str = "GET"
        payload: dict = {"count": count, "before": before, "after": after}
        return self.do_request(method=method, endpoint=endpoint, params=payload)

    # TODO: POSTのBODYパラメータがこの渡し方で機能するかの確認
    def post_withdraw(self, currency_code: str, bank_account_id: int, amount: int, code: int):
        endpoint: str = "/v1/me/withdraw"
        method: str = "POST"
        payload: dict = {"currency_code": currency_code, "bank_account_id": bank_account_id, "amount": amount, "code": code}
        return self.do_request(method=method, endpoint=endpoint, params=payload)

    def get_withdrawals(self, count: int = 100, before: int = sys.maxsize , after: int = -sys.maxsize, message_id: str = ""):
        endpoint: str = "/v1/me/getwithdrawals"
        method: str = "GET"
        payload: dict = {"count": count, "before": before, "after": after, "message_id": message_id}
        return self.do_request(method=method, endpoint=endpoint, params=payload)

    # TODO: POSTのBODYパラメータがこの渡し方で機能するかの確認
    # TODO: sideは"BUY"か"SELL"以外は指定できないため、例外処理の方法を検討する
    def post_sendchildorder(self, product_code: str, child_order_type: str, side: str, price: int, size: int, minute_to_expire: int = 43200, time_in_force: str = "GTC"):
        endpoint: str = "/v1/me/sendchildorder"
        method: str = "POST"
        payload: dict = {"product_code": product_code, "child_order_type": child_order_type, "side": side, "price": price, "size": size, "minute_to_expire": minute_to_expire, "time_in_force": time_in_force}
        return self.do_request(method=method, endpoint=endpoint, data=payload)

    def cancelchildorder_core(self, params: list = None):
        if params is None:
            params = list()
        endpoint: str = "/v1/me/cancelchildorder"
        method: str = "POST"
        payload: dict = {"list": params}
        return self.do_request(method=method, endpoint=endpoint, params=payload)

    def post_cancelchildorder(self, **kwargs):
        # FIXME: あとで実装を考える
        # https://lightning.bitflyer.com/docs?lang=ja#%E6%B3%A8%E6%96%87%E3%82%92%E3%82%AD%E3%83%A3%E3%83%B3%E3%82%BB%E3%83%AB%E3%81%99%E3%82%8B
        pass

    # https://lightning.bitflyer.com/docs?lang=ja#http-api
    # TODO: 新規の親注文を出す（特殊注文）
    # TODO: 尾や注文をキャンセルする
    # TODO: 全ての注文をキャンセルする
    # TODO: 注文の一覧を取得
    # TODO: 親注文の一覧を取得
    # TODO: 親注文の詳細を取得
    # TODO: 約定の一覧を取得
    # TODO: 残高履歴を取得
    # TODO: 建玉の一覧を取得
    # TODO: 証拠金の変動履歴を取得
    # TODO: 取引手数料を取得

