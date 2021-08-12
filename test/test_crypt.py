from lib.crypt import Crypt
import json

if __name__ == "__main__":
    crypt = Crypt()

    api_key, secret_key = crypt.load()
    print(api_key)
    print(secret_key)
