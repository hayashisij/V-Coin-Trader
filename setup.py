from lib.encrypt import key_gen, Crypt
import json
import sys


def save_to_file(key: str, api_key: str, secret_key: str) -> None:
    json_dict: dict = {"KEY": key, "API_KEY": api_key, "API_SECRET_KEY": secret_key}
    with open("./conf/credentials.json", "w") as file:
        json.dump(json_dict, file, indent=4)


def main():
    key: str = key_gen(32)
    crypt: Crypt = Crypt()
    api_key: str = input("input your API_KEY of bitflyer: ")
    secret_key: str = input("input your API_SECRET_KEY of bitflyer: ")

    # API_KEYを暗号化
    crypted_api_key: str = crypt.encrypt(api_key, key)
    # SPI_SECRET_KEYを暗号化
    crypted_secret_key: str = crypt.encrypt(secret_key, key)

    # 復号化したAPI_KEY
    decrypted_api_key: str = crypt.decrypt(crypted_api_key, key)
    # 復号化したAPI_SECRET_KEY
    decrypted_secret_key: str = crypt.decrypt(crypted_secret_key, key)

    # チェック
    if api_key != decrypted_api_key:
        print("API_KEYの暗号化失敗")
        sys.exit(1)
    if secret_key != decrypted_secret_key:
        print("API_SECRET_KEYの暗号化失敗")
        sys.exit(1)

    # confファイルに保存
    save_to_file(key=key, api_key=crypted_api_key, secret_key=crypted_secret_key)
    print("end")


if __name__ == "__main__":
    main()
