import hashlib
import json
from binascii import a2b_hex, b2a_hex

import requests
from Crypto.Cipher import AES

tokenId = "08daa8d0ba2d42ceac8d6a1d083d15af"
appId = "2bcb35ec8dff46868cd8b82857f9c014"


class Tianchuang(object):
    def __init__(self, name, idcard, mobile):
        self.TCApplyNeedleUrl = "http://api.tcredit.com/assessment/radar"
        self.TCCreditNeedleUrl = "http://api.tcredit.com/integration/creditProbe01"
        self.TCWJNeedleUrl = "http://api.tcredit.com/assessment/infernalProbe"
        self.name = name
        self.idcard = idcard
        self.mobile = mobile

    def SQTZ(self):
        json1 = json.dumps({'name': self.name, 'idcard': self.idcard, 'mobile': self.mobile})
        param = str(AESCipher.encrypt(json1, tokenId.replace('-', '')), encoding="utf-8")
        parameter = ("param=%s" % (param))
        ANparams = {'tokenKey': TokenKey.getTokenKey(parameter, self.TCApplyNeedleUrl), 'appId': appId, 'param': param}
        print(ANparams)
        r3 = requests.post(self.TCApplyNeedleUrl, ANparams)
        print(r3.text)
        rep = json.loads(r3.text)
        if rep["status"] == 0:
            data = rep["data"]
            TCdata2 = AESCipher.decode_data(data, tokenId.replace('-', ''))
            print("TCdata2解密后", TCdata2)

    def WJTZ(self):
        json1 = json.dumps({'name': self.name, 'idcard': self.idcard, 'mobile': self.mobile})
        param = str(AESCipher.encrypt(json1, tokenId.replace('-', '')), encoding="utf-8")
        parameter = ("param=%s" % (param))
        WJTZparams = {'tokenKey': TokenKey.getTokenKey(parameter, self.TCWJNeedleUrl), 'appId': appId, 'param': param}
        r2 = requests.post(self.TCWJNeedleUrl, WJTZparams)
        print(r2.text)
        rep = json.loads(r2.text)
        if rep["status"] == 0:
            data = rep["data"]
            TCdata1 = AESCipher.decode_data(data, tokenId.replace('-', ''))
            print("TCdata1解密后", TCdata1)

    def XYTZ(self):

        json1 = json.dumps({'name': self.name, 'idcard': self.idcard, 'mobile': self.mobile})
        parameterXY = ("name=%s,idCard=%s,mobile=%s" % (self.name, self.idcard, self.mobile))

        XYTZparams = {'tokenKey': TokenKey.getTokenKey(parameterXY, self.TCCreditNeedleUrl), 'appId': appId, 'name': self.name,
                      'idCard': self.idcard,
                      'mobile': self.mobile}
        r1 = requests.post(self.TCCreditNeedleUrl, XYTZparams)
        TCdata = r1.text
        print(TCdata)
# param = str(AESCipher.encrypt(json1, tokenId.replace('-', '')), encoding="utf-8")
# parameter = ("param=%s" % (param))
# parameterXY = ("name=%s,idCard=%s,mobile=%s" % (name, idcard, mobile))
# XYTZparams = {'tokenKey': TokenKey.getTokenKey(parameterXY, TCCreditNeedleUrl), 'appId': appId, 'name': name,
#               'idCard': idcard,
#               'mobile': mobile}
# WJTZparams = {'tokenKey': TokenKey.getTokenKey(parameter, TCWJNeedleUrl), 'appId': appId, 'param': param}
# ANparams = {'tokenKey': TokenKey.getTokenKey(parameter, TCApplyNeedleUrl), 'appId': appId, 'param': param}
# r1 = requests.post(TCCreditNeedleUrl, XYTZparams)
# TCdata = r1.text
# print(TCdata)


class AESCipher:
    # 加密
    def encrypt(text, key):
        cryptor = AES.new(a2b_hex(key), AES.MODE_ECB)
        x = AES.block_size - (len(text.encode('utf-8')) % AES.block_size)
        if x != 0:
            text = text + chr(x) * x
            t = text.encode('utf-8')
        ciphertext = cryptor.encrypt(t)
        return b2a_hex(ciphertext)

    def decode_data(data, key):
        cryptor = AES.new(a2b_hex(key), AES.MODE_ECB)
        msg = cryptor.decrypt(a2b_hex(data))
        # print(msg)
        # print(len(msg))
        # print(msg[len(msg)-1])
        paddingLen = msg[len(msg) - 1]
        return msg[0:-paddingLen].decode('utf-8')


class TokenKey:
    # 获取tokenKey
    def getTokenKey(parameter, url):
        spkey = parameter.split(',')
        spkey.sort()
        delimiter = ','
        joinkey = delimiter.join(spkey)
        print(joinkey)
        md5 = hashlib.md5()
        md5.update((url + tokenId + joinkey).encode('utf-8'))
        tokenkey = md5.hexdigest()
        return tokenkey


# r2 = requests.post(TCWJNeedleUrl, WJTZparams)
# print(r2.text)
# rep = json.loads(r2.text)
# if rep["status"] == 0:
#     data = rep["data"]
#     TCdata1 = AESCipher.decode_data(data, tokenId.replace('-', ''))
#     print("TCdata1解密后", TCdata1)
#
# r3 = requests.post(TCApplyNeedleUrl, ANparams)
# print(r3.text)
# rep = json.loads(r3.text)
# if rep["status"] == 0:
#     data = rep["data"]
#     TCdata2 = AESCipher.decode_data(data, tokenId.replace('-', ''))
#     print("TCdata2解密后", TCdata2)
#
#     return json.dumps(TCdata2)
if __name__ == '__main__':
    Tianchuang('林纪鹏', '370612198210122515', '15853545400').WJTZ()
