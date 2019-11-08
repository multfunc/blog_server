from urllib import parse
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5

from Crypto.Hash import SHA


# def encrypt(clear_data,code="123456"):
#     # print(bytes(clear_data.encode("utf-8")))
#     message=bytes(clear_data.encode("utf-8"))
#     h=SHA.new(message)
#     public_key=RSA.import_key(open("receiver.pem").read())
#     cliper_rsa=PKCS1_v1_5.new(public_key)
#     result=cliper_rsa.encrypt(message+h.digest())
#     print(result)
#     return result

def decrypt_by_PKCS1_v1_5(cipher_data, code="123456"):
    """
    输入加密数据，解密出明文字符串
    适配的是前端的JSEncrypt    !!!
    :param cipher_data:
    :param code:
    :return:
    """
    unquote_data = parse.unquote(cipher_data)
    b64decode_data = base64.b64decode(unquote_data)
    private_key = RSA.import_key(open("private.pem").read(), passphrase=code)

    cipher_rsa = PKCS1_v1_5.new(private_key)

    sentinel = None
    # result = cipher_rsa.decrypt(b64decode_data, sentinel).decode("utf-8")
    result = cipher_rsa.decrypt(b64decode_data, sentinel)
    return result


def encrypt_by_PKCS1_OAEP(plain_text:bytes):
    """
    使用 PKCS1_OAEP加密
    最长86
    :param plain_text: 需要加密的明文
    :return:
    """
    key = RSA.importKey(open('receiver.pem').read())
    cipher = PKCS1_OAEP.new(key)
    cipher_text = cipher.encrypt(plain_text)
    return cipher_text


def decrypt_by_PKS1_OAEP(cipher_text:bytes):
    """
    使用PKCS1_OAEP解密密文
    :param cipher_text: 需要解密的密文
    :return:
    """
    key = RSA.importKey(open('private.pem').read())
    cipher = PKCS1_OAEP.new(key)
    plain_text = cipher.decrypt(cipher_text)
    return plain_text


if __name__ == "__main__":
    data = 'r5JmZPCp44l8Faj9qa5o50mtkomcySISO5Eqi1X66TaY+Ilyn8DwPtDKGeFl3QLjPI48g8mBzRhKQjSCk2CaNSI9jtrFztGi8aQUMm8RRrftfENXLn48Yi9PZNGHxfdmI/n2Ap0kkBic96U1T08ZzWvvkJwWQWLFrAfCptVplvk='

    ret = decrypt_by_PKCS1_v1_5(data)
    print(ret)

    test=bytes('junfenghe'.encode("utf-8"))
    cipher_text = encrypt_by_PKCS1_OAEP(test)
    tmp=str(base64.b64encode(cipher_text),"utf8")
    print("tmp->",tmp)
    print(cipher_text)
    print(len(cipher_text))
    plain_text = decrypt_by_PKS1_OAEP(cipher_text)
    print(plain_text)
    #
    # data="junfenghe"
    # result=encrypt(data)
    # print(str(result))
    # print(type(result))
    # ret=decrypt(str(result))
    # print(ret)
