# from PIL import Image
# from io import BytesIO

import base64
# import io
# import cv2
# import numpy as np


from ClassData.Logger import Logging as cls_Logging

# 图片转换
class ImageProcessing(cls_Logging):
    def img_to_base64(self, imgPath):
        try:
            with open(imgPath, "rb") as f:  # 转为二进制格式
                base64_data = base64.b64encode(f.read())  # 使用base64进行加密
                # str(base64_data, encoding="utf-8")
                return base64_data
        except BaseException as e:
            cls_Logging.print_log(self, 'error', 'img_to_base64', e)
            return None

    def base64_to_img(self, bytesData, savePath):
        results = {}
        try:
            with open(savePath, 'wb') as f:
                imgBase64 = base64.b64decode(bytesData)  # 传过来的base64也要这在里转换一下,一定要去掉data:image/png:base64,
                f.write(imgBase64)
                results['state'] = True
        except BaseException as e:
            cls_Logging.print_log(self, 'error', 'base64_to_img', e)
            results['state'] = False
            results['errorMsg'] = str(e)
        return results
