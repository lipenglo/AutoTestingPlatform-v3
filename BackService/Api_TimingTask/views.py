from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Q

import json
import ast

# Create your db here.
from Api_CaseMaintenance.models import CaseBaseData as db_CaseBaseData
from Api_CaseMaintenance.models import CaseTestSet as db_CaseTestSet
from Api_TimingTask.models import ApiTimingTask as db_ApiTimingTask
from Api_TimingTask.models import ApiTimingTaskTestSet as db_ApiTimingTaskTestSet
from Api_TimingTask.models import ApiTimingTaskHistory as db_ApiTimingTaskHistory
from Api_TimingTask.models import ApiTimingTaskRunLog as db_ApiTimingTaskRunLog
from Api_TestReport.models import ApiTestReport as db_ApiTestReport
from Api_BatchTask.models import ApiBatchTaskTestSet as db_ApiBatchTaskTestSet

# Create reference here.
from ClassData.Logger import Logging
from ClassData.GlobalDecorator import GlobalDer
from ClassData.FindCommonTable import FindTable
from ClassData.Common import Common
from ClassData.ImageProcessing import ImageProcessing
from ClassData.ObjectMaker import object_maker as cls_object_maker
from ClassData.TestReport import ApiReport
from ClassData.TimingTask import TimingTask

from Task.tasks import api_asynchronous_run_task

# Create info here.
cls_Logging = Logging()
cls_GlobalDer = GlobalDer()
cls_FindTable = FindTable()
cls_Common = Common()
cls_ImageProcessing = ImageProcessing()
cls_ApiReport = ApiReport()
cls_TimingTask = TimingTask()


