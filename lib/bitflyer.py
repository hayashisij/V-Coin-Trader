import sys
import requests

from requests import Response
from datetime import date, datetime
from encrypt import Crypt

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
        # API_KEY, API_SECRET_KEY = decryption_api_keys()

        crypt = Crypt()

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
    # マーケットの一覧
    def get_markets(self) -> Response:
        endpoint: str = "/v1/getmarkets"
        method: str = "GET"
        return self.do_request(method=method, endpoint=endpoint)

    # 板情報
    def get_board(self, cryptocurrency_code: str) -> Response:
        endpoint: str = "/v1/getboard"
        method: str = "GET"
        payload: dict = {"product_code": cryptocurrency_code}
        return self.do_request(method=method, endpoint=endpoint, params=payload)

    # Ticker
    def get_ticker(self,  cryptocurrency_code: str) -> Response:
        endpoint: str = "/v1/getticker"
        method: str = "GET"
        payload: dict = {"product_code": cryptocurrency_code}
        return self.do_request(method=method, endpoint=endpoint, params=payload)

    # 約定履歴
    def get_executions(self, cryptocurrency_code: str, count: int = 100, before: int = sys.maxsize , after: int = -sys.maxsize):
        endpoint: str = "/v1/getexecutions"
        method: str = "GET"
        payload: dict = {"product_code": cryptocurrency_code, "count": count, "before": before, "after": after}
        return self.do_request(method=method, endpoint=endpoint, params=payload)

    # 板の状態
    def get_board_state(self,  cryptocurrency_code: str) -> Response:
        endpoint: str = "/v1/getboardstate"
        method: str = "GET"
        payload: dict = {"product_code": cryptocurrency_code}
        return self.do_request(method=method, endpoint=endpoint, params=payload)

    # 取引所の状態
    def get_health(self,  cryptocurrency_code: str) -> Response:
        endpoint: str = "/v1/gethealth"
        method: str = "GET"
        payload: dict = {"product_code": cryptocurrency_code}
        return self.do_request(method=method, endpoint=endpoint, params=payload)

    # 法人アカウント最大レバレッジ
    def get_corporate_leverage(self) -> Response:
        endpoint: str = "/v1/getcorporateleverage"
        method: str = "GET"
        return self.do_request(method=method, endpoint=endpoint)

    # チャット
    def get_chats(self,  from_date: date) -> Response:
        endpoint: str = "/v1/getchats"
        method: str = "GET"
        payload: dict = {"from_date": from_date.strftime('%Y-%m-%d')}
        return self.do_request(method=method, endpoint=endpoint, params=payload)

    # HTTP Private APIのエンドポイント
    # HTTP Private API
    def get_permissions(self) -> Response:
        endpoint: str = "/v1/me/getpermissions"
        method: str = "GET"
        return self.do_request(method=method, endpoint=endpoint)

    # 資産残高を取得
    def get_balance(self) -> Response:
        endpoint: str = "/v1/me/getbalance"
        method: str = "GET"
        return self.do_request(method=method, endpoint=endpoint)

    # 証拠金の状態を取得
    def get_collateral(self) -> Response:
        endpoint: str = "/v1/me/getcollateral"
        method: str = "GET"
        return self.do_request(method=method, endpoint=endpoint)

    # 証拠金の状態を取得（通貨別）
    def get_collateral_accounts(self) -> Response:
        endpoint: str = "/v1/me/getcollateralaccounts"
        method: str = "GET"
        return self.do_request(method=method, endpoint=endpoint)

    # 預入用アドレス取得
    def get_addresses(self) -> Response:
        endpoint: str = "/v1/me/getaddresses"
        method: str = "GET"
        return self.do_request(method=method, endpoint=endpoint)

    # 仮想通貨預入履歴
    def get_coin_ins(self, count: int = 100, before: int = sys.maxsize , after: int = -sys.maxsize):
        endpoint: str = "/v1/me/getcoinins"
        method: str = "GET"
        payload: dict = {"count": count, "before": before, "after": after}
        return self.do_request(method=method, endpoint=endpoint, params=payload)

    # 仮想通貨送付履歴
    def get_coin_outs(self, count: int = 100, before: int = sys.maxsize , after: int = -sys.maxsize):
        endpoint: str = "/v1/me/getcoinouts"
        method: str = "GET"
        payload: dict = {"count": count, "before": before, "after": after}
        return self.do_request(method=method, endpoint=endpoint, params=payload)

    # 銀行口座一覧取得
    def get_bank_accounts(self) -> Response:
        endpoint: str = "/v1/me/getbankaccounts"
        method: str = "GET"
        return self.do_request(method=method, endpoint=endpoint)

    # 入金履歴
    def get_deposits(self, count: int = 100, before: int = sys.maxsize, after: int = -sys.maxsize):
        endpoint: str = "/v1/me/getdeposits"
        method: str = "GET"
        payload: dict = {"count": count, "before": before, "after": after}
        return self.do_request(method=method, endpoint=endpoint, params=payload)

    # 出金
    # TODO: POSTのBODYパラメータがこの渡し方で機能するかの確認
    def post_withdraw(self, currency_code: str, bank_account_id: int, amount: int, code: int):
        endpoint: str = "/v1/me/withdraw"
        method: str = "POST"
        payload: dict = {"currency_code": currency_code, "bank_account_id": bank_account_id, "amount": amount, "code": code}
        return self.do_request(method=method, endpoint=endpoint, params=payload)

    # 出金履歴
    def get_withdrawals(self, count: int = 100, before: int = sys.maxsize , after: int = -sys.maxsize, message_id: str = ""):
        endpoint: str = "/v1/me/getwithdrawals"
        method: str = "GET"
        payload: dict = {"count": count, "before": before, "after": after, "message_id": message_id}
        return self.do_request(method=method, endpoint=endpoint, params=payload)

    # 新規注文を出す
    # TODO: POSTのBODYパラメータがこの渡し方で機能するかの確認
    # TODO: sideは"BUY"か"SELL"以外は指定できないため、例外処理の方法を検討する
    def post_send_child_order(self, product_code: str, child_order_type: str, side: str, price: int, size: int, minute_to_expire: int = 43200, time_in_force: str = "GTC"):
        endpoint: str = "/v1/me/sendchildorder"
        method: str = "POST"
        payload: dict = {"product_code": product_code, "child_order_type": child_order_type, "side": side, "price": price, "size": size, "minute_to_expire": minute_to_expire, "time_in_force": time_in_force}
        return self.do_request(method=method, endpoint=endpoint, data=payload)

    # 注文をキャンセルする
    def post_cancel_child_order_core(self, params: list = None):
        if params is None:
            params = list()
        endpoint: str = "/v1/me/cancelchildorder"
        method: str = "POST"
        payload: dict = {"list": params}
        return self.do_request(method=method, endpoint=endpoint, params=payload)

    def post_cancel_child_order(self, **kwargs):
        # FIXME: あとで実装を考える
        # https://lightning.bitflyer.com/docs?lang=ja#%E6%B3%A8%E6%96%87%E3%82%92%E3%82%AD%E3%83%A3%E3%83%B3%E3%82%BB%E3%83%AB%E3%81%99%E3%82%8B
        pass

    # 新規の親注文を出す（特殊注文）
    def post_send_parent_order_core(self, params: list = None):
        if params is None:
            params = list()
        endpoint: str = "/v1/me/sendparentorder"
        method: str = "POST"
        payload: dict = {"list": params}
        return self.do_request(method=method, endpoint=endpoint, params=payload)

    def post_send_parent_order(self, **kwargs):
        # FIXME: あとで実装を考える
        # https://lightning.bitflyer.com/docs?lang=ja#%E6%96%B0%E8%A6%8F%E3%81%AE%E8%A6%AA%E6%B3%A8%E6%96%87%E3%82%92%E5%87%BA%E3%81%99%E7%89%B9%E6%AE%8A%E6%B3%A8%E6%96%87
        pass

    # 親注文をキャンセルする
    def post_cancel_parent_order(self, product_code: str, parent_order_id: str, parent_order_acceptance_id: str):
        endpoint: str = "/v1/me/cancelparentorder"
        method: str = "POST"
        payload: dict = {"product_code": product_code, "parent_order_id": parent_order_id, "parent_order_acceptance_id": parent_order_acceptance_id}
        return self.do_request(method=method, endpoint=endpoint, params=payload)

    # 全ての注文をキャンセルする
    def post_cancel_all_child_orders(self, product_code: str):
        endpoint: str = "/v1/me/cancelallchildorders"
        method: str = "POST"
        payload: dict = {"product_code": product_code}
        return self.do_request(method=method, endpoint=endpoint, params=payload)

    # 注文の一覧を取得
    def get_child_orders(self, product_code: str, count: int = 100, before: int = sys.maxsize , after: int = -sys.maxsize, child_order_state: str = "", child_order_id: str = "", child_order_acceptance_id: str = "", parent_order_id: str = ""):
        endpoint: str = "/v1/me/getchildorders"
        method: str = "GET"
        payload: dict = {"product_code": product_code, "count": count, "before": before, "after": after, "child_order_state": child_order_state, "child_order_id": child_order_id, "child_order_acceptance_id": child_order_acceptance_id, "parent_order_id": parent_order_id}
        return self.do_request(method=method, endpoint=endpoint, params=payload)

    # 親注文の一覧を取得
    def get_parent_orders(self, product_code: str, count: int = 100, before: int = sys.maxsize , after: int = -sys.maxsize, parent_order_state: str = ""):
        endpoint: str = "/v1/me/getparentorders"
        method: str = "GET"
        payload: dict = {"product_code": product_code, "count": count, "before": before, "after": after, "child_order_state": parent_order_state}
        return self.do_request(method=method, endpoint=endpoint, params=payload)

    # 親注文の詳細を取得
    def get_parent_order(self, product_code: str, count: int = 100, before: int = sys.maxsize , after: int = -sys.maxsize, parent_order_state: str = ""):
        endpoint: str = "/v1/me/getparentorder"
        method: str = "GET"
        payload: dict = {"product_code": product_code, "count": count, "before": before, "after": after, "child_order_state": parent_order_state}
        return self.do_request(method=method, endpoint=endpoint, params=payload)

    # 約定の一覧を取得
    def get_executions(self, product_code: str, count: int = 100, before: int = sys.maxsize , after: int = -sys.maxsize, child_order_id: str = "", child_order_acceptance_id: str = ""):
        endpoint: str = "/v1/me/getexecutions"
        method: str = "GET"
        payload: dict = {"product_code": product_code, "count": count, "before": before, "after": after, "child_order_id": child_order_id, "child_order_acceptance_id": child_order_acceptance_id}
        return self.do_request(method=method, endpoint=endpoint, params=payload)

    # 残高履歴を取得
    def get_balance_history(self, currency_code: str, count: int = 100, before: int = sys.maxsize , after: int = -sys.maxsize):
        endpoint: str = "/v1/me/getbalancehistory"
        method: str = "GET"
        payload: dict = {"currency_code": currency_code, "count": count, "before": before, "after": after}
        return self.do_request(method=method, endpoint=endpoint, params=payload)

    # 建玉の一覧を取得
    def get_positions(self, product_code: str):
        endpoint: str = "/v1/me/getpositions"
        method: str = "GET"
        payload: dict = {"product_code": product_code}
        return self.do_request(method=method, endpoint=endpoint, params=payload)

    # 証拠金の変動履歴を取得
    def get_collateral_history(self, count: int = 100, before: int = sys.maxsize , after: int = -sys.maxsize):
        endpoint: str = "/v1/me/getcollateralhistory"
        method: str = "GET"
        payload: dict = {"count": count, "before": before, "after": after}
        return self.do_request(method=method, endpoint=endpoint, params=payload)

    # 取引手数料を取得
    def get_trading_commission(self, product_code: str):
        endpoint: str = "/v1/me/gettradingcommission"
        method: str = "GET"
        payload: dict = {"product_code": product_code}
        return self.do_request(method=method, endpoint=endpoint, params=payload)
