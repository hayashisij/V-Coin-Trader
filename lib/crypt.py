import json
from typing import Final

from cryptography.fernet import Fernet


class Crypt:
    ENCODE: Final[str] = "utf-8"

    def __init__(self, key: bytes = None):
        if key is not None:
            self.key: bytes = key
        else:
            self.key = Fernet.generate_key()
        self.f = Fernet(self.key)

    def encrypt(self, target_str: str) -> str:
        return self.f.encrypt(target_str.encode(Crypt.ENCODE)).decode(Crypt.ENCODE)

    def decrypt(self, target_bytes: bytes, key: bytes) -> str:
        self.f = Fernet(key)
        return self.f.decrypt(target_bytes).decode(Crypt.ENCODE)

    @staticmethod
    def save(api_key: str, secret_key: str, key: str) -> None:
        save_dict: dict = {"API_KEY": api_key, "SECRET_API_KEY": secret_key, "KEY": key}
        with open("./conf/credentials.json", "w") as f:
            json.dump(save_dict, f, indent=4)

    def load(self) -> tuple:
        with open("./conf/credentials.json", "r") as f:
            credentials: dict = json.load(f)
            str_key: str = credentials.get("KEY")
            str_api_key: str = credentials.get("API_KEY")
            str_secret_key: str = credentials.get("SECRET_API_KEY")

            return self.decrypt(
                target_bytes=str_api_key.encode(Crypt.ENCODE), key=str_key.encode(Crypt.ENCODE)
            ), self.decrypt(
                target_bytes=str_secret_key.encode(Crypt.ENCODE), key=str_key.encode(Crypt.ENCODE)
            )
