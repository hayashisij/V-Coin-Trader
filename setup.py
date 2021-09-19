from lib.crypt import Crypt


def main():
    print("---start---")
    crypt = Crypt()

    api_key = input("input your API Key: ")
    secret_key = input("input your SECRET API Key: ")
    key = crypt.key.decode(crypt.ENCODE)
    print(f"\tkey: {key}")
    print(f"\tapi_key: {api_key}")
    print(f"\tsecret_key: {secret_key}")

    crypted_api_key: str = crypt.encrypt(api_key)
    crypted_secret_key: str = crypt.encrypt(secret_key)
    print(f"\tcrypted api key: {crypted_api_key}")
    print(f"\tcrypted secret key: {crypted_secret_key}")

    check = Crypt()
    decrypted_api_key = check.decrypt(
        target_bytes=crypted_api_key.encode(Crypt.ENCODE), key=key.encode(Crypt.ENCODE)
    )
    decrypted_secret_key = check.decrypt(
        target_bytes=crypted_secret_key.encode(Crypt.ENCODE), key=key.encode(Crypt.ENCODE)
    )

    if api_key == decrypted_api_key:
        print(f"decrypt succeeded! API KEY: {decrypted_api_key}")
    else:
        print("decrypt failure API KEY")

    if secret_key == decrypted_secret_key:
        print(f"decrypt succeeded! SECRET KEY: {decrypted_secret_key}")
    else:
        print("decrypt failure SECRET KEY")

    crypt.save(api_key=crypted_api_key, secret_key=crypted_secret_key, key=key)
    print("---end---")


if __name__ == "__main__":
    main()
