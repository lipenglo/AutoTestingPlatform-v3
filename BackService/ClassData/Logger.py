from django.conf import settings
import logging
import json
import datetime
import os

from login.models import ErrorMsg as db_ErrorMsg

# region 配置日志
# 获取日志记录器，配置日志等级
logging.basicConfig(level=logging.INFO)  # 设置日志级别
logger = logging.getLogger(__name__)
logger.propagate = False  # 重复打印解决方法 当logger其中一个子记录器收集了一条消息时，它在层次结构中向后退，导致logger的父节点也记录信息。
# 默认日志格式
formatter = logging.Formatter("%(asctime)s - [%(levelname)s] - %(message)s")
# 输出到控制台的handler
chlr = logging.StreamHandler()
# 配置默认日志格式
chlr.setFormatter(formatter)
# 日志记录器增加此handler
logger.addHandler(chlr)


# endregion

class Logging(object):
    def log(self, func):  # 日志装饰器
        def inner(*args, **kwargs):
            # timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            res = func(*args, **kwargs)
            text = json.loads(res.content)
            method = args[0].method
            path = args[0].path
            if 'HTTP_TOKEN' in args[0].META:
                HTTP_TOKEN = args[0].META['HTTP_TOKEN']
            else:
                HTTP_TOKEN = None
            if 'HTTP_ORIGIN' in args[0].META:
                HTTP_ORIGIN = args[0].META['HTTP_ORIGIN']
            else:
                HTTP_ORIGIN = None
            if 'HTTP_REFERER' in args[0].META:
                HTTP_REFERER = args[0].META['HTTP_REFERER']
            else:
                HTTP_REFERER = None
            if 'HTTP_ACCEPT_LANGUAGE' in args[0].META:
                HTTP_ACCEPT_LANGUAGE = args[0].META['HTTP_ACCEPT_LANGUAGE']
            else:
                HTTP_ACCEPT_LANGUAGE = None
            if method == "GET":
                params = args[0].META['QUERY_STRING']
                logger.info(f"[{func.__name__}]:\n"
                            f"{method} {path}?{params} {args[0].META['SERVER_PROTOCOL']} {res.status_code}\n"
                            f"Host:{args[0].META['HTTP_HOST']}\n"
                            f"Connection:{args[0].META['HTTP_CONNECTION']}\n"
                            f"Accept:{args[0].META['HTTP_CONNECTION']}\n"
                            f"Accept:{args[0].META['HTTP_ACCEPT']}\n"
                            f"User-Agent:{args[0].META['HTTP_USER_AGENT']}\n"
                            f"token:{HTTP_TOKEN}\n"
                            f"Origin:{HTTP_ORIGIN}\n"
                            f"Referer:{HTTP_REFERER}\n"
                            f"Accept-Encoding:{args[0].META['HTTP_ACCEPT_ENCODING']}\n"
                            f"Accept-Language:{HTTP_ACCEPT_LANGUAGE}\n"
                            f"{text}\n"
                            f"----------------------------------------------------------------------\n")
            elif method == "POST":
                dicts = {}
                for i in args[0].POST:
                    dicts[i] = args[0].POST[i]
                params = dicts
                logger.info(f"[{func.__name__}]:\n"
                            f"{method} {path} {args[0].META['SERVER_PROTOCOL']} {res.status_code}\n"
                            f"Host:{args[0].META['HTTP_HOST']}\n"
                            f"Connection:{args[0].META['HTTP_CONNECTION']}\n"
                            f"Accept:{args[0].META['HTTP_CONNECTION']}\n"
                            f"Accept:{args[0].META['HTTP_ACCEPT']}\n"
                            f"User-Agent:{args[0].META['HTTP_USER_AGENT']}\n"
                            f"token:{HTTP_TOKEN}\n"
                            f"Origin:{HTTP_ORIGIN}\n"
                            f"Referer:{HTTP_REFERER}\n"
                            f"Accept-Encoding:{args[0].META['HTTP_ACCEPT_ENCODING']}\n"
                            f"Accept-Language:{HTTP_ACCEPT_LANGUAGE}\n"
                            f"{params}\n"
                            f"{text}\n"
                            f"----------------------------------------------------------------------\n")
            return res
        return inner

    def record_error_info(self,sys,level,methodsName,info):
        """
        :param sys: 所属系统
        :param level: 错误等级，1:主逻辑错误，2:普通错误
        :param methodsName: 方法名称
        :param info:
        :return:
        """
        db_ErrorMsg.objects.create(
            sys=sys,level=level,methodsName=methodsName,info=info,is_read=0
        )