# Create your views here.
@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def select_data(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)

        proId = objData.proId
        taskName = objData.taskName

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_TimingTask', 'select_data', errorMsg)
    else:
        obj_db_ApiTimingTask = db_ApiTimingTask.objects.filter(is_del=0, pid_id=proId).order_by('-updateTime')
        if taskName:
            obj_db_ApiTimingTask = obj_db_ApiTimingTask.filter(taskName__icontains=taskName)
        select_db_ApiTimingTask = obj_db_ApiTimingTask[minSize: maxSize]
        for i in select_db_ApiTimingTask:
            obj_db_ApiTestReport = db_ApiTestReport.objects.filter(
                is_del=0, reportType='TASK', taskId=i.id).order_by('-updateTime')
            if obj_db_ApiTestReport.exists():
                lastReportTime = str(obj_db_ApiTestReport[0].updateTime.strftime('%Y-%m-%d %H:%M:%S'))
                lastReportStatus = obj_db_ApiTestReport[0].reportStatus
            else:
                lastReportTime = ''
                lastReportStatus = ''
            # region 通过率
            obj_db_ApiTestReport = db_ApiTestReport.objects.filter(is_del=0, reportType='TASK', taskId=i.id)
            passTotal = obj_db_ApiTestReport.filter(reportStatus='Pass').count()
            if obj_db_ApiTestReport.count() == 0:
                passRate = 0
            else:
                passRate = round(passTotal / obj_db_ApiTestReport.count() * 100, 2)
            # endregion
            dataList.append({
                'id': i.id,
                'taskName': i.taskName,
                'timingConfig': i.timingConfig,
                'taskSetTotal': db_ApiTimingTaskTestSet.objects.filter(is_del=0, timingTask_id=i.id).count(),
                'remarks': i.remarks,
                'taskStatus': True if i.taskStatus == 1 else False,
                'lastReportTime': lastReportTime,
                'lastReportStatus': lastReportStatus,
                'passRate': passRate,
                'updateTime': str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                "userName": f"{i.uid.userName}({i.uid.nickName})",
                'createUserName': cls_FindTable.get_userName(i.cuid),
            })
        response['TableData'] = dataList
        response['Total'] = obj_db_ApiTimingTask.count()
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def select_case_data(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)

        proId = objData.proId
        pageId = objData.pageId
        funId = objData.funId
        passCaseId = objData.passCaseId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_TimingTask', 'select_case_data', errorMsg)
    else:
        if passCaseId:
            splitCaseId = passCaseId.split(',')
            passCaseIdList = [i for i in splitCaseId]
            # 这里过滤掉已放在用例集中的用例
            obj_db_CaseBaseData = db_CaseBaseData.objects.filter(~Q(id__in=passCaseIdList), is_del=0, pid_id=proId)
        else:
            obj_db_CaseBaseData = db_CaseBaseData.objects.filter(is_del=0, pid_id=proId)
        if pageId:
            obj_db_CaseBaseData = obj_db_CaseBaseData.filter(page_id=pageId)
        if funId:
            obj_db_CaseBaseData = obj_db_CaseBaseData.filter(fun_id=funId)

        for i in obj_db_CaseBaseData:
            # region 通过率
            obj_db_ApiTestReport = db_ApiTestReport.objects.filter(is_del=0, taskId=i.id)
            passTotal = obj_db_ApiTestReport.filter(reportStatus='Pass').count()
            if obj_db_ApiTestReport.count() == 0:
                passRate = 0
            else:
                passRate = round(passTotal / obj_db_ApiTestReport.count() * 100, 2)
            # endregion
            dataList.append({
                'id': i.id,
                'pageName': i.page.pageName,
                'funName': i.fun.funName,
                'caseName': i.caseName,
                'apiTotal':db_CaseTestSet.objects.filter(is_del=0,caseId_id=i.id).count(),
                'caseState': i.caseState,
                'passRate': passRate,
                'testType': i.testType,
                "userName": f"{i.uid.userName}({i.uid.nickName})",
                'updateTime': str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
            })

        response['TableData'] = dataList
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 效验接数据的完成性
def charm_task_data(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(request.body)
        objData = cls_object_maker(responseData)
        charmType = objData.CharmType  # true 新增，false 修改
        basicInfo = objData.BasicInfo
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_TimingTask', 'charm_task_data', errorMsg)
    else:
        # region 验证基本信息
        # region 项目下名称
        obj_db_ApiTimingTask = db_ApiTimingTask.objects.filter(
            is_del=0, pid_id=basicInfo.proId, taskName=basicInfo.taskName
        )
        if obj_db_ApiTimingTask.exists():
            if charmType:
                dataList.append({
                    'stepsName': '基本信息',
                    'errorMsg': '当前所属项目下已有相同定时任务名称,请更改!',
                    'updateTime': cls_Common.get_date_time()})
            else:
                if obj_db_ApiTimingTask.exists():
                    if basicInfo.taskId == obj_db_ApiTimingTask[0].id:
                        pass
                    else:
                        dataList.append({
                            'stepsName': '基本信息',
                            'errorMsg': '当前所属项目下已有相同定时任务名称,请更改!',
                            'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 相同时间
        obj_db_ApiTimingTask = db_ApiTimingTask.objects.filter(is_del=0, timingConfig=basicInfo.timingConfig)
        if obj_db_ApiTimingTask.exists():
            if charmType:
                dataList.append({
                    'stepsName': '基本信息',
                    'errorMsg': '当前所属项目下已有相同定时任务时间配置,请更改!',
                    'updateTime': cls_Common.get_date_time()})
            else:
                if obj_db_ApiTimingTask.exists():
                    if basicInfo.taskId == obj_db_ApiTimingTask[0].id:
                        pass
                    else:
                        dataList.append({
                            'stepsName': '基本信息',
                            'errorMsg': '当前所属项目下已有相同定时任务时间配置,请更改!',
                            'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 时间配置
        try:
            timingConfig = basicInfo.timingConfig.split(' ')
            if len(timingConfig) != 5:
                dataList.append({
                    'stepsName': '基本信息',
                    'errorMsg': '当前时间配置错误:时间格式不满足条件5,例子:* * * * *,请更改!',
                    'updateTime': cls_Common.get_date_time()})
        except BaseException as e:
            dataList.append({
                'stepsName': '基本信息',
                'errorMsg': f'当前时间配置错误:{e},例子:* * * * *,请更改!',
                'updateTime': cls_Common.get_date_time()})
        # endregion
        # endregion
        response['statusCode'] = 2000
        response['TableData'] = dataList
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def save_data(request):
    response = {}
    try:
        responseData = json.loads(request.body)
        objData = cls_object_maker(responseData)
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])  # 当前操作者
        basicInfo = objData.BasicInfo
        testSet = objData.TestSet
        onlyCode = cls_Common.generate_only_code()
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_TimingTask', 'data_save', errorMsg)
    else:
        obj_db_ApiTimingTask = db_ApiTimingTask.objects.filter(
            is_del=0, pid_id=basicInfo.proId, taskName=basicInfo.taskName, timingConfig=basicInfo.timingConfig
        )
        if obj_db_ApiTimingTask.exists():
            response['errorMsg'] = f'当前所属项目下已有相同定时任务名称或配置时间,请更改!'
        else:
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    # region 保存内置定时任务
                    createTask = cls_TimingTask.create_task(
                        basicInfo.taskName, 'Task.tasks.api_daily_run_tasks',
                        {}, basicInfo.timingConfig, basicInfo.taskStatus)
                    # endregion
                    if createTask['state']:
                        # region 添加操作信息
                        cls_Logging.record_operation_info(
                            'API', 'Manual', 3, 'Add',
                            cls_FindTable.get_pro_name(basicInfo.proId),
                            None, None,
                            userId,
                            '【新增定时任务】', CUFront=responseData
                        )
                        # endregion
                        # region 保存基本信息
                        save_db_ApiTimingTask = db_ApiTimingTask.objects.create(
                            pid_id=basicInfo.proId, taskName=basicInfo.taskName, environment_id=basicInfo.environmentId,
                            timingConfig=basicInfo.timingConfig, priority=basicInfo.priorityId,
                            remarks=basicInfo.remarks,
                            pushTo=basicInfo.pushTo, taskStatus=basicInfo.taskStatus, periodicTask_id=createTask['id'],
                            cuid=userId, uid_id=userId, is_del=0, onlyCode=onlyCode
                        )
                        # endregion
                        # region 历史记录
                        restoreData = responseData
                        restoreData['BasicInfo']['updateTime'] = save_db_ApiTimingTask.updateTime.strftime(
                            '%Y-%m-%d %H:%M:%S')
                        restoreData['BasicInfo']['createTime'] = save_db_ApiTimingTask.createTime.strftime(
                            '%Y-%m-%d %H:%M:%S')
                        restoreData['BasicInfo']['uid_id'] = save_db_ApiTimingTask.uid_id
                        restoreData['BasicInfo']['cuid'] = save_db_ApiTimingTask.cuid
                        restoreData['onlyCode'] = onlyCode
                        db_ApiTimingTaskHistory.objects.create(
                            timingTask_id=save_db_ApiTimingTask.id,
                            taskName=basicInfo.taskName,
                            operationType='Add',
                            restoreData=restoreData,
                            onlyCode=onlyCode,
                            uid_id=userId
                        )
                        # endregion
                        # region 测试集
                        product_list_to_insert = list()
                        for item_index, item_testSet in enumerate(testSet, 0):
                            product_list_to_insert.append(db_ApiTimingTaskTestSet(
                                timingTask_id=save_db_ApiTimingTask.id,
                                index=item_index,
                                case_id=item_testSet.id,
                                state=1 if item_testSet.state else 0,
                                uid_id=userId,
                                is_del=0,
                                onlyCode=onlyCode)
                            )
                        db_ApiTimingTaskTestSet.objects.bulk_create(product_list_to_insert)
                        # endregion
                    else:
                        raise ValueError('内置任务创建失败!')
            except BaseException as e:  # 自动回滚，不需要任何操作
                response['errorMsg'] = f'保存失败:{e}'
            else:
                response['statusCode'] = 2001
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def load_task_data(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        taskId = objData.taskId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_TimingTask', 'load_task_data', errorMsg)
    else:
        obj_db_ApiTimingTask = db_ApiTimingTask.objects.filter(is_del=0, id=taskId)
        if obj_db_ApiTimingTask.exists():
            # region 基础信息
            basicInfo = {
                'taskName': obj_db_ApiTimingTask[0].taskName,
                'environmentId': obj_db_ApiTimingTask[0].environment_id,
                'timingConfig': obj_db_ApiTimingTask[0].timingConfig,
                'priorityId': obj_db_ApiTimingTask[0].priority,
                'taskStatus': obj_db_ApiTimingTask[0].taskStatus,
                'pushTo': ast.literal_eval(obj_db_ApiTimingTask[0].pushTo) if obj_db_ApiTimingTask[0].pushTo else [],
                'remarks': obj_db_ApiTimingTask[0].remarks,
            }
            # endregion
            # region 测试集
            testSet = []
            obj_db_ApiTimingTaskTestSet = db_ApiTimingTaskTestSet.objects.filter(
                is_del=0, timingTask_id=taskId).order_by('index')
            for item_testSet in obj_db_ApiTimingTaskTestSet:
                # region 通过率
                obj_db_ApiTestReport = db_ApiTestReport.objects.filter(is_del=0, taskId=item_testSet.case_id)
                passTotal = obj_db_ApiTestReport.filter(reportStatus='Pass').count()
                if obj_db_ApiTestReport.count() == 0:
                    passRate = 0
                else:
                    passRate = round(passTotal / obj_db_ApiTestReport.count() * 100, 2)
                # endregion
                testSet.append({
                    'id': item_testSet.case_id,
                    'testType': item_testSet.case.testType,
                    'caseName': item_testSet.case.caseName,
                    'pageName': item_testSet.case.page.pageName,
                    'funName': item_testSet.case.fun.funName,
                    'caseState': item_testSet.case.caseState,
                    'apiTotal':db_CaseTestSet.objects.filter(is_del=0,caseId_id=item_testSet.case_id).count(),
                    'passRate':f'{passRate}%',
                    'state': True if item_testSet.state == 1 else False
                })
            # endregion
            response['dataTable'] = {
                'basicInfo': basicInfo,
                'testSet': testSet,
            }
            response['statusCode'] = 2000
        else:
            response['errorMsg'] = "当前选择的数据不存在,请刷新后在重新尝试!"
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def edit_data(request):
    response = {}
    try:
        responseData = json.loads(request.body)
        objData = cls_object_maker(responseData)
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])  # 当前操作者
        basicInfo = objData.BasicInfo
        testSet = objData.TestSet
        taskId = basicInfo.taskId
        onlyCode = cls_Common.generate_only_code()  # 生成历史记录唯一码
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_TimingTask', 'edit_data', errorMsg)
    else:
        obj_db_ApiTimingTask = db_ApiTimingTask.objects.filter(is_del=0, id=taskId)
        if obj_db_ApiTimingTask.exists():
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    # region 内置定时任务
                    editTask = cls_TimingTask.edit_task(
                        obj_db_ApiTimingTask[0].periodicTask_id,
                        basicInfo.taskName,
                        basicInfo.timingConfig,
                        basicInfo.taskStatus)
                    # endregion
                    if editTask['state']:
                        # region 添加操作信息
                        # region 查询以前的数据
                        oldTestSet = []
                        obj_db_ApiTimingTaskTestSet = db_ApiTimingTaskTestSet.objects.filter(
                            is_del=0, timingTask_id=taskId).order_by('index')
                        for item_testSet in obj_db_ApiTimingTaskTestSet:
                            oldTestSet.append({
                                'id': item_testSet.case_id,
                                'testType': item_testSet.case.testType,
                                'caseName': item_testSet.case.caseName,
                                'pageName': item_testSet.case.page.pageName,
                                'funName': item_testSet.case.fun.funName,
                                'caseState': item_testSet.case.caseState,
                                'state': True if item_testSet.state == 1 else False
                            })
                        oldData = {
                            'basicInfo': {
                                'id': taskId,
                                'taskName': obj_db_ApiTimingTask[0].taskName,
                                'environmentId': obj_db_ApiTimingTask[0].environment_id,
                                'timingConfig': obj_db_ApiTimingTask[0].timingConfig,
                                'priorityId': obj_db_ApiTimingTask[0].priority,
                                'taskStatus': obj_db_ApiTimingTask[0].taskStatus,
                                'pushTo': ast.literal_eval(obj_db_ApiTimingTask[0].pushTo) if obj_db_ApiTimingTask[
                                    0].pushTo else [],
                                'remarks': obj_db_ApiTimingTask[0].remarks,
                            },
                            'testSet': oldTestSet,
                        }
                        cls_Logging.record_operation_info(
                            'API', 'Manual', 3, 'Edit',
                            cls_FindTable.get_pro_name(basicInfo.proId),
                            None, None,
                            userId,
                            f'【修改定时任务】 ID{taskId}:{obj_db_ApiTimingTask[0].taskName}',
                            CUFront=oldData, CURear=responseData
                        )
                        # endregion
                        # endregion
                        # region 历史记录
                        restoreData = responseData
                        restoreData['BasicInfo']['updateTime'] = obj_db_ApiTimingTask[0].updateTime.strftime(
                            '%Y-%m-%d %H:%M:%S')
                        restoreData['BasicInfo']['createTime'] = obj_db_ApiTimingTask[0].createTime.strftime(
                            '%Y-%m-%d %H:%M:%S')
                        restoreData['BasicInfo']['uid_id'] = obj_db_ApiTimingTask[0].uid_id
                        restoreData['BasicInfo']['cuid'] = obj_db_ApiTimingTask[0].cuid
                        restoreData['onlyCode'] = onlyCode
                        db_ApiTimingTaskHistory.objects.create(
                            timingTask_id=taskId,
                            taskName=basicInfo.taskName,
                            onlyCode=onlyCode,
                            operationType='Edit',
                            restoreData=restoreData,
                            uid_id=userId
                        )
                        # endregion
                        # region 删除测试集数据
                        db_ApiTimingTaskTestSet.objects.filter(
                            is_del=0, timingTask_id=taskId, onlyCode=obj_db_ApiTimingTask[0].onlyCode).update(
                            is_del=1, updateTime=cls_Common.get_date_time(), uid_id=userId
                        )
                        # endregion
                        # region 更新基本信息
                        db_ApiTimingTask.objects.filter(is_del=0, id=taskId).update(
                            pid_id=basicInfo.proId,
                            taskName=basicInfo.taskName, environment_id=basicInfo.environmentId,
                            timingConfig=basicInfo.timingConfig, priority=basicInfo.priorityId,
                            pushTo=basicInfo.pushTo, taskStatus=basicInfo.taskStatus, remarks=basicInfo.remarks,
                            onlyCode=onlyCode, uid_id=userId, updateTime=cls_Common.get_date_time()
                        )
                        # endregion
                        # region 新增测试集数据
                        for item_index, item_testSet in enumerate(testSet, 0):
                            db_ApiTimingTaskTestSet.objects.create(
                                timingTask_id=taskId,
                                index=item_index,
                                case_id=item_testSet.id,
                                state=1 if item_testSet.state else 0,
                                uid_id=userId,
                                is_del=0,
                                onlyCode=onlyCode,
                            )
                        # endregion
                    else:
                        raise ValueError(f'内置定时任务修改失败:{editTask["errorMsg"]}')
            except BaseException as e:  # 自动回滚，不需要任何操作
                response['errorMsg'] = f'保存失败:{e}'
            else:
                response['statusCode'] = 2002
        else:
            response['errorMsg'] = '未找到当前定时任务,请刷新后在重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def delete_data(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        taskId = request.POST['taskId']
        onlyCode = cls_Common.generate_only_code()
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_TimingTask', 'delete_data', errorMsg)
    else:
        obj_db_ApiTimingTask = db_ApiTimingTask.objects.filter(id=taskId, is_del=0)
        if obj_db_ApiTimingTask.exists():
            obj_db_ApiBatchTaskTestSet = db_ApiBatchTaskTestSet.objects.filter(is_del=0, task_id=taskId)
            if obj_db_ApiBatchTaskTestSet.exists():
                batchName = obj_db_ApiBatchTaskTestSet[0].batchTask.batchName
                response['errorMsg'] = f'当前定时任务已被批量任务:{batchName},绑定!请解除绑定后在进行删除操作!'
            else:
                try:
                    with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                        deleteTask = cls_TimingTask.delete_task(obj_db_ApiTimingTask[0].periodicTask_id)
                        if deleteTask['state']:
                            # region 添加历史恢复
                            db_ApiTimingTaskHistory.objects.create(
                                timingTask_id=taskId,
                                taskName=obj_db_ApiTimingTask[0].taskName,
                                operationType='Delete',
                                uid_id=userId,
                            )
                            # endregion
                            # region 添加操作信息
                            cls_Logging.record_operation_info(
                                'API', 'Manual', 3, 'Delete',
                                cls_FindTable.get_pro_name(obj_db_ApiTimingTask[0].pid_id),
                                None, None,
                                userId,
                                f'【删除定时任务】 ID:{taskId}:{obj_db_ApiTimingTask[0].taskName}',
                                CUFront=json.dumps(request.POST)
                            )
                            # endregion
                            # region 删除关联信息
                            db_ApiTimingTaskTestSet.objects.filter(
                                is_del=0, timingTask_id=taskId,onlyCode=obj_db_ApiTimingTask[0].onlyCode).update(
                                is_del=1, updateTime=cls_Common.get_date_time(), uid_id=userId
                            )
                            obj_db_ApiTimingTask.update(
                                is_del=1, updateTime=cls_Common.get_date_time(),
                                periodicTask_id=None, uid_id=userId, onlyCode=onlyCode
                            )
                            # endregion
                        else:
                            raise ValueError(f'内置定时任务删除失败:{deleteTask["errorMsg"]}!')
                except BaseException as e:  # 自动回滚，不需要任何操作
                    response['errorMsg'] = f'数据删除失败:{e}'
                else:
                    response['statusCode'] = 2003
        else:
            response['errorMsg'] = '未找到当前定时任务,请刷新后重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 查询历史恢复
def select_history(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)

        taskId = objData.taskId
        taskName = objData.taskName
        operationType = objData.operationType

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_TimingTask', 'select_history', errorMsg)
    else:
        if taskId:
            obj_db_ApiTimingTaskHistory = db_ApiTimingTaskHistory.objects.filter(
                timingTask_id=taskId).order_by('-createTime')
        else:
            obj_db_ApiTimingTaskHistory = db_ApiTimingTaskHistory.objects.filter().order_by('-createTime')
            if taskName:
                obj_db_ApiTimingTaskHistory = obj_db_ApiTimingTaskHistory.filter(
                    timingTask__taskName__icontains=taskName).order_by('-createTime')
            if operationType:
                obj_db_ApiTimingTaskHistory = obj_db_ApiTimingTaskHistory.filter(
                    operationType=operationType).order_by('-createTime')
        select_db_ApiTimingTaskHistory = obj_db_ApiTimingTaskHistory[minSize: maxSize]
        for i in select_db_ApiTimingTaskHistory:
            if i.restoreData:
                restoreData = json.dumps(ast.literal_eval(i.restoreData),
                                         sort_keys=True, indent=4, separators=(",", ": "), ensure_ascii=False)
            else:
                restoreData = None
            tableItem = [{'restoreData': restoreData}] if restoreData else []
            dataList.append({
                'id': i.id,
                'taskName': i.timingTask.taskName,
                'operationType': i.operationType,
                'tableItem': tableItem,
                'createTime': str(i.createTime.strftime('%Y-%m-%d %H:%M:%S')),
                'userName': f"{i.uid.userName}({i.uid.nickName})",
            })
        response['TableData'] = dataList
        response['Total'] = obj_db_ApiTimingTaskHistory.count()
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 恢复数据 只有管理员组或是项目创建人才可以恢复
def restor_data(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        roleId = cls_FindTable.get_roleId(userId)
        is_admin = cls_FindTable.get_role_is_admin(roleId)
        id = request.POST['id']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_TimingTask', 'restor_data', errorMsg)
    else:
        obj_db_ApiTimingTaskHistory = db_ApiTimingTaskHistory.objects.filter(id=id)
        if obj_db_ApiTimingTaskHistory.exists():
            onlyCode = obj_db_ApiTimingTaskHistory[0].onlyCode  # 当前选择的历史恢复 历史ID
            # 恢复时是管理员或是 当前创建人时才可恢复
            if is_admin or obj_db_ApiTimingTaskHistory[0].timingTask.cuid == userId:
                try:
                    with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                        taskId = obj_db_ApiTimingTaskHistory[0].timingTask_id
                        restoreData = obj_db_ApiTimingTaskHistory[0].restoreData
                        # region 操作记录
                        cls_Logging.record_operation_info(
                            'API', 'Manual', 3, 'Update',
                            cls_FindTable.get_pro_name(obj_db_ApiTimingTaskHistory[0].timingTask.pid_id),
                            None,None,
                            userId,
                            f'【恢复定时任务】 '
                            f'ID:{obj_db_ApiTimingTaskHistory[0].timingTask_id}:'
                            f"{obj_db_ApiTimingTaskHistory[0].taskName}",
                        )
                        # endregion
                        if obj_db_ApiTimingTaskHistory[0].operationType in ["Edit", "Add"]:
                            restoreData = ast.literal_eval(restoreData)
                            obj_db_ApiTimingTask = db_ApiTimingTask.objects.filter(id=taskId)
                            if obj_db_ApiTimingTask.exists():
                                # region 删除原来的测试集数据
                                db_ApiTimingTaskTestSet.objects.filter(
                                    timingTask_id=taskId, onlyCode=obj_db_ApiTimingTask[0].onlyCode).update(
                                    is_del=1, updateTime=cls_Common.get_date_time()
                                )
                                # endregion
                                # region 基本数据
                                obj_db_ApiTimingTask.update(
                                    taskName=restoreData['BasicInfo']['taskName'],
                                    environment_id=restoreData['BasicInfo']['environmentId'],
                                    priority=restoreData['BasicInfo']['priorityId'],
                                    pushTo=restoreData['BasicInfo']['pushTo'],
                                    remarks=restoreData['BasicInfo']['remarks'],
                                    taskStatus=restoreData['BasicInfo']['taskStatus'],
                                    timingConfig=restoreData['BasicInfo']['timingConfig'],
                                    uid_id=restoreData['BasicInfo']['uid_id'],
                                    cuid=restoreData['BasicInfo']['cuid'],
                                    createTime=restoreData['BasicInfo']['createTime'],
                                    updateTime=restoreData['BasicInfo']['updateTime'],
                                    is_del=0,
                                    onlyCode=restoreData['onlyCode'],
                                )
                                # endregion
                                # region 测试集
                                db_ApiTimingTaskTestSet.objects.filter(
                                    timingTask_id=taskId, onlyCode=onlyCode).update(is_del=0)
                                # endregion
                                # region 内置定时任务
                                periodicTaskId = obj_db_ApiTimingTask[0].periodicTask_id
                                if periodicTaskId:  # 更新
                                    editTask = cls_TimingTask.edit_task(
                                        periodicTaskId,
                                        restoreData['BasicInfo']['taskName'],
                                        restoreData['BasicInfo']['timingConfig'],
                                        restoreData['BasicInfo']['taskStatus'])
                                    if editTask['state']:
                                        pass
                                    else:
                                        raise ValueError(f'内置定时任务修改失败:{editTask["errorMsg"]}')
                                else:  # 新增进去
                                    createTask = cls_TimingTask.create_task(
                                        restoreData['BasicInfo']['taskName'], 'Task.tasks.api_daily_run_tasks',
                                        {},
                                        restoreData['BasicInfo']['timingConfig'],
                                        restoreData['BasicInfo']['taskStatus'])
                                    # endregion
                                    if createTask['state']:
                                        obj_db_ApiTimingTask.update(periodicTask_id=createTask['id'])
                                    else:
                                        raise ValueError(f'内置定时新增修改失败:{createTask["errorMsg"]}')

                                # endregion
                            else:
                                raise ValueError('此数据原始数据在库中无法查询到!')
                        else:
                            raise ValueError('使用了未录入的操作类型!')
                except BaseException as e:  # 自动回滚，不需要任何操作
                    response['errorMsg'] = f"数据恢复失败:{e}"
                else:
                    response['statusCode'] = 2002
            else:
                response['errorMsg'] = "您没有权限进行此操作,请联系项目的创建者或是管理员!"
        else:
            response['errorMsg'] = "当前选择的恢复数据不存在,请刷新后重新尝试!"
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 运行
def execute_task(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        taskId = request.POST['taskId']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_TimingTask', 'execute_case', errorMsg)
    else:
        obj_db_ApiTimingTask = db_ApiTimingTask.objects.filter(is_del=0, id=taskId)
        if obj_db_ApiTimingTask.exists():
            queueState = cls_FindTable.get_queue_state('TASK', taskId)
            if queueState:
                response['errorMsg'] = '当前已有相同定时任务在运行,不可重复运行!您可在主页中项目里查看此用例的动态!' \
                                       '如遇错误可取消该项目队列后重新运行!'
            else:
                # region 获取当前定时任务的需要运行多少个接口
                total = 0
                obj_db_ApiTimingTaskTestSet = db_ApiTimingTaskTestSet.objects.filter(is_del=0, timingTask_id=taskId)
                for item_testSet in obj_db_ApiTimingTaskTestSet:
                    if item_testSet.state == 1:
                        total += db_CaseTestSet.objects.filter(is_del=0, caseId_id=item_testSet.case_id,
                                                               state=1).count()
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
                                runType='Manual',
                                testReport_id=testReportId,
                                uid_id=userId
                            )
                            # endregion
                        else:
                            raise ValueError(f'创建主测试报告失败:{createTestReport["errorMsg"]}')
                except BaseException as e:  # 自动回滚，不需要任何操作
                    response['errorMsg'] = f"失败:{e}"
                else:
                    environmentId = obj_db_ApiTimingTask[0].environment_id
                    remindLabel = f"【定时任务:{obj_db_ApiTimingTask[0].taskName}】>"  # 推送的标识
                    result = api_asynchronous_run_task.delay(
                        testReportId, queueId, taskId, remindLabel, environmentId, userId)
                    if result.task_id:
                        response['statusCode'] = 2001
                        response['celeryTaskId'] = result.task_id
        else:
            response['errorMsg'] = '当前选择的定时任务不存在,请刷新后在重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 执行记录
def executive_logging(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)

        taskId = objData.taskId
        taskName = objData.taskName
        runType = objData.runType

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_TimingTask', 'executive_logging', errorMsg)
    else:
        if taskId:
            obj_db_ApiTimingTaskRunLog = db_ApiTimingTaskRunLog.objects.filter(
                timingTask_id=taskId).order_by('-updateTime')
        else:
            obj_db_ApiTimingTaskRunLog = db_ApiTimingTaskRunLog.objects.filter().order_by('-updateTime')
            if taskName:
                obj_db_ApiTimingTaskRunLog = obj_db_ApiTimingTaskRunLog.filter(
                    timingTask__taskName__icontains=taskName).order_by('-updateTime')
            if runType:
                obj_db_ApiTimingTaskRunLog = obj_db_ApiTimingTaskRunLog.filter(runType=runType).order_by('-updateTime')
        select_db_ApiTimingTask = obj_db_ApiTimingTaskRunLog[minSize: maxSize]
        for i in select_db_ApiTimingTask:
            dataList.append({
                'id': i.id,
                'taskName': i.timingTask.taskName,
                'runType': i.runType,
                'updateTime': str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                "userName": f"{i.uid.userName}({i.uid.nickName})",
            })

        response['TableData'] = dataList
        response['Total'] = obj_db_ApiTimingTaskRunLog.count()
        response['statusCode'] = 2000
    return JsonResponse(response)
