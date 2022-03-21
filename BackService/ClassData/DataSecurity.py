# 数据安全性
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
from django.conf import settings

# Create reference here.
from ClassData.Logger import Logging as cls_Logging
from ClassData.Common import Common as cls_Common


# Create info here.
class DataSecurity(cls_Logging, cls_Common):
    def pad(self, text):
        while len(text) % 16 != 0:
            text += ' '
        return text

    # 加密秘钥需要长达16位字符，所以进行空格拼接
    def pad_key(self, key):
        while len(key) % 16 != 0:
            key += ' '
        return key

    # 加密
    def aes_encrypt(self, text):
        """ 加密
        :param text: 需要加密的信息
        :return:
        """
        aes = AES.new(self.pad_key(settings.SECRET_KEY).encode(), AES.MODE_ECB)
        encrypted_text = aes.encrypt(self.pad(text).encode())
        encrypted_text_hex = b2a_hex(encrypted_text)
        return encrypted_text_hex

    # 解密
    def aes_decode(self, textHex):
        """ 解密
        :param textHex: 被加密的信息
        :return:
        """
        aes = AES.new(self.pad_key(settings.SECRET_KEY).encode(), AES.MODE_ECB)
        # #此处是为了验证是否能将字节转为字符串后，进行解密成功
        # #实际上a 就是 encrypted_text ，也就是加密后的内容
        # #用aes对象进行解密，将字节类型转为str类型，错误编码忽略不计
        de = str(aes.decrypt(a2b_hex(textHex)), encoding='utf-8', errors="ignore")
        # #获取str从0开始到文本内容的字符串长度。
        # print(de[:len(text)])
        return de.replace(' ', '')
