
import base64
import json
import requests
import rsa
from Crypto.Hash import SHA, SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

#提取出来的公钥证书
key = """MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDCDpkY7ihHKAKBx+QTJ0f+WftG
pZTeLE6J1nTM2WJQ4poEbVeV2LMlT2fDJD7Y0dwU9aTnljpYoEN9V1aEzMqzfCT2
Y2A5argvRHpy5lqa26ja3DDO1AoTmHoDuRhsz1Wbp8Br7i3X9I3Ku2A7U3BUhbvH
x3FtNG5XlaDOLTMgUQIDAQAB"""



def handle_pub_key(key):
    """
    处理公钥
    公钥格式pem，处理成以-----BEGIN PUBLIC KEY-----开头，-----END PUBLIC KEY-----结尾的格式
    :param key:pem格式的公钥，无-----BEGIN PUBLIC KEY-----开头，-----END PUBLIC KEY-----结尾
    :return:
    """
    start = '-----BEGIN PUBLIC KEY-----\n'
    end = '-----END PUBLIC KEY-----'
    result = ''
    # 分割key，每64位长度换一行
    divide = int(len(key) / 64)
    divide = divide if (divide > 0) else divide+1
    line = divide if (len(key) % 64 == 0) else divide+1
    for i in range(line):
        result += key[i*64:(i+1)*64] + '\n'
    result = start + result + end
    return result

def encrypt(key, content):
    """
    ras 加密[公钥加密]
    :param key: 无BEGIN PUBLIC KEY头END PUBLIC KEY尾的pem格式key
    :param content:待加密内容
    :return:
    """
    pub_key = handle_pub_key(key)
    pub = RSA.import_key(pub_key)
    cipher = PKCS1_v1_5.new(pub)
    encrypt_bytes = cipher.encrypt(content.encode(encoding='utf-8'))
    result = base64.b64encode(encrypt_bytes)
    result = str(result, encoding='utf-8')
    print(result)
    return result


content = "HH"
encrypt(key, content)