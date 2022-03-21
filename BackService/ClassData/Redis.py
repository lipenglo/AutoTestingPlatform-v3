import json
import ast

from django_redis import get_redis_connection
from ClassData.Logger import Logging as cls_Logging


class RedisHandle(cls_Logging):
    def witer_type_dict(self, label, key, value, timeOut=None):
        """
        :param label: '标记':{'k':'v','k':v}
        :param key:
        :param value:
        :param timeOut:为空时永久保存
        :return: True or False
        """
        try:
            conn = get_redis_connection("default")  # 连接
            conn.hset(label, key, value)
            if timeOut:
                conn.expire(label, timeOut)  # expire函数设置过期时间为秒
        except BaseException as e:
            cls_Logging.print_log(self,'error','Redis>witer_type_dict',e)
            cls_Logging.record_error_info(self,'ALL', 'ClassData', 'Redis>witer_type_dict', e)
            return False
        else:
            return True

    def find_type_dict(self, label, key):
        conn = get_redis_connection("default")
        exists = conn.hget(label,key)  # 若 label 存在，返回 1 ，否则返回 0
        if exists:
            pass
        else:
            return None

    def witer_type_list(self, label,dictData, timeOut=300):
        """
        :param label: '标记':[{'k':'v','k':v}]
        :param dictData:
        :param timeOut:为空时永久保存
        :return: True or False
        """
        try:
            conn = get_redis_connection("default")  # 连接
            conn.rpush(label,json.dumps(dictData))
            if timeOut:
                conn.expire(label, timeOut)  # expire函数设置过期时间为秒
        except BaseException as e:
            cls_Logging.print_log(self,'error','Redis>witer_type_listdict',e)
            cls_Logging.record_error_info(self,'ALL', 'ClassData', 'Redis>witer_type_listdict', e)
            return False
        else:
            return True

    def read_type_list(self,label):
        try:
            rowData = None
            conn = get_redis_connection("default")
            exists = conn.exists(label)  # 若 key 存在，返回 1 ，否则返回 0
            if exists:
                readData = conn.blpop(label)  # 从头开始读1个删除1个， 如果列表为空,就会删除此Key
                if len(readData) == 2:
                    rowData = readData[1].decode("UTF-8")
                    rowData = ast.literal_eval(rowData.replace('true','True').replace('false','False'))

        except BaseException as e:
            cls_Logging.print_log(self, 'error', 'Redis>read_type_list', e)
            cls_Logging.record_error_info(self, 'ALL', 'ClassData', 'Redis>read_type_list', e)
            return False
        else:
            return rowData


