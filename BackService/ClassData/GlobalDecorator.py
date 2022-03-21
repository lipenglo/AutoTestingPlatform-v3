from functools import wraps
from rest_framework.authtoken.models import Token as db_Token

import json


# 全局装饰器
class GlobalDer(object):
    # def user_state(self, func):
    #     @wraps(func)
    #     def isToken(*args, **kwargs):
    #         a = func(*args, **kwargs)
    #         content = {}
    #         try:
    #             obj_db_Token = db_Token.objects.filter(key=args[0].META['HTTP_TOKEN'])  # 从请求中获取数据，查询token
    #             # content = json.loads(a.content)
    #             # a.content = json.dumps(content)
    #         except BaseException as e:
    #             content['errorMsg'] = "Request Hearders Not TOKEN"
    #             a.status_code = 500
    #         else:
    #             pass
    #         return a
    #
    #     return isToken

    # Token是否为空/Token是否是库中相匹配的 所有接口都必须调用 此装饰器
    def foo_isToken(self, func):
        @wraps(func)
        def isToken(*args, **kwargs):
            a = func(*args, **kwargs)
            content = {}
            try:
                token = db_Token.objects.filter(key=args[0].META['HTTP_TOKEN'])  # 从请求中获取数据，查询token
                # content = json.loads(a.content)
                # a.content = json.dumps(content)
            except BaseException as e:
                content['errorMsg'] = "Request Hearders Not TOKEN"
                a.status_code = 500
            else:
                if token.exists():
                    content = json.loads(a.content)
                    # Token正常时带入正确code
                    content['code'] = 1001
                else:
                    # 查询不到token或是为空时就不让访问
                    content['code'] = 1000
                    content['errorMsg'] = "Request Hearders TOKEN Error"
            a.content = json.dumps(content)
            return a
        return isToken