# Create reference here.
from ClassData.Logger import Logging

import random
import string
import os
import hashlib
import datetime

# Create info here.
cls_Logging = Logging()


class Common(object):
    # 生成随机值
    def generate_random_value(self):
        new_password = ""
        count = 4
        src_digits = string.digits  # string_数字
        src_uppercase = string.ascii_uppercase  # string_大写字母
        src_lowercase = string.ascii_lowercase  # string_小写字母

        for index, item in enumerate(range(count), 1):
            # 随机生成数字、大写字母、小写字母的组成个数（可根据实际需要进行更改）
            digits_num = random.randint(1, 6)
            uppercase_num = random.randint(1, 8 - digits_num - 1)
            lowercase_num = 8 - (digits_num + uppercase_num)

            # 生成字符串
            password = random.sample(src_digits, digits_num) + random.sample(src_uppercase,
                                                                             uppercase_num) + random.sample(
                src_lowercase, lowercase_num)
            # 打乱字符串
            random.shuffle(password)
            # 列表转字符串
            if count - index != 0:
                new_password += ''.join(password) + "-"
            else:
                new_password += ''.join(password)
            # print(new_password)

        return new_password

    # 返回文件MD5值
    def get_file_md5(self,filePath):
        with open(filePath, 'rb') as fp:
            data = fp.read()
        file_md5 = hashlib.md5(data).hexdigest()
        return file_md5

    def get_date_time(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 执行本地命令
    def run_command(self, cmd,isPrint):
        if isPrint:
            cls_Logging.print_log("info", "run_command", cmd)
        temp = os.popen(cmd)
        text = temp.read()
        if text:
            split_text = [i for i in text.split('\n') if i]
            return split_text
        else:
            return None

    # 生成唯一ID Q79r5XWT-409qT276-6V30t124-36Pw0784
    def generate_only_code(self):
        new_password = ""
        count = 4
        src_digits = string.digits  # string_数字
        src_uppercase = string.ascii_uppercase  # string_大写字母
        src_lowercase = string.ascii_lowercase  # string_小写字母

        for index, item in enumerate(range(count), 1):
            # 随机生成数字、大写字母、小写字母的组成个数（可根据实际需要进行更改）
            digits_num = random.randint(1, 6)
            uppercase_num = random.randint(1, 8 - digits_num - 1)
            lowercase_num = 8 - (digits_num + uppercase_num)

            # 生成字符串
            password = random.sample(src_digits, digits_num) + random.sample(src_uppercase,
                                                                             uppercase_num) + random.sample(
                src_lowercase, lowercase_num)
            # 打乱字符串
            random.shuffle(password)
            # 列表转字符串
            if count - index != 0:
                new_password += ''.join(password) + "-"
            else:
                new_password += ''.join(password)
            # print(new_password)

        return new_password

    # 获取过去7天
    def get_seven_days_ago_time(self):
        currentTime = datetime.datetime.now()
        sevenDaysAgo = currentTime + datetime.timedelta(days=-7)
        # dayOfWeek = currentTime.isoweekday()  # 返回数字1-7代表周一到周日
        # # 算出星期1日期
        # dayData = dayOfWeek
        # while True:
        #     if dayOfWeek - dayData == 1:
        #         break
        #     else:
        #         dayData -= 1
        # mondayData = currentTime + datetime.timedelta(days=-dayData)
        #
        # # 算出星期7日期
        # dayData = 0
        # while True:
        #     if dayOfWeek + dayData == 7:
        #         break
        #     else:
        #         dayData += 1
        # sundayData = currentTime + datetime.timedelta(days=dayData)
        # return mondayData, sundayData
        return sevenDaysAgo, currentTime

    # 返回本周的星期一和星期天的日期
    def get_this_weeks_interval_data(self):
        currentTime = datetime.datetime.now()
        dayOfWeek = currentTime.isoweekday()  # 返回数字1-7代表周一到周日
        # 算出星期1日期
        dayData = dayOfWeek
        while True:
            if dayOfWeek - dayData == 1:
                break
            else:
                dayData -= 1
        mondayData = currentTime + datetime.timedelta(days=-dayData)

        # 算出星期7日期
        dayData = 0
        while True:
            if dayOfWeek + dayData == 7:
                break
            else:
                dayData += 1
        sundayData = currentTime + datetime.timedelta(days=dayData)
        return mondayData, sundayData

    # 转换key value 类型的列表字典
    def conversion_kv_to_dict(self,kv):
        dicts = {}
        for item in kv:
            dicts[item['key']] = item['value']
        return dicts

    # 转换字典类型为 key value类型
    def conversion_dict_to_kv(self,dicts):
        dictList = []
        for item in dicts:
            key = item
            value = dicts[item]
            dictList.append({'key': key, 'value': value})
        return dictList