import base64
import M2Crypto

import datetime
import hashlib
import json
import base64

import requests


class RsaUtil(object):
    private_key = M2Crypto.RSA.load_key('third_party/key1/8000013189_pri.pem')
    print(private_key)

    @staticmethod
    def encrypt(digest, private_key):
        digest = base64.b64encode(digest.encode('utf-8'))
        result = ""
        while (len(digest) > 117):
            some = digest[0:117]
            digest = digest[117:]
            result += private_key.private_encrypt(some, M2Crypto.RSA.pkcs1_padding).hex()
        result += private_key.private_encrypt(digest, M2Crypto.RSA.pkcs1_padding).hex()

        return result


class Xinyan(object):
    def __init__(self):
        self.member_id = '8000013189'
        self.terminal_id = '8000013189'
    def xinyan(self, orderNo, name, idcard):
        data_content = self.xinyanParam(orderNo, name, idcard)
        print(data_content)
        param = {
            'member_id': self.member_id,
            'terminal_id': self.terminal_id,
            "data_type": "json",
            'data_content': data_content
        }
        print(param)
        # param1 = json.dumps(param)
        s = requests.session()
        #测试url
        resp = s.post('https://test.xinyan.com/product/credit/v1/unify', data=param)
        print(resp.text)

    def xinyanParam(self, orderNo, name, idcard):
        _data = {
            'member_id': '8000013189',
            'terminal_id': '8000013189',
            'trade_date': datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
            'trans_id': orderNo + datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
            'industry_type': 'B18',
            'id_no': self.generateMD5(idcard),
            'id_name': self.generateMD5(name),
            'product_type': 'QJLDLEZ',
            'versions': '1.4.0',
        }
        data_content = json.dumps(_data)
        rsaUtil = RsaUtil()
        cc = rsaUtil.encrypt(data_content, RsaUtil.private_key)
        print(cc)
        return cc

    def generateMD5(self, str):
        hl = hashlib.md5()
        hl.update(str.encode(encoding='utf-8'))
        return hl.hexdigest()


if __name__ == '__main__':
    Xinyan().xinyan("123", "刘世超", '330523199105012318')
