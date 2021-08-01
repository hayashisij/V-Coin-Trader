from base64 import b64encode, b64decode
from Crypto.Cipher import AES
import random
import string


def key_gen(num: int) -> str:
    """
    暗号化キーとしてい使うランダムな{num}桁の文字列を生成する
    :param num:
    :return: str
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=num))


class Crypt:
    def __init__(self, salt='SlTKeYOpHygTYkP3'):
        self.salt = salt
        self.enc_dec_method = 'utf-8'

    def encrypt(self, str_to_enc: str, str_key: str) -> str:
        try:
            aes_obj = AES.new(str_key, AES.MODE_CBC, self.salt)
            hx_enc = aes_obj.encrypt(str_to_enc)
            mret: str = b64encode(hx_enc).decode(self.enc_dec_method)
            return mret
        except ValueError as value_error:
            if value_error.args[0] == 'IV must be 16 bytes long':
                raise ValueError('Encryption Error: SALT must be 16 characters long')
            elif value_error.args[0] == 'AES key must be either 16, 24, or 32 bytes long':
                raise ValueError('Encryption Error: Encryption key must be either 16, 24, or 32 characters long')
            else:
                raise ValueError(value_error)

    def decrypt(self, enc_str, str_key):
        try:
            aes_obj = AES.new(str_key, AES.MODE_CBC, self.salt)
            str_tmp = b64decode(enc_str.encode(self.enc_dec_method))
            str_dec = aes_obj.decrypt(str_tmp)
            mret = str_dec.decode(self.enc_dec_method)
            return mret
        except ValueError as value_error:
            if value_error.args[0] == 'IV must be 16 bytes long':
                raise ValueError('Decryption Error: SALT must be 16 characters long')
            elif value_error.args[0] == 'AES key must be either 16, 24, or 32 bytes long':
                raise ValueError('Decryption Error: Encryption key must be either 16, 24, or 32 characters long')
            else:
                raise ValueError(value_error)
