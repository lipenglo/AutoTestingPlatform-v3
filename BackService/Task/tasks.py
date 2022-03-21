from celery import shared_task
from django.db import transaction

import json
import ast
import datetime

# Create your db here.
from Api_TimingTask.models import ApiTimingTask as db_ApiTimingTask
from Api_TimingTask.models import ApiTimingTaskTestSet as db_ApiTimingTaskTestSet
from Api_CaseMaintenance.models import CaseTestSet as db_CaseTestSet
from Api_TimingTask.models import ApiTimingTaskRunLog as db_ApiTimingTaskRunLog
from Api_BatchTask.models import ApiBatchTask as db_ApiBatchTask

# Create reference here.
from ClassData.Logger import Logging
from ClassData.GlobalDecorator import GlobalDer
from ClassData.FindCommonTable import FindTable
from ClassData.Common import Common
from ClassData.ImageProcessing import ImageProcessing
from ClassData.Request import RequstOperation
from ClassData.TestReport import ApiReport
from ClassData.TimingTask import TimingTask
from ClassData.EmailOperation import Email

# Create info here.
cls_Logging = Logging()
cls_GlobalDer = GlobalDer()
cls_FindTable = FindTable()
cls_Common = Common()
cls_ImageProcessing = ImageProcessing()
cls_RequstOperation = RequstOperation()
cls_ApiReport = ApiReport()
cls_TimingTask = TimingTask()
cls_Email = Email()


@shared_task  # 异步任务-测试用例运行
def api_asynchronous_run_case(remindLabel, redisKey, testReportId, queueId, caseId, environmentId, userId):
    """
    :param remindLabel: 推送的标识,用于操作信息中提取失败时提示使用
    :param redisKey:
    :param testReportId:
    :param queueId:
    :param caseId:
    :param environmentId:
    :param userId:
    :return:
    """
    cls_ApiReport.update_queue(queueId, 1, userId)  # 更新队列-执行中
    # 组合成Case执行的用例
    executeCase = cls_RequstOperation.execute_case(remindLabel, redisKey, testReportId, caseId, environmentId, userId)
    cls_ApiReport.update_queue(queueId, 2, userId)  # 更新队列-完成
    if executeCase['state']:
        return "int_asynchronous_run_case-测试用例运行完成"
    else:
        return f"int_asynchronous_run_case-测试用例运行失败:{executeCase['errorMsg']}"


@shared_task  # 异步任务-定时任务运行
def api_asynchronous_run_task(testReportId, queueId, taskId, label, environmentId, userId):
    cls_ApiReport.update_queue(queueId, 1, userId)  # 更新队列-执行中
    executeTask = cls_RequstOperation.excute_task(testReportId, taskId, label, environmentId, userId)
    cls_ApiReport.update_queue(queueId, 2, userId)  # 更新队列-完成
    # region 发送邮件信息
    obj_db_ApiTimingTask = db_ApiTimingTask.objects.filter(id=taskId)
    if obj_db_ApiTimingTask.exists():
        pushTo = obj_db_ApiTimingTask[0].pushTo
        if pushTo:
            getReportTopData = cls_ApiReport.get_report_top_data(testReportId)
            userList = [item_userId for item_roleId,item_userId in ast.literal_eval(pushTo)]
            userEmailList = cls_FindTable.user_email_list(userList)
            emailReport = cls_Email.email_report(getReportTopData['topData'])
            cls_Email.send_email(userEmailList,emailReport[0],emailReport[1])
        else:
            pass
    # endregion
    if executeTask['state']:
        return "int_asynchronous_run_case-定时任务运行完成"
    else:
        return f"int_asynchronous_run_case-定时任务运行失败:{executeTask['errorMsg']}"


@shared_task  # 异步任务-批量任务运行
def api_asynchronous_run_batch(testReportId, queueId, batchId, label, userId):
    cls_ApiReport.update_queue(queueId, 1, userId)  # 更新队列-执行中
    executeBatch = cls_RequstOperation.excute_batch(testReportId, batchId, label, userId)
    cls_ApiReport.update_queue(queueId, 2, userId)  # 更新队列-完成
    # region 发送邮件信息
    obj_db_ApiBatchTask = db_ApiBatchTask.objects.filter(id=batchId)
    if obj_db_ApiBatchTask.exists():
        pushTo = obj_db_ApiBatchTask[0].pushTo
        if pushTo:
            getReportTopData = cls_ApiReport.get_report_top_data(testReportId)
            userList = [item_userId for item_roleId, item_userId in ast.literal_eval(pushTo)]
            userEmailList = cls_FindTable.user_email_list(userList)
            emailReport = cls_Email.email_report(getReportTopData['topData'])
            cls_Email.send_email(userEmailList, emailReport[0], emailReport[1])
        else:
            pass
    # endregion
    if executeBatch['state']:
        return "int_asynchronous_run_case-批量任务运行完成"
    else:
        return f"int_asynchronous_run_case-批量任务运行失败:{executeBatch['errorMsg']}"


