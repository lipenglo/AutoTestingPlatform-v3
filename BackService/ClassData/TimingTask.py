from functools import wraps

import json
import datetime
import croniter

# select db here
from djcelery import models as celery_models


# Create reference here.


# Create init here.

class TimingTask(object):
    # 创建内置定时任务
    def create_task(self, taskName, task, taskArgs, crontabTime, taskStatus):
        """
        name # 任务名字
        task # 执行的任务 "myapp.tasks.add"
        task_args # 任务参数 {"x":1, "Y":1}
        is_disable #是否启用 True False

        crontab_time # 定时任务时间 格式：
        {
            'month_of_year': 9 # 月份
            'day_of_month': 5 # 日期
            'day_of_week': '1' # 周
            'hour': 01 # 小时
            'minute':05 # 分钟
        }
        """
        # task任务， created是否定时创建
        results = {}
        try:
            task, created = celery_models.PeriodicTask.objects.get_or_create(name=taskName, task=task, enabled=0)
            # 转换crontabtime
            temp_Timingconfig = crontabTime.split(' ')
            minute = temp_Timingconfig[0]
            hour = temp_Timingconfig[1]
            day_of_week = temp_Timingconfig[2]
            day_of_month = temp_Timingconfig[3]
            month_of_year = temp_Timingconfig[4]
            crontabTime = {'month_of_year': month_of_year,  # 月份
                           'day_of_month': day_of_month,  # 日期
                           'day_of_week': day_of_week,  # 周
                           'hour': hour,  # 小时
                           'minute': minute,  # 分钟
                           }
            # 如果没有就创建，有的话就继续复用之前的crontab
            crontab = celery_models.CrontabSchedule.objects.create(**crontabTime)
            task.crontab = crontab  # 设置crontab
            task.enabled = taskStatus  # 开启task
            task.kwargs = json.dumps(taskArgs)  # 传入task参数
            task.save()
        except BaseException as e:
            results['state'] = False
            results['errorMsg'] = e
        else:
            results['id'] = task.id
            results['state'] = True
        return results

    # 编辑定时任务
    def edit_task(self, periodicTaskId, taskName, crontabtime, taskStatus):
        results = {}
        try:
            temp_Timingconfig = crontabtime.split(' ')
            minute = temp_Timingconfig[0]
            hour = temp_Timingconfig[1]
            day_of_week = temp_Timingconfig[2]
            day_of_month = temp_Timingconfig[3]
            month_of_year = temp_Timingconfig[4]
            obj_PeriodicTask = celery_models.PeriodicTask.objects.filter(id=periodicTaskId)
            if obj_PeriodicTask:
                # 修改定时任务表的名称
                obj_PeriodicTask.update(name=taskName)
                # 修改定时任务的时间
                crontabid = obj_PeriodicTask[0].crontab_id
                celery_models.CrontabSchedule.objects.filter(id=crontabid).update(
                    minute=minute,
                    hour=hour,
                    day_of_week=day_of_week,
                    day_of_month=day_of_month,
                    month_of_year=month_of_year
                )
                statis = True if taskStatus else False
                disable_task = self.disable_task(periodicTaskId, statis)
                if disable_task['state']:
                    pass
                else:
                    results['state'] = False
                    results['errorMsg'] = f"修改内置定时任务失败:{disable_task['errorMsg']}"
                    return results
        except BaseException as e:
            results['state'] = False
            results['errorMsg'] = f"修改内置定时任务失败:{e}"
        else:
            results['state'] = True
        return results

    # 删除定时任务
    def delete_task(self, periodicTaskId):
        results = {}
        try:
            task = celery_models.PeriodicTask.objects.filter(id=periodicTaskId)
            if task:
                crontabid = task[0].crontab_id
                task.delete()
                celery_models.CrontabSchedule.objects.filter(id=crontabid).delete()
                results['state'] = True
            else:
                results['state'] = True
        except BaseException as e:
            results['state'] = False
            results['errorMsg'] = e
        return results

    # 关闭或开启任务 定时任务开启和关闭必须通过这种方式来调用，不然会出现不运行的问题
    def disable_task(self, periodicTaskId, is_disable):
        results = {}
        try:
            task = celery_models.PeriodicTask.objects.get(id=periodicTaskId)
            task.enabled = is_disable  # 设置关闭
            task.save()
            results['state'] = True
        except BaseException as e:
            results['state'] = False
            results['errorMsg'] = f"修改内置定时任务失败:{e}"
        return results

    # 计算定时任务下次运行时间
    def crontab_next_run_time(self, crontabTime, timeFormat="%Y-%m-%d %H:%M", queryTimes=1):
        """计算定时任务下次运行时间
        sched str: 定时任务时间表达式
        timeFormat str: 格式为"%Y-%m-%d %H:%M"
        queryTimes int: 查询下次运行次数
        get_next 明天
        get_prev 当天
        """
        results = {}
        now = datetime.datetime.now()
        try:
            # 以当前时间为基准开始计算
            cron = croniter.croniter(crontabTime, now)
            for i in range(queryTimes):
                get_prev = cron.get_prev(datetime.datetime).strftime(timeFormat)
                results['time'] = get_prev
                break
            else:
                results['state'] = False
        except BaseException as e:
            results['state'] = False
            results['errorMsg'] = f"时间转换失败:{e}"
        else:
            results['state'] = True
        return results
