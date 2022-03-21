from loguru import logger

from info.models import OperateInfo as db_OperateInfo
from info.models import PushInfo as db_PushInfo
from login.models import UserTable as db_UserTable

# import logging
import json
import colorlog


# # region 配置日志
# log_colors_config = {
#     'DEBUG': 'cyan',
#     'INFO': 'white',
#     'ERROR': 'red',
#     'WARNING': 'yellow'
# }
# # 获取日志记录器，配置日志等级
# logging.basicConfig(level=logging.INFO)  # 设置日志级别
# logger = logging.getLogger(__name__)
# logger.propagate = False  # 重复打印解决方法 当logger其中一个子记录器收集了一条消息时，它在层次结构中向后退，导致logger的父节点也记录信息。
# # 默认日志格式
# formatter = colorlog.ColoredFormatter("%(log_color)s [%(asctime)s] %(message)s",
#                                       log_colors=log_colors_config)
# # formatter = logging.Formatter("%(asctime)s - [%(levelname)s] - %(message)s")
# # 输出到控制台的handler
# chlr = logging.StreamHandler()
# # 配置默认日志格式
# chlr.setFormatter(formatter)
# # 日志记录器增加此handler
# logger.addHandler(chlr)
#
#
# # endregion

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
            if 'SERVER_PROTOCOL' in args[0].META:
                SERVER_PROTOCOL = args[0].META['SERVER_PROTOCOL']
            else:
                SERVER_PROTOCOL = ""
            if method == "GET":
                params = args[0].META['QUERY_STRING']
                logger.debug(f"[{func.__name__}]:\n"
                             f"{method} {path}?{params} {SERVER_PROTOCOL} {res.status_code}\n"
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
                logger.debug(f"[{func.__name__}]:\n"
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

    # 错误日志
    def record_error_info(self, sysType, toPage, toFun, info):
        """
        :param sysType: 系统类型
        :param toFun: 所属页面
        :param toPage: 所属功能
        :param level: 错误等级，1:主逻辑错误，2:普通错误
        :param info:
        :return:
        """
        try:
            obj_db_UserTable = db_UserTable.objects.filter(userName="admin")
            db_OperateInfo.objects.create(
                sysType=sysType, level=1, triggerType='System', remindType='Error',
                toPage=toPage, toFun=toFun, info=info, is_read=0,
                uid_id=obj_db_UserTable[0].id
            )
        except BaseException as e:
            self.print_log('error', 'record_error_info', str(e))

    # 添加通用操作信息
    def record_operation_info(self, sysType, triggerType, level, remindType, toPro, toPage, toFun, userId, info,
                              CUFront=None, CURear=None):
        """
        :param triggerType:触发类型:系统(System)/手动(Manual)'
        :param sysType: 系统类型
        :param level: "提醒等级(错误(1),警告(2),新增/修改/删除(3))"
        :param remindType: 提醒(警告/新增/修改/删除/更新/其他)
        :param toPro:
        :param toPage:
        :param toFun:
        :param info:
        :param userId: 创建者
        :param CUFront:
        :param CURear:
        :return:
        """
        try:
            save_db_OperateInfo = db_OperateInfo.objects.create(
                sysType=sysType, triggerType=triggerType, level=level, remindType=remindType,
                toPro=toPro, toPage=toPage, toFun=toFun, info=info, CUFront=CUFront, CURear=CURear, uid_id=userId
            )
        except BaseException as e:
            self.print_log('error', 'record_operation_info', str(e))
            return None
        else:
            return save_db_OperateInfo.id

    # 添加本地的操作信息例：警告
    def record_local_operation_info(self, sysType, triggerType, level, remindType, toPro, toPage, toFun, info):
        """
        :param triggerType:触发类型:系统(System)/手动(Manual)'
        :param sysType: 系统类型
        :param level: "提醒等级(错误(1),警告(2),新增/修改/删除(3))"
        :param remindType: 提醒(警告/新增/修改/删除/其他)
        :param toPro:
        :param toPage:
        :param toFun:
        :param info:
        :return:
        """
        try:
            obj_db_UserTable = db_UserTable.objects.filter(userName="admin")
            save_db_OperateInfo = db_OperateInfo.objects.create(
                sysType=sysType, triggerType=triggerType, level=level, remindType=remindType,
                toPro=toPro, toPage=toPage, toFun=toFun, info=info, uid_id=obj_db_UserTable[0].id
            )
        except BaseException as e:
            self.print_log('error', 'record_local_operation_info', str(e))
            return None
        else:
            return save_db_OperateInfo.id

    # 推送用户
    def push_to_user(self, operationId, pushToUserId):
        try:
            db_PushInfo.objects.create(
                uid_id=pushToUserId,
                oinfo_id=operationId,
                is_read=0,
            )
        except BaseException as e:
            self.print_log('error', 'push_to_user', str(e))

    def print_log(self, logType, methods, msg):  # 打印log信息
        """
        :param logType: info/error
        :param methods: 方法名称
        :param msg: 打印的信息
        :return:
        """
        if logType == "info":
            logger.info(f'[{methods}] [{logType}]: {msg}')
        if logType == "debug":
            logger.debug(f'[{methods}] [{logType}]: {msg}')
        elif logType == "error":
            logger.error(f'[{methods}] [{logType}]: {msg}')
        elif logType == "warning":
            logger.warning(f'[{methods}] [{logType}]: {msg}')