@shared_task  # 定时任务设置好后 自动到时间运行
def api_daily_run_tasks():
    results = {
        'itemResults': []
    }
    obj_db_ApiTimingTask = db_ApiTimingTask.objects.filter(is_del=0)
    performList = [(i.id, i.timingConfig) for i in obj_db_ApiTimingTask]  # 执行列表
    for item_task in performList:
        itemResults = {}
        taskId, timingConfig = item_task
        crontabNextRunTime = cls_TimingTask.crontab_next_run_time(timingConfig)  # 计算定时任务下次运行时间
        if crontabNextRunTime['state']:
            obj_db_ApiTimingTaskTestSet = db_ApiTimingTaskTestSet.objects.filter(
                is_del=0, timingTask_id=taskId).order_by('index')
            currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')  # 当前时间
            # 时间相等且测试集不是0时运行
            if crontabNextRunTime['time'] == currentTime and obj_db_ApiTimingTaskTestSet.count() != 0:
                # region 运行定时任务
                itemResults['taskId'] = taskId
                itemResults['timingConfig'] = timingConfig

                obj_db_ApiTimingTask = db_ApiTimingTask.objects.filter(is_del=0, id=taskId)
                if obj_db_ApiTimingTask.exists():
                    userId = obj_db_ApiTimingTask[0].uid_id
                    queueState = cls_FindTable.get_queue_state('TASK', taskId)
                    if queueState:
                        errorMsg = '当前已有相同定时任务在运行,不可重复运行!您可在主页中项目里查看此用例的动态!' \
                                   '如遇错误可取消该项目队列后重新运行!'
                        itemResults['errorMsg'] = errorMsg
                        cls_Logging.print_log('warning', 'api_daily_run_tasks', errorMsg)

                    else:
                        # region 获取当前定时任务的需要运行多少个接口
                        total = 0
                        obj_db_ApiTimingTaskTestSet = db_ApiTimingTaskTestSet.objects.filter(
                            is_del=0, timingTask_id=taskId)
                        for item_testSet in obj_db_ApiTimingTaskTestSet:
                            if item_testSet.state == 1:
                                total += db_CaseTestSet.objects.filter(
                                    is_del=0, caseId_id=item_testSet.case_id, state=1).count()
                        # endregion
                        try:
                            with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                                # region 创建1级主报告
                                createTestReport = cls_ApiReport.create_test_report(
                                    obj_db_ApiTimingTask[0].pid_id,
                                    obj_db_ApiTimingTask[0].taskName,
                                    'TASK', taskId, total, userId
                                )
                                # endregion
                                if createTestReport['state']:
                                    testReportId = createTestReport['testReportId']
                                    # region 创建队列
                                    queueId = cls_ApiReport.create_queue(
                                        obj_db_ApiTimingTask[0].pid_id, None, None,
                                        'TASK', taskId, testReportId, userId)  # 创建队列
                                    # endregion
                                    # region 运行记录
                                    db_ApiTimingTaskRunLog.objects.create(
                                        timingTask_id=taskId,
                                        runType='Auto',
                                        testReport_id=testReportId,
                                        uid_id=userId
                                    )
                                    # endregion
                                else:
                                    raise ValueError(f'创建主测试报告失败:{createTestReport["errorMsg"]}')
                        except BaseException as e:  # 自动回滚，不需要任何操作
                            errorMsg = f"运行失败:{e}"
                            itemResults['errorMsg'] = errorMsg
                            cls_Logging.print_log('error', 'api_daily_run_tasks', errorMsg)
                            cls_Logging.print_log('error', 'api_daily_run_tasks', errorMsg)
                            cls_Logging.record_error_info(
                                'API', 'ClassData>TimingTask', 'api_daily_run_tasks', errorMsg)
                        else:
                            environmentId = obj_db_ApiTimingTask[0].environment_id
                            remindLabel = f"【定时任务:{obj_db_ApiTimingTask[0].taskName}】>"  # 推送的标识
                            result = api_asynchronous_run_task.delay(testReportId, queueId, taskId, remindLabel,
                                                                     environmentId, userId)
                            itemResults['celeryTaskId'] = result.task_id
                else:
                    errorMsg = f'ID:{taskId},当前定时任务不存在,请刷新后在重新尝试!'
                    itemResults['errorMsg'] = errorMsg
                    cls_Logging.print_log('warning', 'api_daily_run_tasks', errorMsg)
                # endregion
            else:
                pass
        else:
            errorMsg = f"当前定时任务:{taskId},{crontabNextRunTime['errorMsg']}!"
            itemResults['errorMsg'] = errorMsg
            cls_Logging.print_log('error', 'api_daily_run_tasks', errorMsg)
            cls_Logging.record_error_info('API', 'ClassData>TimingTask', 'api_daily_run_tasks', errorMsg)
        results['itemResults'].append(itemResults)
    return results
