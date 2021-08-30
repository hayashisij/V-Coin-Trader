from .crypt import Crypt
import hashlib
import hmac
import json
import requests
from requests import Response
import time


def get_keys() -> tuple:
    crypo = Crypt()
    return crypo.load()


class PrivateApi:
    def __init__(self):
        self.url = 'https://api.bitflyer.jp'
        self.api_key, self.secret_key = get_keys()

    def base_get(self, path: str = None, **kwargs) -> dict:
        timestamp: str = str(int(time.time()))
        uri: str = self.url + path
        method: str = "GET"
        text: str = timestamp + method + path
        sign: str = hmac.new(self.secret_key.encode("utf-8"), text.encode("utf-8"), hashlib.sha256).hexdigest()
        headers: dict = {
            'ACCESS-KEY': self.api_key,
            'ACCESS-TIMESTAMP': timestamp,
            'ACCESS-SIGN': sign
        }
        res: Response = requests.get(uri, headers=headers)
        if res.text:
            # TODO: namedtupleかdataclassにしたほうが良いかも？
            result = {"status_code": res.status_code, "response": json.loads(res.text)}
        else:
            # TODO: namedtupleかdataclassにしたほうが良いかも？
            result = {"status_code": res.status_code}
        return result

    def base_post(self, path: str = None, **kwargs) -> dict:
        timestamp: str = str(int(time.time()))
        body: str = str(kwargs)
        method: str = "POST"
        uri: str = self.url + path
        text: str = timestamp + method + path + body
        sign: str = hmac.new(self.secret_key.encode("utf-8"), text.encode("utf-8"), hashlib.sha256).hexdigest()
        headers: dict = {
            'ACCESS-KEY': self.api_key,
            'ACCESS-TIMESTAMP': timestamp,
            'ACCESS-SIGN': sign,
            'Content-Type': 'application/json'
        }
        res: Response = requests.post(uri, headers=headers, data=body)
        if res.text:
            # TODO: namedtupleかdataclassにしたほうが良いかも？
            result = {"status_code": res.status_code, "response": json.loads(res.text)}
        else:
            # TODO: namedtupleかdataclassにしたほうが良いかも？
            result = {"status_code": res.status_code}
        return result

    def get_permissions(self):
        """
        API キーの権限を取得
        :return: {status_code: int, response: list[str]}
        """
        path: str = "/v1/me/getpermissions"
        return self.base_get(path=path)

    def get_balance(self):
        """
        資産残高を取得
        :return: {status_code: int, response: list[dict]}
        """
        path: str = "/v1/me/getbalance"
        return self.base_get(path=path)

    def get_collateral(self):
        """
        証拠金の状態を取得
        collateral: 預け入れた証拠金の評価額(円)
        open_position_pnl: 建玉の評価損益(円)
        require_collateral: 現在の必要証拠金(円)
        keep_rate: 現在の証拠金維持率
        :return: {status_code: int, response: dict}
        """
        path: str = "/v1/me/getcollateral"
        return self.base_get(path=path)

    def get_collateral_accounts(self):
        """
        通過別の証拠金の数量を取得
        :return: {status_code: int, response: list[dict]}
        """
        path: str = "/v1/me/getcollateralaccounts"
        return self.base_get(path=path)

    def get_addresses(self) ->dict:
        """
        仮想通貨をbirFlyerアカウントに預入るためのアドレスを取得
        :return: {status_code: int, response: list[dict]}
        """
        path: str = "/v1/me/getcollateralaccounts"
        return self.base_get(path=path)
