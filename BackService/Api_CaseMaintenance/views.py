from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction
from dwebsocket.decorators import accept_websocket
from django.db.models import Q
from time import sleep
from django.conf import settings

import json
import ast

# Create your db here.
from ProjectManagement.models import ProManagement as db_ProManagement
from PageManagement.models import PageManagement as db_PageManagement
from FunManagement.models import FunManagement as db_FunManagement
from Api_IntMaintenance.models import ApiBaseData as db_ApiBaseData
from Api_IntMaintenance.models import ApiHeaders as db_ApiHeaders
from Api_IntMaintenance.models import ApiParams as db_ApiParams
from Api_IntMaintenance.models import ApiBody as db_ApiBody
from Api_IntMaintenance.models import ApiDynamic as db_ApiDynamic

from Api_CaseMaintenance.models import CaseBaseData as db_CaseBaseData
from Api_CaseMaintenance.models import CaseTestSet as db_CaseTestSet
from Api_CaseMaintenance.models import CaseApiBase as db_CaseApiBase
from Api_CaseMaintenance.models import CaseApiHeaders as db_CaseApiHeaders
from Api_CaseMaintenance.models import CaseApiParams as db_CaseApiParams
from Api_CaseMaintenance.models import CaseApiBody as db_CaseApiBody
from Api_CaseMaintenance.models import CaseApiExtract as db_CaseApiExtract
from Api_CaseMaintenance.models import CaseApiValidate as db_CaseApiValidate
from Api_CaseMaintenance.models import CaseApiOperation as db_CaseApiOperation
from Api_TestReport.models import ApiTestReport as db_ApiTestReport
from Api_TimingTask.models import ApiTimingTaskTestSet as db_ApiTimingTaskTestSet
from Api_CaseMaintenance.models import ApiCaseHistory as db_ApiCaseHistory

# Create reference here.
from ClassData.Logger import Logging
from ClassData.GlobalDecorator import GlobalDer
from ClassData.FindCommonTable import FindTable
from ClassData.Common import Common
from ClassData.ImageProcessing import ImageProcessing
from ClassData.ObjectMaker import object_maker as cls_object_maker
from ClassData.Request import RequstOperation
from ClassData.TestReport import ApiReport
from ClassData.Redis import RedisHandle
from ClassData.FileOperations import FileOperations

from Task.tasks import api_asynchronous_run_case

# Create info here.
cls_Logging = Logging()
cls_GlobalDer = GlobalDer()
cls_FindTable = FindTable()
cls_Common = Common()
cls_ImageProcessing = ImageProcessing()
cls_RequstOperation = RequstOperation()
cls_ApiReport = ApiReport()
cls_RedisHandle = RedisHandle()
cls_FileOperations = FileOperations()


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

        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        proId = objData.proId
        pageId = objData.pageId
        funId = objData.funId
        testType = objData.testType
        labelId = objData.labelId
        caseState = objData.caseState
        caseName = objData.caseName
        associations = objData.associations

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_CaseMaintenance', 'select_data', errorMsg)
    else:
        obj_db_CaseBaseData = db_CaseBaseData.objects.filter(is_del=0, pid_id=proId).order_by('-updateTime')
        if pageId:
            obj_db_CaseBaseData = obj_db_CaseBaseData.filter(page_id=pageId)
        if funId:
            obj_db_CaseBaseData = obj_db_CaseBaseData.filter(fun_id=funId)
        if testType:
            obj_db_CaseBaseData = obj_db_CaseBaseData.filter(testType=testType)
        if labelId:
            obj_db_CaseBaseData = obj_db_CaseBaseData.filter(label=labelId)
        if caseState:
            obj_db_CaseBaseData = obj_db_CaseBaseData.filter(caseState=caseState)
        if caseName:
            obj_db_CaseBaseData = obj_db_CaseBaseData.filter(caseName__icontains=caseName)
        select_db_CaseBaseData = obj_db_CaseBaseData[minSize: maxSize]
        for i in select_db_CaseBaseData:
            obj_db_ApiDynamic = db_ApiDynamic.objects.filter(is_del=0, case_id=i.id, is_read=0)
            if obj_db_ApiDynamic.exists():
                apidynamic = True
            else:
                apidynamic = False
            tableItem = []
            obj_db_CaseTestSet = db_CaseTestSet.objects.filter(is_del=0, caseId_id=i.id)
            for item_testSet in obj_db_CaseTestSet:
                obj_db_CaseApiBase = db_CaseApiBase.objects.filter(is_del=0, testSet_id=item_testSet.id)
                if obj_db_CaseApiBase.exists():
                    requestType = obj_db_CaseApiBase[0].requestType
                    requestParamsType = obj_db_CaseApiBase[0].requestParamsType
                else:
                    requestType = None
                    requestParamsType = None
                tableItem.append({
                    'index': item_testSet.index,
                    'apiName': item_testSet.apiId.apiName,
                    'testName': item_testSet.testName,
                    'requestType': requestType,
                    'requestParamsType': requestParamsType,
                    'state': True if item_testSet.state == 1 else False,
                    'updateTime': str(item_testSet.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                })
            # region 通过率
            obj_db_ApiTestReport = db_ApiTestReport.objects.filter(is_del=0, taskId=i.id)
            passTotal = obj_db_ApiTestReport.filter(reportStatus='Pass').count()
            if obj_db_ApiTestReport.count() == 0:
                passRate = 0
            else:
                passRate = round(passTotal / obj_db_ApiTestReport.count() * 100, 2)
            # endregion
            if associations == 'My':
                # 当前查询的用户是修改者 或是 创建者
                if userId == i.uid_id or userId == i.cuid:
                    dataList.append({
                        'id': i.id,
                        'tableItem': tableItem,
                        'priority': i.priority,
                        'testType': i.testType,
                        'caseName': i.caseName,
                        'pageName': i.page.pageName,
                        'funName': i.fun.funName,
                        'labelId': i.label,
                        'apidynamic': apidynamic,
                        'caseState': i.caseState,
                        'passRate': passRate,
                        'updateTime': str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                        "userName": f"{i.uid.userName}({i.uid.nickName})",
                        'createUserName': cls_FindTable.get_userName(i.cuid),
                    })
            else:
                dataList.append({
                    'id': i.id,
                    'tableItem': tableItem,
                    'priority': i.priority,
                    'testType': i.testType,
                    'caseName': i.caseName,
                    'pageName': i.page.pageName,
                    'funName': i.fun.funName,
                    'labelId': i.label,
                    'apidynamic': apidynamic,
                    'caseState': i.caseState,
                    'passRate': passRate,
                    'updateTime': str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                    "userName": f"{i.uid.userName}({i.uid.nickName})",
                    'createUserName': cls_FindTable.get_userName(i.cuid),
                })
        response['TableData'] = dataList
        response['Total'] = obj_db_CaseBaseData.count()
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def load_data(request):
    response = {}
    headers = []
    params = []
    body = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)

        # if '-' in objData.apiId:
        #     apiId = objData.apiId.split('-')[0]
        # else:
        apiId = objData.apiId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_CaseMaintenance', 'load_data', errorMsg)
    else:
        obj_db_ApiBaseData = db_ApiBaseData.objects.filter(is_del=0, id=apiId)
        if obj_db_ApiBaseData.exists():
            requestType = obj_db_ApiBaseData[0].requestType
            requestUrlRadio = obj_db_ApiBaseData[0].requestUrlRadio
            requestUrl = ast.literal_eval(obj_db_ApiBaseData[0].requestUrl)[f'url{requestUrlRadio}']
            # region headers
            obj_db_ApiHeaders = db_ApiHeaders.objects.filter(is_del=0, apiId_id=apiId).order_by('index')
            for item_headers in obj_db_ApiHeaders:
                headers.append({
                    'index': item_headers.index,
                    'key': item_headers.key,
                    'value': item_headers.value,
                    'remarks': item_headers.remarks,
                    'state': True if item_headers.state else False,
                })
            # endregion
            # region params
            obj_db_ApiParams = db_ApiParams.objects.filter(is_del=0, apiId_id=apiId).order_by('index')
            for item_params in obj_db_ApiParams:
                params.append({
                    'index': item_params.index,
                    'key': item_params.key,
                    'value': item_params.value,
                    'remarks': item_params.remarks,
                    'state': True if item_params.state else False,
                })
            # endregion
            # region body
            bodyData = None
            obj_db_ApiBody = db_ApiBody.objects.filter(is_del=0, apiId_id=apiId).order_by('index')
            requestSaveType = obj_db_ApiBaseData[0].bodyRequestSaveType
            if obj_db_ApiBaseData[0].bodyRequestSaveType == 'form-data':
                for item_body in obj_db_ApiBody:
                    if item_body.paramsType == 'Text':
                        fileList = []
                    else:
                        splitStr = item_body.filePath.split('/')
                        name = splitStr[-1]
                        url = f"{settings.NGINX_SERVER}ApiFile/{apiId}/{name}"
                        fileList = [
                            {'name': name, 'url': url}
                        ]
                    body.append({
                        'index': item_body.index,
                        'key': item_body.key,
                        'paramsType': item_body.paramsType,
                        'value': item_body.value,
                        'fileList': fileList,
                        'remarks': item_body.remarks,
                        'state': True if item_body.state else False,
                    })
                bodyData = body
            elif obj_db_ApiBaseData[0].bodyRequestSaveType in ('raw','json'):
                bodyData = obj_db_ApiBody[0].value
            else:
                pass
            # endregion

            apiInfo = {
                'requestType': requestType,
                'requestUrl': requestUrl,
                'request': {
                    'headers': headers,
                    'params': params,
                    'body': {
                        'requestSaveType': requestSaveType,
                        'bodyData': bodyData
                    },
                }
            }

            response['apiInfo'] = apiInfo
            response['statusCode'] = 2000
        else:
            response['errorMsg'] = "未找到当前选择的接口数据,请刷新后重新尝试!"
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 效验接用例数据的完成性
def charm_case_data(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(request.body)
        objData = cls_object_maker(responseData)
        charmType = objData.CharmType  # true 新增，false 修改
        basicInfo = objData.BasicInfo
        testSet = objData.TestSet
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_CaseMaintenance', 'charm_case_data', errorMsg)
    else:
        # region 验证基本信息
        obj_db_CaseBaseData = db_CaseBaseData.objects.filter(
            is_del=0, pid_id=basicInfo.proId, page_id=basicInfo.pageId, fun_id=basicInfo.funId,
            label=basicInfo.labelId, testType=basicInfo.testType, caseName=basicInfo.caseName
        )
        if obj_db_CaseBaseData.exists():
            if charmType:
                dataList.append({
                    'stepsName': '基本信息',
                    'errorMsg': '当前所属功能及同标签同类型下已有相同用例名称,请更改!',
                    'updateTime': cls_Common.get_date_time()})
            else:
                if obj_db_CaseBaseData.exists():
                    if basicInfo.caseId == obj_db_CaseBaseData[0].id:
                        pass
                    else:
                        dataList.append({
                            'stepsName': '基本信息',
                            'errorMsg': '当前所属功能及同标签同类型下已有相同用例名称,请更改!',
                            'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证测试集
        for index_testSet, item_testSet in enumerate(testSet, 1):
            # region 验证 headers
            if item_testSet.request.headers:
                for index, item_headers in enumerate(item_testSet.request.headers, 1):
                    if item_headers.state:
                        if not item_headers.key:
                            dataList.append({
                                'stepsName': f'接口信息-Headers',
                                'errorMsg': f'测试集(顺序:{index_testSet}):第{index}行:参数名称不可为空!',
                                'updateTime': cls_Common.get_date_time()})
            # endregion
            # region 验证 params
            if item_testSet.request.params:
                for index, item_params in enumerate(item_testSet.request.params, 1):
                    if item_params.state:
                        if not item_params.key:
                            dataList.append({
                                'stepsName': '接口信息-Params',
                                'errorMsg': f'测试集(顺序:{index_testSet}):{index_testSet}):第{index}行:参数名称不可为空!',
                                'updateTime': cls_Common.get_date_time()})
            # endregion
            # region 验证 body
            if item_testSet.request.body.requestSaveType == 'form-data':
                for index, item_body in enumerate(item_testSet.request.body.formData, 1):
                    if item_body.paramsType == 'Text':
                        if not item_body.key:
                            dataList.append({
                                'stepsName': '接口信息-Body',
                                'errorMsg': f'第{index}行:参数名称不可为空!',
                                'updateTime': cls_Common.get_date_time()})
                    else:  # 文件类型
                        if not item_body.key:
                            dataList.append({
                                'stepsName': '接口信息-Body',
                                'errorMsg': f'第{index}行:参数名称不可为空!',
                                'updateTime': cls_Common.get_date_time()})
                        if not item_body.fileList:
                            dataList.append({
                                'stepsName': '接口信息-Body',
                                'errorMsg': f'第{index}行:上传文件不可为空!',
                                'updateTime': cls_Common.get_date_time()})
            elif item_testSet.request.body.requestSaveType == 'raw':
                if not item_testSet.request.body.rawValue:
                    dataList.append({
                        'stepsName': '接口信息-Body',
                        'errorMsg': f'Raw参数不可为空!',
                        'updateTime': cls_Common.get_date_time()})
            elif item_testSet.request.body.requestSaveType == 'json':
                if not item_testSet.request.body.jsonValue:
                    dataList.append({
                        'stepsName': '接口信息-Body',
                        'errorMsg': f'Json参数不可为空!',
                        'updateTime': cls_Common.get_date_time()})
            # endregion
            # region 验证 提取
            if item_testSet.request.extract:
                for index, item_extract in enumerate(item_testSet.request.extract, 1):
                    if item_extract.state:
                        if not item_extract.key:
                            dataList.append({
                                'stepsName': '接口信息-Extract',
                                'errorMsg': f'测试集(顺序:{index_testSet}):第{index}行:变量名称不可为空!',
                                'updateTime': cls_Common.get_date_time()})
                        if not item_extract.value:
                            dataList.append({
                                'stepsName': '接口信息-Extract',
                                'errorMsg': f'测试集(顺序:{index_testSet}):第{index}行:提取表达式不可为空!',
                                'updateTime': cls_Common.get_date_time()})
            # endregion
            # region 验证 断言
            if item_testSet.request.validate:
                for index, item_validate in enumerate(item_testSet.request.validate, 1):
                    if item_validate.state:
                        if not item_validate.checkName:
                            dataList.append({
                                'stepsName': '接口信息-Validate',
                                'errorMsg': f'测试集(顺序:{index_testSet}):第{index}行,提取变量名称不可为空!',
                                'updateTime': cls_Common.get_date_time()})
                        if not item_validate.validateType:
                            dataList.append({
                                'stepsName': '接口信息-Validate',
                                'errorMsg': f'测试集(顺序:{index_testSet}):第{index}行,断言类型不可为空!',
                                'updateTime': cls_Common.get_date_time()})
                        if not item_validate.valueType:
                            dataList.append({
                                'stepsName': '接口信息-Validate',
                                'errorMsg': f'测试集(顺序:{index_testSet}):第{index}行:断言值类型不可为空!',
                                'updateTime': cls_Common.get_date_time()})
            # endregion
            # region 验证 前置操作
            if item_testSet.request.preOperation:
                for index, item_preOperation in enumerate(item_testSet.request.preOperation, 1):
                    if item_preOperation.state:
                        if item_preOperation.operationType == 'Methods':
                            if not item_preOperation.methodsName:
                                dataList.append({
                                    'stepsName': '接口信息-前置操作',
                                    'errorMsg': f'测试集(顺序:{index_testSet}):第{index}行:函数方法名称不可为空!',
                                    'updateTime': cls_Common.get_date_time()})
                            if '(' not in item_preOperation.methodsName or ')' not in item_preOperation.methodsName:
                                dataList.append({
                                    'stepsName': '接口信息-前置操作',
                                    'errorMsg': f'测试集(顺序:{index_testSet}):第{index}行:函数方法名称未检测到 ()',
                                    'updateTime': cls_Common.get_date_time()})

                        elif item_preOperation.operationType == 'DataBase':
                            if not item_preOperation.dataBase:
                                dataList.append({
                                    'stepsName': '接口信息-前置操作',
                                    'errorMsg': f'测试集(顺序:{index_testSet}):第{index}行:当前没有选择需要执行的数据库!',
                                    'updateTime': cls_Common.get_date_time()})
                            if not item_preOperation.sql:
                                dataList.append({
                                    'stepsName': '接口信息-前置操作',
                                    'errorMsg': f'测试集(顺序:{index_testSet}):第{index}行:请输入SQL语句!',
                                    'updateTime': cls_Common.get_date_time()})
            # endregion
            # region 验证 后置操作
            if item_testSet.request.rearOperation:
                for index, item_rearOperation in enumerate(item_testSet.request.rearOperation, 1):
                    if item_rearOperation.state:
                        if item_rearOperation.operationType == 'Methods':
                            if not item_rearOperation.methodsName:
                                dataList.append({
                                    'stepsName': '接口信息-后置操作',
                                    'errorMsg': f'测试集(顺序:{index_testSet}):第{index}行:函数方法名称不可为空!',
                                    'updateTime': cls_Common.get_date_time()})
                            if '(' not in item_rearOperation.methodsName or ')' not in item_rearOperation.methodsName:
                                dataList.append({
                                    'stepsName': '接口信息-后置操作',
                                    'errorMsg': f'测试集(顺序:{index_testSet}):第{index}行:函数方法名称未检测到 ()',
                                    'updateTime': cls_Common.get_date_time()})
                        elif item_rearOperation.operationType == 'DataBase':
                            if not item_rearOperation.dataBase:
                                dataList.append({
                                    'stepsName': '接口信息-后置操作',
                                    'errorMsg': f'测试集(顺序:{index_testSet}):第{index}行:当前没有选择需要执行的数据库!',
                                    'updateTime': cls_Common.get_date_time()})
                            if not item_rearOperation.sql:
                                dataList.append({
                                    'stepsName': '接口信息-后置操作',
                                    'errorMsg': f'测试集(顺序:{index_testSet}):第{index}行:请输入SQL语句!',
                                    'updateTime': cls_Common.get_date_time()})
            # endregion
            # region 验证params 和body 至少有1个有参数
            if not item_testSet.request.params and \
                    not item_testSet.request.body.formData and \
                    not item_testSet.request.body.rawValue and \
                    not item_testSet.request.body.jsonValue and \
                    not item_testSet.request.body.requestSaveType == 'none':
                dataList.append({
                    'stepsName': '接口信息-参数请求',
                    'errorMsg': f'测试集(顺序:{index_testSet}):不可创建空参数请求,Params或Body请求中至少有1个不可为空!',
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
        cls_Logging.record_error_info('API', 'Api_CaseMaintenance', 'data_save', errorMsg)
    else:
        obj_db_CaseBaseData = db_CaseBaseData.objects.filter(
            is_del=0, pid_id=basicInfo.proId, page_id=basicInfo.pageId, fun_id=basicInfo.funId,
            label=basicInfo.labelId, testType=basicInfo.testType, caseName=basicInfo.caseName
        )
        if obj_db_CaseBaseData.exists():
            response['errorMsg'] = f'当前所属功能及同标签同类型下已有相同用例名称,请更改!'
        else:
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    # region 添加操作信息
                    cls_Logging.record_operation_info(
                        'API', 'Manual', 3, 'Add',
                        cls_FindTable.get_pro_name(basicInfo.proId),
                        cls_FindTable.get_page_name(basicInfo.pageId),
                        cls_FindTable.get_fun_name(basicInfo.funId),
                        userId,
                        '【新增用例】', CUFront=responseData
                    )
                    # endregion
                    # region 保存基本信息
                    save_db_CaseBaseData = db_CaseBaseData.objects.create(
                        pid_id=basicInfo.proId, page_id=basicInfo.pageId, fun_id=basicInfo.funId,
                        environmentId_id=basicInfo.environmentId, testType=basicInfo.testType,
                        label=basicInfo.labelId, priority=basicInfo.priorityId, caseName=basicInfo.caseName,
                        caseState=basicInfo.caseState, cuid=userId, uid_id=userId, is_del=0,onlyCode=onlyCode
                    )
                    # endregion
                    # region 历史恢复
                    restoreData = responseData
                    restoreData['BasicInfo']['updateTime'] = save_db_CaseBaseData.updateTime.strftime(
                        '%Y-%m-%d %H:%M:%S')
                    restoreData['BasicInfo']['createTime'] = save_db_CaseBaseData.createTime.strftime(
                        '%Y-%m-%d %H:%M:%S')
                    restoreData['BasicInfo']['uid_id'] = save_db_CaseBaseData.uid_id
                    restoreData['BasicInfo']['cuid'] = save_db_CaseBaseData.cuid
                    restoreData['onlyCode'] = onlyCode
                    db_ApiCaseHistory.objects.create(
                        pid_id=basicInfo.proId,
                        page_id=basicInfo.pageId,
                        fun_id=basicInfo.funId,
                        case_id=save_db_CaseBaseData.id,
                        caseName=basicInfo.caseName,
                        onlyCode=onlyCode,
                        operationType='Add',
                        restoreData=restoreData,
                        uid_id=userId
                    )
                    # endregion
                    # region 测试集
                    for item_index, item_testSet in enumerate(testSet, 0):
                        pluralIntId = item_testSet.id
                        apiId = item_testSet.apiId
                        save_db_CaseTestSet = db_CaseTestSet.objects.create(
                            caseId_id=save_db_CaseBaseData.id,
                            index=item_index,
                            apiId_id=apiId,
                            pluralIntId=pluralIntId,
                            testName=item_testSet.testName,
                            is_synchronous=1 if item_testSet.is_synchronous else 0,
                            state=1 if item_testSet.state else 0,
                            uid_id=userId,
                            is_del=0,
                            onlyCode=onlyCode
                        )
                        # region 请求基本数据
                        headers = item_testSet.request.headers
                        params = item_testSet.request.params
                        bodyRequestSaveType = item_testSet.request.body.requestSaveType
                        bodyFormData = item_testSet.request.body.formData
                        bodyRawValue = item_testSet.request.body.rawValue
                        bodyJsonValue = item_testSet.request.body.jsonValue
                        extract = item_testSet.request.extract
                        validate = item_testSet.request.validate
                        preOperation = item_testSet.request.preOperation
                        rearOperation = item_testSet.request.rearOperation

                        requestParamsType = cls_RequstOperation.for_data_get_requset_params_type(
                            params, bodyFormData, bodyRawValue, bodyJsonValue
                        )
                        db_CaseApiBase.objects.create(
                            testSet_id=save_db_CaseTestSet.id,
                            requestType=item_testSet.request.requestType,
                            requestUrl=item_testSet.request.requestUrl,
                            requestParamsType=requestParamsType,
                            bodyRequestSaveType=bodyRequestSaveType,
                            is_del=0,onlyCode=onlyCode
                        )
                        # endregion
                        # region Headers
                        product_list_to_insert = list()
                        for item_headers in headers:
                            product_list_to_insert.append(db_CaseApiHeaders(
                                testSet_id=save_db_CaseTestSet.id,
                                index=item_headers.index,
                                key=item_headers.key,
                                value=item_headers.value,
                                remarks=item_headers.remarks,
                                state=1 if item_headers.state else 0,
                                is_del=0,onlyCode=onlyCode)
                            )
                        db_CaseApiHeaders.objects.bulk_create(product_list_to_insert)
                        # endregion
                        # region Params
                        product_list_to_insert = list()
                        for item_params in params:
                            product_list_to_insert.append(db_CaseApiParams(
                                testSet_id=save_db_CaseTestSet.id,
                                index=item_params.index,
                                key=item_params.key,
                                value=item_params.value,
                                remarks=item_params.remarks,
                                state=1 if item_params.state else 0,
                                is_del=0,onlyCode=onlyCode)
                            )
                        db_CaseApiParams.objects.bulk_create(product_list_to_insert)
                        # endregion
                        # region Body
                        # region 删除多次上传的一些不需要的文件
                        deleteFileList = item_testSet.request.body.deleteFileList
                        for item_delFile in deleteFileList:
                            if item_delFile.dirName == 'Temp':
                                filePath = settings.TEMP_PATH
                            else:
                                filePath = f"{settings.CASEFILE_PATH}{item_delFile.dirName}"
                            cls_FileOperations.delete_file(f"{filePath}{item_delFile.fileName}")
                        # endregion
                        if bodyRequestSaveType == 'form-data':
                            product_list_to_insert = list()
                            for item_body in bodyFormData:
                                paramsType = item_body.paramsType
                                if paramsType == 'Text':
                                    filePath = None
                                else:  # file
                                    # region file文件处理
                                    filePath = None
                                    fileData = item_body.fileList[0]._object_maker__data
                                    fileName = fileData['name']
                                    # 创建文件夹
                                    newFolder = cls_FileOperations.new_folder(
                                        f'{settings.CASEFILE_PATH}{save_db_CaseBaseData.id}/{save_db_CaseTestSet.id}')
                                    if newFolder['state']:
                                        # 复制文件从临时目录到接口目录
                                        copyFile = cls_FileOperations.copy_file_to_dir(
                                            f'{settings.TEMP_PATH}{fileName}', newFolder['path'])
                                        if copyFile['state']:
                                            filePath = copyFile['newFilePath']
                                        else:
                                            # 删除新增的文件夹
                                            cls_FileOperations.delete_folder(newFolder['path'])
                                            raise FileExistsError(copyFile['errorMsg'])
                                    else:
                                        raise FileExistsError(newFolder['errorMsg'])
                                    # endregion
                                product_list_to_insert.append(db_CaseApiBody(
                                    testSet_id=save_db_CaseTestSet.id,
                                    index=item_body.index,
                                    key=item_body.key,
                                    paramsType=item_body.paramsType,
                                    value=item_body.value,
                                    filePath=filePath,
                                    remarks=item_body.remarks,
                                    state=1 if item_body.state else 0,
                                    is_del=0,onlyCode=onlyCode)
                                )
                            db_CaseApiBody.objects.bulk_create(product_list_to_insert)
                        elif bodyRequestSaveType in ['raw', 'json']:
                            if bodyRequestSaveType == 'raw':
                                value = bodyRawValue
                            elif bodyRequestSaveType == 'json':
                                value = bodyJsonValue
                            else:
                                value = None
                            db_CaseApiBody.objects.create(
                                testSet_id=save_db_CaseTestSet.id,
                                index=0,
                                key=None,
                                value=value,
                                state=1,
                                is_del=0,onlyCode=onlyCode
                            )
                        # file 之后在做
                        # endregion
                        # region Extract
                        product_list_to_insert = list()
                        for item_extract in extract:
                            product_list_to_insert.append(db_CaseApiExtract(
                                testSet_id=save_db_CaseTestSet.id,
                                index=item_extract.index,
                                key=item_extract.key,
                                value=item_extract.value,
                                remarks=item_extract.remarks,
                                state=1 if item_extract.state else 0,
                                is_del=0,onlyCode=onlyCode )
                            )
                        db_CaseApiExtract.objects.bulk_create(product_list_to_insert)
                        # endregion
                        # region Validate
                        product_list_to_insert = list()
                        for item_validate in validate:
                            product_list_to_insert.append(db_CaseApiValidate(
                                testSet_id=save_db_CaseTestSet.id,
                                index=item_validate.index,
                                checkName=item_validate.checkName,
                                validateType=item_validate.validateType,
                                valueType=item_validate.valueType,
                                expectedResults=item_validate.expectedResults,
                                remarks=item_validate.remarks,
                                state=1 if item_validate.state else 0,
                                is_del=0,onlyCode=onlyCode)
                            )
                        db_CaseApiValidate.objects.bulk_create(product_list_to_insert)
                        # endregion
                        # region 前置
                        product_list_to_insert = list()
                        for item_preOperation in preOperation:
                            product_list_to_insert.append(db_CaseApiOperation(
                                testSet_id=save_db_CaseTestSet.id,
                                index=item_preOperation.index,
                                location='Pre',
                                operationType=item_preOperation.operationType,
                                methodsName=item_preOperation.methodsName,
                                dataBaseId=item_preOperation.dataBase,
                                sql=item_preOperation.sql,
                                remarks=item_preOperation.remarks,
                                state=1 if item_preOperation.state else 0,
                                is_del=0,onlyCode=onlyCode)
                            )
                        db_CaseApiOperation.objects.bulk_create(product_list_to_insert)
                        # endregion
                        # region 后置
                        product_list_to_insert = list()
                        for item_rearOperation in rearOperation:
                            product_list_to_insert.append(db_CaseApiOperation(
                                testSet_id=save_db_CaseTestSet.id,
                                index=item_rearOperation.index,
                                location='Rear',
                                operationType=item_rearOperation.operationType,
                                methodsName=item_rearOperation.methodsName,
                                dataBaseId=item_rearOperation.dataBase,
                                sql=item_rearOperation.sql,
                                remarks=item_rearOperation.remarks,
                                state=1 if item_rearOperation.state else 0,
                                is_del=0,onlyCode=onlyCode )
                            )
                        db_CaseApiOperation.objects.bulk_create(product_list_to_insert)
                        # endregion
                    # endregion
            except BaseException as e:  # 自动回滚，不需要任何操作
                response['errorMsg'] = f'保存失败:{e}'
            else:
                response['statusCode'] = 2001
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
        onlyCode = cls_Common.generate_only_code()
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_CaseMaintenance', 'edit_data', errorMsg)
    else:
        obj_db_CaseBaseData = db_CaseBaseData.objects.filter(is_del=0, id=basicInfo.caseId)
        if obj_db_CaseBaseData.exists():
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    # region 添加操作信息
                    # region 查询以前的数据
                    oldTestSet = []
                    obj_db_CaseTestSet = db_CaseTestSet.objects.filter(
                        is_del=0, caseId_id=basicInfo.caseId).order_by('index')
                    for item_testSet in obj_db_CaseTestSet:
                        settingParams = False
                        oldRequestData = {
                            'requestType': 'GET',
                            'requestUrl': '',
                            'headers': [],
                            'params': [],
                            'body': {
                                'requestSaveType': 'form-data',
                                'formData': [],
                                'rawValue': '',
                                'jsonValue': '',
                            },
                            'extract': [],
                            'validate': [],
                            'preOperation': [],
                            'rearOperation': [],
                        }
                        obj_db_CaseApiBase = db_CaseApiBase.objects.filter(is_del=0, testSet_id=item_testSet.id)
                        if obj_db_CaseApiBase.exists():
                            oldRequestData['requestType'] = obj_db_CaseApiBase[0].requestType
                            oldRequestData['requestUrl'] = obj_db_CaseApiBase[0].requestUrl
                            oldRequestData['body']['requestSaveType'] = obj_db_CaseApiBase[0].bodyRequestSaveType
                            if obj_db_CaseApiBase[0].requestUrl:
                                settingParams = True
                                # region headers
                                obj_db_CaseApiHeaders = db_CaseApiHeaders.objects.filter(
                                    is_del=0, testSet_id=item_testSet.id).order_by('index')
                                for item_headers in obj_db_CaseApiHeaders:
                                    oldRequestData['headers'].append({
                                        'index': item_headers.index,
                                        'state': True if item_headers.state == 1 else False,
                                        'key': item_headers.key,
                                        'value': item_headers.value,
                                        'remarks': item_headers.remarks,
                                    })
                                # endregion
                                # region params
                                obj_db_CaseApiParams = db_CaseApiParams.objects.filter(
                                    is_del=0, testSet_id=item_testSet.id).order_by('index')
                                for item_params in obj_db_CaseApiParams:
                                    oldRequestData['params'].append({
                                        'index': item_params.index,
                                        'state': True if item_params.state == 1 else False,
                                        'key': item_params.key,
                                        'value': item_params.value,
                                        'remarks': item_params.remarks,
                                    })
                                # endregion
                                # region body
                                obj_db_CaseApiBody = db_CaseApiBody.objects.filter(
                                    is_del=0, testSet_id=item_testSet.id).order_by('index')
                                if obj_db_CaseApiBase[0].bodyRequestSaveType == 'form-data':
                                    for item_body in obj_db_CaseApiBody:
                                        oldRequestData['body']['formData'].append({
                                            'index': item_body.index,
                                            'state': True if item_body.state == 1 else False,
                                            'key': item_body.key,
                                            'value': item_body.value,
                                            'remarks': item_body.remarks,
                                        })
                                elif obj_db_CaseApiBase[0].bodyRequestSaveType == 'raw':
                                    oldRequestData['body']['rawValue'] = obj_db_CaseApiBody[0].value
                                elif obj_db_CaseApiBase[0].bodyRequestSaveType == 'json':
                                    oldRequestData['body']['jsonValue'] = obj_db_CaseApiBody[0].value
                                # endregion
                                # region Extract
                                obj_db_CaseApiExtract = db_CaseApiExtract.objects.filter(
                                    is_del=0, testSet_id=item_testSet.id).order_by('index')
                                for item_extract in obj_db_CaseApiExtract:
                                    oldRequestData['extract'].append({
                                        'index': item_extract.index,
                                        'state': True if item_extract.state == 1 else False,
                                        'key': item_extract.key,
                                        'value': item_extract.value,
                                        'remarks': item_extract.remarks,
                                    })
                                # endregion
                                # region Validate
                                obj_db_CaseApiValidate = db_CaseApiValidate.objects.filter(
                                    is_del=0, testSet_id=item_testSet.id).order_by('index')
                                for item_validate in obj_db_CaseApiValidate:
                                    oldRequestData['validate'].append({
                                        'index': item_validate.index,
                                        'state': True if item_validate.state == 1 else False,
                                        'checkName': item_validate.checkName,
                                        'validateType': item_validate.validateType,
                                        'valueType': item_validate.valueType,
                                        'expectedResults': item_validate.expectedResults,
                                        'remarks': item_validate.remarks,
                                    })
                                # endregion
                                # region 前置操作
                                obj_db_CaseApiOperation = db_CaseApiOperation.objects.filter(
                                    is_del=0, testSet_id=item_testSet.id, location='Pre').order_by('index')
                                for item_preOperation in obj_db_CaseApiOperation:
                                    oldRequestData['preOperation'].append({
                                        'id': item_preOperation.index,
                                        'index': item_preOperation.index,
                                        'state': True if item_preOperation.state == 1 else False,
                                        'operationType': item_preOperation.operationType,
                                        'methodsName': item_preOperation.methodsName,
                                        'dataBase': item_preOperation.dataBaseId,
                                        'sql': item_preOperation.sql,
                                        'remarks': item_preOperation.remarks,
                                    })
                                # endregion
                                # region 后置操作
                                obj_db_CaseApiOperation = db_CaseApiOperation.objects.filter(
                                    is_del=0, testSet_id=item_testSet.id, location='Rear').order_by('index')
                                for item_rearOperation in obj_db_CaseApiOperation:
                                    oldRequestData['rearOperation'].append({
                                        'id': item_rearOperation.index,
                                        'index': item_rearOperation.index,
                                        'state': True if item_rearOperation.state == 1 else False,
                                        'operationType': item_rearOperation.operationType,
                                        'methodsName': item_rearOperation.methodsName,
                                        'dataBase': item_rearOperation.dataBaseId,
                                        'sql': item_rearOperation.sql,
                                        'remarks': item_rearOperation.remarks,
                                    })
                                # endregion
                        oldTestSet.append({
                            'apiId': item_testSet.apiId_id,
                            'state': True if item_testSet.state == 1 else False,
                            'apiName': item_testSet.apiId.apiName,
                            'apiState': item_testSet.apiId.apiState,
                            'testName': item_testSet.testName,
                            'is_synchronous': True if item_testSet.is_synchronous == 1 else False,
                            'settingParams': settingParams,
                            'request': oldRequestData
                        })
                    oldData = {
                        'basicInfo': {
                            'caseId': obj_db_CaseBaseData[0].id,
                            'proId': obj_db_CaseBaseData[0].pid_id,
                            'pageId': obj_db_CaseBaseData[0].page_id,
                            'funId': obj_db_CaseBaseData[0].fun_id,
                            'environmentId': obj_db_CaseBaseData[0].environmentId_id,
                            'priorityId': obj_db_CaseBaseData[0].priority,
                            'labelId': obj_db_CaseBaseData[0].label,
                            'testType': obj_db_CaseBaseData[0].testType,
                            'caseName': obj_db_CaseBaseData[0].caseName,
                            'caseState': obj_db_CaseBaseData[0].caseState,
                        },
                        'testSet': oldTestSet,

                    }
                    cls_Logging.record_operation_info(
                        'API', 'Manual', 3, 'Edit',
                        cls_FindTable.get_pro_name(basicInfo.proId),
                        cls_FindTable.get_page_name(basicInfo.pageId),
                        cls_FindTable.get_fun_name(basicInfo.funId),
                        userId,
                        f'【修改用例】 ID{obj_db_CaseBaseData[0].id}:{obj_db_CaseBaseData[0].caseName}',
                        CUFront=oldData, CURear=responseData
                    )

                    # endregion
                    # endregion
                    # region 历史恢复
                    restoreData = responseData
                    restoreData['BasicInfo']['updateTime'] = obj_db_CaseBaseData[0].updateTime.strftime(
                        '%Y-%m-%d %H:%M:%S')
                    restoreData['BasicInfo']['createTime'] = obj_db_CaseBaseData[0].createTime.strftime(
                        '%Y-%m-%d %H:%M:%S')
                    restoreData['BasicInfo']['uid_id'] = obj_db_CaseBaseData[0].uid_id
                    restoreData['BasicInfo']['cuid'] = obj_db_CaseBaseData[0].cuid
                    restoreData['onlyCode'] = onlyCode
                    db_ApiCaseHistory.objects.create(
                        pid_id=basicInfo.proId,
                        page_id=basicInfo.pageId,
                        fun_id=basicInfo.funId,
                        case_id=basicInfo.caseId,
                        caseName=basicInfo.caseName,
                        onlyCode=onlyCode,
                        operationType='Edit',
                        restoreData=restoreData,
                        uid_id=userId
                    )
                    # endregion
                    # region 删除 各类原数据
                    obj_db_CaseTestSet = db_CaseTestSet.objects.filter(is_del=0, caseId_id=basicInfo.caseId)
                    for item_testSet in obj_db_CaseTestSet:
                        db_CaseApiBase.objects.filter(is_del=0, testSet_id=item_testSet.id).update(
                            is_del=1, updateTime=cls_Common.get_date_time()
                        )
                        db_CaseApiHeaders.objects.filter(is_del=0, testSet_id=item_testSet.id).update(
                            is_del=1, updateTime=cls_Common.get_date_time()
                        )
                        db_CaseApiParams.objects.filter(is_del=0, testSet_id=item_testSet.id).update(
                            is_del=1, updateTime=cls_Common.get_date_time()
                        )
                        db_CaseApiBody.objects.filter(is_del=0, testSet_id=item_testSet.id).update(
                            is_del=1, updateTime=cls_Common.get_date_time()
                        )
                        db_CaseApiExtract.objects.filter(is_del=0, testSet_id=item_testSet.id).update(
                            is_del=1, updateTime=cls_Common.get_date_time()
                        )
                        db_CaseApiValidate.objects.filter(is_del=0, testSet_id=item_testSet.id).update(
                            is_del=1, updateTime=cls_Common.get_date_time()
                        )
                        db_CaseApiOperation.objects.filter(is_del=0, testSet_id=item_testSet.id).update(
                            is_del=1, updateTime=cls_Common.get_date_time()
                        )
                    obj_db_CaseTestSet.update(is_del=1, updateTime=cls_Common.get_date_time(), uid_id=userId)
                    # endregion
                    # region 更新基本信息
                    db_CaseBaseData.objects.filter(is_del=0, id=basicInfo.caseId).update(
                        pid_id=basicInfo.proId, page_id=basicInfo.pageId, fun_id=basicInfo.funId,
                        environmentId_id=basicInfo.environmentId, testType=basicInfo.testType,
                        label=basicInfo.labelId, priority=basicInfo.priorityId, caseName=basicInfo.caseName,
                        caseState=basicInfo.caseState, uid_id=userId, updateTime=cls_Common.get_date_time(),
                        onlyCode=onlyCode
                    )
                    # endregion
                    # region 测试集
                    for item_index, item_testSet in enumerate(testSet, 0):
                        pluralIntId = item_testSet.id
                        apiId = item_testSet.apiId
                        save_db_CaseTestSet = db_CaseTestSet.objects.create(
                            caseId_id=basicInfo.caseId,
                            index=item_index,
                            apiId_id=apiId,
                            pluralIntId=pluralIntId,
                            testName=item_testSet.testName,
                            is_synchronous=1 if item_testSet.is_synchronous else 0,
                            state=1 if item_testSet.state else 0,
                            uid_id=userId,
                            is_del=0,
                            onlyCode=onlyCode
                        )
                        # region 请求基本数据
                        headers = item_testSet.request.headers
                        params = item_testSet.request.params
                        bodyRequestSaveType = item_testSet.request.body.requestSaveType
                        bodyFormData = item_testSet.request.body.formData
                        bodyRawValue = item_testSet.request.body.rawValue
                        bodyJsonValue = item_testSet.request.body.jsonValue

                        extract = item_testSet.request.extract
                        validate = item_testSet.request.validate
                        preOperation = item_testSet.request.preOperation
                        rearOperation = item_testSet.request.rearOperation

                        requestParamsType = cls_RequstOperation.for_data_get_requset_params_type(
                            params, bodyFormData, bodyRawValue, bodyJsonValue
                        )
                        db_CaseApiBase.objects.create(
                            testSet_id=save_db_CaseTestSet.id,
                            requestType=item_testSet.request.requestType,
                            requestUrl=item_testSet.request.requestUrl,
                            requestParamsType=requestParamsType,
                            bodyRequestSaveType=bodyRequestSaveType,
                            is_del=0,onlyCode=onlyCode
                        )
                        # endregion
                        # region Headers
                        product_list_to_insert = list()
                        for item_headers in headers:
                            product_list_to_insert.append(db_CaseApiHeaders(
                                testSet_id=save_db_CaseTestSet.id,
                                index=item_headers.index,
                                key=item_headers.key,
                                value=item_headers.value,
                                remarks=item_headers.remarks,
                                state=1 if item_headers.state else 0,
                                is_del=0,onlyCode=onlyCode)
                            )
                        db_CaseApiHeaders.objects.bulk_create(product_list_to_insert)
                        # endregion
                        # region Params
                        product_list_to_insert = list()
                        for item_params in params:
                            product_list_to_insert.append(db_CaseApiParams(
                                testSet_id=save_db_CaseTestSet.id,
                                index=item_params.index,
                                key=item_params.key,
                                value=item_params.value,
                                remarks=item_params.remarks,
                                state=1 if item_params.state else 0,
                                is_del=0,onlyCode=onlyCode)
                            )
                        db_CaseApiParams.objects.bulk_create(product_list_to_insert)
                        # endregion
                        # region Body
                        # region 删除多次上传的一些不需要的文件
                        deleteFileList = item_testSet.request.body.deleteFileList
                        for item_delFile in deleteFileList:
                            if item_delFile.dirName == 'Temp':
                                filePath = settings.TEMP_PATH
                            else:
                                filePath = f"{settings.APIFILE_PATH}{item_delFile.dirName}/"
                            cls_FileOperations.delete_file(f"{filePath}{item_delFile.fileName}")
                        # endregion
                        if bodyRequestSaveType == 'form-data':
                            product_list_to_insert = list()
                            for item_body in bodyFormData:
                                paramsType = item_body.paramsType
                                if paramsType == 'Text':
                                    filePath = None
                                else:  # file
                                    # region file文件处理
                                    filePath = None
                                    fileData = item_body.fileList[0]._object_maker__data
                                    fileName = fileData['name']
                                    fileUrl = fileData['url']

                                    tempUrl = fileUrl.replace(
                                        settings.NGINX_SERVER, f"{settings.BASE_DIR._str}/_DataFiles/")
                                    dirType = 'Temp' if 'Temp' in tempUrl else 'Case'
                                    if dirType == 'Temp':  # 移动文件
                                        # 创建文件夹
                                        newFolder = cls_FileOperations.new_folder(
                                            f'{settings.CASEFILE_PATH}{save_db_CaseTestSet.id}')
                                        if newFolder['state']:
                                            # 复制文件从临时目录到接口目录
                                            copyFile = cls_FileOperations.copy_file_to_dir(
                                                f'{settings.TEMP_PATH}{fileName}', newFolder['path'])
                                            if copyFile['state']:
                                                filePath = copyFile['newFilePath']
                                            else:
                                                response['errorMsg'] = copyFile['errorMsg']
                                                # 删除新增的文件夹
                                                cls_FileOperations.delete_folder(newFolder['path'])
                                                raise FileExistsError(copyFile['errorMsg'])
                                        else:
                                            response['errorMsg'] = newFolder['errorMsg']
                                            raise FileExistsError(newFolder['errorMsg'])
                                    else:  # 改写文件夹名称为新的TestSetId
                                        is_flie = cls_FileOperations.is_flie(tempUrl)
                                        if is_flie:
                                            oldTestSetId = tempUrl.split('/')[-2]
                                            oldPath = f"{settings.CASEFILE_PATH}{basicInfo.caseId}/{oldTestSetId}"
                                            newPath = f"{settings.CASEFILE_PATH}{basicInfo.caseId}/{save_db_CaseTestSet.id}"
                                            renameDir = cls_FileOperations.rename_dir(oldPath, newPath)
                                            if renameDir['state']:
                                                filePath = f"{renameDir['newPath']}/{fileName}"
                                            else:
                                                raise FileExistsError('用例步骤上传修改文件目录失败,请删除该用例后重新录制!')
                                        else:
                                            raise FileExistsError('用例步骤上传文件缺失,请删除该用例后重新录制!')
                                    # endregion
                                product_list_to_insert.append(db_CaseApiBody(
                                    testSet_id=save_db_CaseTestSet.id,
                                    index=item_body.index,
                                    key=item_body.key,
                                    paramsType=item_body.paramsType,
                                    value=item_body.value,
                                    filePath=filePath,
                                    remarks=item_body.remarks,
                                    state=1 if item_body.state else 0,
                                    is_del=0,onlyCode=onlyCode)
                                )
                            db_CaseApiBody.objects.bulk_create(product_list_to_insert)
                        elif bodyRequestSaveType in ['raw', 'json']:
                            if bodyRequestSaveType == 'raw':
                                value = item_testSet.request.body.rawValue
                            elif bodyRequestSaveType == 'json':
                                value = item_testSet.request.body.jsonValue
                            else:
                                value = None
                            db_CaseApiBody.objects.create(
                                testSet_id=save_db_CaseTestSet.id,
                                index=0,
                                key=None,
                                value=value,
                                state=1,
                                is_del=0,onlyCode=onlyCode
                            )
                        # endregion
                        # region Extract
                        product_list_to_insert = list()
                        for item_extract in extract:
                            product_list_to_insert.append(db_CaseApiExtract(
                                testSet_id=save_db_CaseTestSet.id,
                                index=item_extract.index,
                                key=item_extract.key,
                                value=item_extract.value,
                                remarks=item_extract.remarks,
                                state=1 if item_extract.state else 0,
                                is_del=0,onlyCode=onlyCode )
                            )
                        db_CaseApiExtract.objects.bulk_create(product_list_to_insert)
                        # endregion
                        # region Validate
                        product_list_to_insert = list()
                        for item_validate in validate:
                            product_list_to_insert.append(db_CaseApiValidate(
                                testSet_id=save_db_CaseTestSet.id,
                                index=item_validate.index,
                                checkName=item_validate.checkName,
                                validateType=item_validate.validateType,
                                valueType=item_validate.valueType,
                                expectedResults=item_validate.expectedResults,
                                remarks=item_validate.remarks,
                                state=1 if item_validate.state else 0,
                                is_del=0,onlyCode=onlyCode)
                            )
                        db_CaseApiValidate.objects.bulk_create(product_list_to_insert)
                        # endregion
                        # region 前置
                        product_list_to_insert = list()
                        for item_preOperation in preOperation:
                            product_list_to_insert.append(db_CaseApiOperation(
                                testSet_id=save_db_CaseTestSet.id,
                                index=item_preOperation.index,
                                location='Pre',
                                operationType=item_preOperation.operationType,
                                methodsName=item_preOperation.methodsName,
                                dataBaseId=item_preOperation.dataBase,
                                sql=item_preOperation.sql,
                                remarks=item_preOperation.remarks,
                                state=1 if item_preOperation.state else 0,
                                is_del=0,onlyCode=onlyCode)
                            )
                        db_CaseApiOperation.objects.bulk_create(product_list_to_insert)
                        # endregion
                        # region 后置
                        product_list_to_insert = list()
                        for item_rearOperation in rearOperation:
                            product_list_to_insert.append(db_CaseApiOperation(
                                testSet_id=save_db_CaseTestSet.id,
                                index=item_rearOperation.index,
                                location='Rear',
                                operationType=item_rearOperation.operationType,
                                methodsName=item_rearOperation.methodsName,
                                dataBaseId=item_rearOperation.dataBase,
                                sql=item_rearOperation.sql,
                                remarks=item_rearOperation.remarks,
                                state=1 if item_rearOperation.state else 0,
                                is_del=0,onlyCode=onlyCode)
                            )
                        db_CaseApiOperation.objects.bulk_create(product_list_to_insert)
                        # endregion
                    # endregion
                    # region 更新接口动态表为无更变
                    db_ApiDynamic.objects.filter(is_del=0, case_id=basicInfo.caseId).update(
                        updateTime=cls_Common.get_date_time(), is_read=1, uid_id=userId
                    )
                    # endregion
            except BaseException as e:  # 自动回滚，不需要任何操作
                response['errorMsg'] = f'保存失败:{e}'
            else:
                response['statusCode'] = 2002
        else:
            response['errorMsg'] = '未找到当前测试用例,请刷新后在重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def delete_data(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        caseId = request.POST['caseId']
        onlyCode = cls_Common.generate_only_code()
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_CaseMaintenance', 'delete_data', errorMsg)
    else:
        obj_db_CaseBaseData = db_CaseBaseData.objects.filter(id=caseId)
        if obj_db_CaseBaseData.exists():
            obj_db_ApiTimingTaskTestSet = db_ApiTimingTaskTestSet.objects.filter(is_del=0, case_id=caseId)
            if obj_db_ApiTimingTaskTestSet.exists():
                taskName = obj_db_ApiTimingTaskTestSet[0].timingTask.taskName
                response['errorMsg'] = f'当前用例已被定时任务:{taskName},绑定!请解除绑定后在进行删除操作!'
            else:
                try:
                    with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                        # region 历史恢复
                        db_ApiCaseHistory.objects.create(
                            pid_id=obj_db_CaseBaseData[0].pid_id,
                            page_id=obj_db_CaseBaseData[0].page_id,
                            fun_id=obj_db_CaseBaseData[0].fun_id,
                            case_id=caseId,
                            caseName=obj_db_CaseBaseData[0].caseName,
                            onlyCode=onlyCode,
                            operationType='Delete',
                            uid_id=userId
                        )
                        # endregion
                        # region 删除关联信息
                        obj_db_CaseTestSet = db_CaseTestSet.objects.filter(is_del=0, caseId_id=caseId)
                        for item_testSet in obj_db_CaseTestSet:
                            db_CaseApiBase.objects.filter(is_del=0, testSet_id=item_testSet.id).update(
                                is_del=1, updateTime=cls_Common.get_date_time()
                            )
                            db_CaseApiHeaders.objects.filter(is_del=0, testSet_id=item_testSet.id).update(
                                is_del=1, updateTime=cls_Common.get_date_time()
                            )
                            db_CaseApiParams.objects.filter(is_del=0, testSet_id=item_testSet.id).update(
                                is_del=1, updateTime=cls_Common.get_date_time()
                            )
                            db_CaseApiBody.objects.filter(is_del=0, testSet_id=item_testSet.id).update(
                                is_del=1, updateTime=cls_Common.get_date_time()
                            )
                            db_CaseApiExtract.objects.filter(is_del=0, testSet_id=item_testSet.id).update(
                                is_del=1, updateTime=cls_Common.get_date_time()
                            )
                            db_CaseApiValidate.objects.filter(is_del=0, testSet_id=item_testSet.id).update(
                                is_del=1, updateTime=cls_Common.get_date_time()
                            )
                            db_CaseApiOperation.objects.filter(is_del=0, testSet_id=item_testSet.id).update(
                                is_del=1, updateTime=cls_Common.get_date_time()
                            )
                        obj_db_CaseTestSet.update(
                            is_del=1, updateTime=cls_Common.get_date_time(), uid_id=userId)
                        obj_db_CaseBaseData.update(
                            is_del=1, updateTime=cls_Common.get_date_time(), uid_id=userId,onlyCode=onlyCode)
                        db_ApiDynamic.objects.filter(is_del=0, case_id=caseId).update(
                            is_del=1, updateTime=cls_Common.get_date_time(), uid_id=userId)
                        # endregion
                        # region 移动File文件到历史目录中 先判断有没有此用例的文件夹
                        sourcePath = f"{settings.CASEFILE_PATH}{caseId}"
                        targetPath = f"{settings.BAKDATA_PATH}CaseFile/{caseId}"
                        is_folder = cls_FileOperations.is_folder(sourcePath)
                        if is_folder:
                            newFolder = cls_FileOperations.new_folder(targetPath)
                            if newFolder['state']:
                                copy_dir = cls_FileOperations.copy_dir(sourcePath, targetPath)
                                if copy_dir['state']:
                                    cls_FileOperations.delete_folder(sourcePath)
                                else:
                                    raise FileExistsError(copy_dir['errorMsg'])
                            else:
                                raise FileExistsError(newFolder['errorMsg'])
                        # endregion
                        # region 添加操作信息
                        cls_Logging.record_operation_info(
                            'API', 'Manual', 3, 'Delete',
                            cls_FindTable.get_pro_name(obj_db_CaseBaseData[0].pid_id),
                            cls_FindTable.get_page_name(obj_db_CaseBaseData[0].page_id),
                            cls_FindTable.get_fun_name(obj_db_CaseBaseData[0].fun_id),
                            userId,
                            f'【删除用例】 ID:{caseId}:{obj_db_CaseBaseData[0].caseName}',
                            CUFront=json.dumps(request.POST)
                        )
                        # endregion
                except BaseException as e:  # 自动回滚，不需要任何操作
                    response['errorMsg'] = f'数据删除失败:{e}'
                else:
                    response['statusCode'] = 2003
        else:
            response['errorMsg'] = '未找到当前用例数据,请刷新后重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def load_case_data(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        caseId = objData.caseId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_CaseMaintenance', 'load_data', errorMsg)
    else:
        obj_db_CaseBaseData = db_CaseBaseData.objects.filter(is_del=0, id=caseId)
        if obj_db_CaseBaseData.exists():
            # region 基础信息
            basicInfo = {
                'pageId': obj_db_CaseBaseData[0].page_id,
                'funId': obj_db_CaseBaseData[0].fun_id,
                'environmentId': obj_db_CaseBaseData[0].environmentId_id,
                'testType': obj_db_CaseBaseData[0].testType,
                'labelId': obj_db_CaseBaseData[0].label,
                'priorityId': obj_db_CaseBaseData[0].priority,
                'caseName': obj_db_CaseBaseData[0].caseName,
                'caseState': obj_db_CaseBaseData[0].caseState,
            }
            # endregion
            # region 测试集
            testSet = []
            obj_db_CaseTestSet = db_CaseTestSet.objects.filter(is_del=0, caseId_id=caseId)
            for item_testSet in obj_db_CaseTestSet:
                settingParams = False
                synchronous = True if item_testSet.is_synchronous == 1 else False
                requestData = {
                    'requestType': 'GET',
                    'requestUrl': '',
                    'headers': [],
                    'params': [],
                    'body': {
                        'requestSaveType': 'form-data',
                        'formData': [],
                        'rawValue': '',
                        'jsonValue': '',
                        'deleteFileList': [],
                    },
                    'extract': [],
                    'validate': [],
                    'preOperation': [],
                    'rearOperation': [],
                }
                obj_db_CaseApiBase = db_CaseApiBase.objects.filter(is_del=0, testSet_id=item_testSet.id)
                if obj_db_CaseApiBase.exists():
                    requestData['requestType'] = obj_db_CaseApiBase[0].requestType
                    requestData['requestUrl'] = obj_db_CaseApiBase[0].requestUrl
                    requestData['body']['requestSaveType'] = obj_db_CaseApiBase[0].bodyRequestSaveType
                    if obj_db_CaseApiBase[0].requestUrl:
                        settingParams = True
                    # region headers
                    obj_db_CaseApiHeaders = db_CaseApiHeaders.objects.filter(
                        is_del=0, testSet_id=item_testSet.id).order_by('index')
                    for item_headers in obj_db_CaseApiHeaders:
                        requestData['headers'].append({
                            'index': item_headers.index,
                            'state': True if item_headers.state == 1 else False,
                            'key': item_headers.key,
                            'value': item_headers.value,
                            'remarks': item_headers.remarks,
                        })
                    # endregion
                    # region params
                    obj_db_CaseApiParams = db_CaseApiParams.objects.filter(
                        is_del=0, testSet_id=item_testSet.id).order_by('index')
                    for item_params in obj_db_CaseApiParams:
                        requestData['params'].append({
                            'index': item_params.index,
                            'state': True if item_params.state == 1 else False,
                            'key': item_params.key,
                            'value': item_params.value,
                            'remarks': item_params.remarks,
                        })
                    # endregion
                    # region body
                    obj_db_CaseApiBody = db_CaseApiBody.objects.filter(
                        is_del=0, testSet_id=item_testSet.id).order_by('index')
                    if obj_db_CaseApiBase[0].bodyRequestSaveType == 'form-data':
                        for item_body in obj_db_CaseApiBody:
                            if item_body.paramsType == 'Text':
                                fileList = []
                            else:
                                splitStr = item_body.filePath.split('/')
                                name = splitStr[-1]
                                url = f"{settings.NGINX_SERVER}CaseFile/{caseId}/{item_testSet.id}/{name}"
                                fileList = [
                                    {'name': name, 'url': url}
                                ]
                            requestData['body']['formData'].append({
                                'index': item_body.index,
                                'state': True if item_body.state == 1 else False,
                                'key': item_body.key,
                                'paramsType': item_body.paramsType,
                                'value': item_body.value,
                                'fileList': fileList,
                                'remarks': item_body.remarks,
                            })
                    elif obj_db_CaseApiBase[0].bodyRequestSaveType == 'raw':
                        requestData['body']['rawValue'] = obj_db_CaseApiBody[0].value
                    elif obj_db_CaseApiBase[0].bodyRequestSaveType == 'json':
                        requestData['body']['jsonValue'] = obj_db_CaseApiBody[0].value
                    # endregion
                    # region Extract
                    obj_db_CaseApiExtract = db_CaseApiExtract.objects.filter(
                        is_del=0, testSet_id=item_testSet.id).order_by('index')
                    for item_extract in obj_db_CaseApiExtract:
                        requestData['extract'].append({
                            'index': item_extract.index,
                            'state': True if item_extract.state == 1 else False,
                            'key': item_extract.key,
                            'value': item_extract.value,
                            'remarks': item_extract.remarks,
                        })
                    # endregion
                    # region Validate
                    obj_db_CaseApiValidate = db_CaseApiValidate.objects.filter(
                        is_del=0, testSet_id=item_testSet.id).order_by('index')
                    for item_validate in obj_db_CaseApiValidate:
                        requestData['validate'].append({
                            'index': item_validate.index,
                            'state': True if item_validate.state == 1 else False,
                            'checkName': item_validate.checkName,
                            'validateType': item_validate.validateType,
                            'valueType': item_validate.valueType,
                            'expectedResults': item_validate.expectedResults,
                            'remarks': item_validate.remarks,
                        })
                    # endregion
                    # region 前置操作
                    obj_db_CaseApiOperation = db_CaseApiOperation.objects.filter(
                        is_del=0, testSet_id=item_testSet.id, location='Pre').order_by('index')
                    for item_preOperation in obj_db_CaseApiOperation:
                        if item_preOperation.dataBaseId:
                            dataBase = ast.literal_eval(item_preOperation.dataBaseId)
                        else:
                            dataBase = []
                        requestData['preOperation'].append({
                            'id': item_preOperation.index,
                            'index': item_preOperation.index,
                            'state': True if item_preOperation.state == 1 else False,
                            'operationType': item_preOperation.operationType,
                            'methodsName': item_preOperation.methodsName,
                            'dataBase': dataBase,
                            'sql': item_preOperation.sql,
                            'remarks': item_preOperation.remarks,
                        })
                    # endregion
                    # region 后置操作
                    obj_db_CaseApiOperation = db_CaseApiOperation.objects.filter(
                        is_del=0, testSet_id=item_testSet.id, location='Rear').order_by('index')
                    for item_rearOperation in obj_db_CaseApiOperation:
                        if item_rearOperation.dataBaseId:
                            dataBase = ast.literal_eval(item_rearOperation.dataBaseId)
                        else:
                            dataBase = []
                        requestData['rearOperation'].append({
                            'id': item_rearOperation.index,
                            'index': item_rearOperation.index,
                            'state': True if item_rearOperation.state == 1 else False,
                            'operationType': item_rearOperation.operationType,
                            'methodsName': item_rearOperation.methodsName,
                            'dataBase': dataBase,
                            'sql': item_rearOperation.sql,
                            'remarks': item_rearOperation.remarks,
                        })
                    # endregion
                obj_db_ApiDynamic = db_ApiDynamic.objects.filter(
                    case_id=caseId, apiId_id=item_testSet.apiId_id, is_del=0, is_read=0)
                # 0 无更变、1 已更变、2 已知晓
                if obj_db_ApiDynamic.exists():
                    if synchronous:  # 只对开启同步功能的接口 提示接口动态，未开始同步的接口因为是独立的参数可不提醒
                        apidynamic = 1
                    else:
                        apidynamic = 0
                else:
                    apidynamic = 0
                testSet.append({
                    'id': item_testSet.pluralIntId,
                    'apiId': item_testSet.apiId_id,
                    'state': True if item_testSet.state == 1 else False,
                    'apiName': item_testSet.apiId.apiName,
                    'apiState': item_testSet.apiId.apiState,
                    'testName': item_testSet.testName,
                    'is_synchronous': synchronous,
                    'settingParams': settingParams,
                    'apidynamic': apidynamic,
                    'request': requestData,
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
@require_http_methods(["POST"])  # 执行用例
def execute_case(request):
    response = {
        'leftData': {},
        'rightData': {},
    }
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        runType = request.POST['runType']
        caseId = request.POST['caseId']
        environmentId = request.POST['environmentId']
        redisKey = cls_Common.generate_only_code()
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_CaseMaintenance', 'execute_case', errorMsg)
    else:
        obj_db_CaseBaseData = db_CaseBaseData.objects.filter(is_del=0, id=caseId)
        if obj_db_CaseBaseData.exists():
            remindLabel = f"【用例:{obj_db_CaseBaseData[0].caseName}】:"  # 推送的标识
            queueState = cls_FindTable.get_queue_state('CASE', caseId)
            if queueState:
                response['errorMsg'] = '当前已有相同用例在运行,不可重复运行!您可在主页中项目里查看此用例的动态!' \
                                       '如遇错误可取消该项目队列后重新运行!'
            else:
                # region 获取TopData
                preOperationTotal = 0  # 前置总数
                rearOperationTotal = 0  # 后置总数
                extractTotal = 0  # 提取总数
                assertionsTotal = 0  # 断言总数

                obj_db_CaseTestSet = db_CaseTestSet.objects.filter(is_del=0, caseId_id=caseId)
                failedTotal = obj_db_CaseTestSet.filter(state=1).count()
                response['leftData']['failedTotal'] = failedTotal
                for item_testSet in obj_db_CaseTestSet:
                    state = True if item_testSet.state == 1 else False
                    if state:
                        obj_db_CaseApiOperation = db_CaseApiOperation.objects.filter(is_del=0,
                                                                                     testSet_id=item_testSet.id)
                        preOperationTotal += obj_db_CaseApiOperation.filter(location='Pre').count()
                        rearOperationTotal += obj_db_CaseApiOperation.filter(location='Rear').count()

                        obj_db_CaseApiExtract = db_CaseApiExtract.objects.filter(is_del=0, testSet_id=item_testSet.id)
                        extractTotal += obj_db_CaseApiExtract.count()

                        obj_db_CaseApiValidate = db_CaseApiValidate.objects.filter(is_del=0, testSet_id=item_testSet.id)
                        assertionsTotal += obj_db_CaseApiValidate.count()
                response['rightData']['preOperationTotal'] = preOperationTotal
                response['rightData']['rearOperationTotal'] = rearOperationTotal
                response['rightData']['extractTotal'] = extractTotal
                response['rightData']['assertionsTotal'] = assertionsTotal
                # endregion
                # region 创建1级主报告
                createTestReport = cls_ApiReport.create_test_report(
                    obj_db_CaseBaseData[0].pid_id,
                    obj_db_CaseBaseData[0].caseName,
                    'CASE', caseId, failedTotal, userId
                )
                # endregion
                if createTestReport['state']:
                    testReportId = createTestReport['testReportId']
                    # region 创建队列
                    queueId = cls_ApiReport.create_queue(
                        obj_db_CaseBaseData[0].pid_id, obj_db_CaseBaseData[0].page_id, obj_db_CaseBaseData[0].fun_id
                        , 'CASE', caseId, testReportId, userId)  # 创建队列
                    # endregion
                    result = api_asynchronous_run_case.delay(remindLabel, redisKey, testReportId, queueId, caseId,
                                                             environmentId, userId)
                    if result.task_id:
                        response['statusCode'] = 2001
                        response['redisKey'] = redisKey
                else:
                    response['errorMsg'] = f'创建主测试报告失败:{createTestReport["errorMsg"]}'
        else:
            response['errorMsg'] = '当前选择的用例不存在,请刷新后在重新尝试'
    return JsonResponse(response)


@accept_websocket  # 读取redis数据
def read_case_result(request):
    counter = 0  # 计数器 到100就会断开通信
    if request.is_websocket():
        retMessage = str(request.websocket.wait(), 'utf-8')  # 接受前段发送来的数据
        if retMessage:
            objData = cls_object_maker(json.loads(retMessage))
            redisKey = objData.Params.redisKey
            if objData.Message == "Start":  # 开始执行
                while True:
                    try:
                        retMessage = request.websocket.read()
                    except BaseException as e:
                        cls_Logging.print_log('error', 'get_server_indicators', f'前端已关闭,断开连接:{e}')
                        break
                    else:
                        readTypeList = cls_RedisHandle.read_type_list(redisKey)
                        if readTypeList:
                            request.websocket.send(json.dumps(readTypeList, ensure_ascii=False).encode('utf-8'))

                        if retMessage:
                            objData = cls_object_maker(json.loads(retMessage))
                            if objData.Message == 'Heartbeat':
                                counter = 0
                        else:
                            counter += 1
                            # 这里的时间 需要在调试的时候改！
                            if counter >= 324:
                                request.websocket.close()
                                cls_Logging.print_log('error', 'read_case_result', f'心跳包:{counter}秒内无响应,断开连接')
                                break
                        sleep(0.1)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def copy_case(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        caseId = objData.caseId
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_CaseMaintenance', 'copy_case', errorMsg)
    else:
        obj_db_CaseBaseData = db_CaseBaseData.objects.filter(is_del=0, id=caseId)
        if obj_db_CaseBaseData.exists():
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    # region 基本信息
                    save_db_CaseBaseData = db_CaseBaseData.objects.create(
                        pid_id=obj_db_CaseBaseData[0].pid_id,
                        page_id=obj_db_CaseBaseData[0].page_id,
                        fun_id=obj_db_CaseBaseData[0].fun_id,
                        environmentId_id=obj_db_CaseBaseData[0].environmentId_id,
                        testType=obj_db_CaseBaseData[0].testType,
                        label=obj_db_CaseBaseData[0].label,
                        priority=obj_db_CaseBaseData[0].priority,
                        caseName=f"副本-{obj_db_CaseBaseData[0].caseName}",
                        caseState=obj_db_CaseBaseData[0].caseState,
                        cuid=userId,
                        uid_id=userId,
                        is_del=0
                    )
                    # endregion
                    # region 测试集
                    obj_db_CaseTestSet = db_CaseTestSet.objects.filter(is_del=0, caseId_id=caseId)
                    for item_testSet in obj_db_CaseTestSet:
                        # region TestSet
                        save_db_CaseTestSet = db_CaseTestSet.objects.create(
                            caseId_id=save_db_CaseBaseData.id,
                            index=item_testSet.index,
                            apiId_id=item_testSet.apiId_id,
                            pluralIntId=item_testSet.pluralIntId,
                            testName=item_testSet.testName,
                            is_synchronous=item_testSet.is_synchronous,
                            state=item_testSet.state,
                            uid_id=userId,
                            is_del=0,
                        )
                        # endregion
                        # region ApiBase
                        obj_db_CaseApiBase = db_CaseApiBase.objects.filter(is_del=0, testSet_id=item_testSet.id)
                        product_list_to_insert = list()
                        for item_apiBase in obj_db_CaseApiBase:
                            product_list_to_insert.append(db_CaseApiBase(
                                testSet_id=save_db_CaseTestSet.id,
                                requestType=item_apiBase.requestType,
                                requestUrl=item_apiBase.requestUrl,
                                requestParamsType=item_apiBase.requestParamsType,
                                bodyRequestSaveType=item_apiBase.bodyRequestSaveType,
                                is_del=0,
                            ))
                        db_CaseApiBase.objects.bulk_create(product_list_to_insert)
                        # endregion
                        # region Header
                        obj_db_CaseApiHeaders = db_CaseApiHeaders.objects.filter(is_del=0, testSet_id=item_testSet.id)
                        product_list_to_insert = list()
                        for item_headers in obj_db_CaseApiHeaders:
                            product_list_to_insert.append(db_CaseApiHeaders(
                                testSet_id=save_db_CaseTestSet.id,
                                index=item_headers.index,
                                key=item_headers.key,
                                value=item_headers.value,
                                remarks=item_headers.remarks,
                                state=item_headers.state,
                                is_del=0,
                            ))
                        db_CaseApiHeaders.objects.bulk_create(product_list_to_insert)
                        # endregion
                        # region params
                        obj_db_CaseApiParams = db_CaseApiParams.objects.filter(is_del=0, testSet_id=item_testSet.id)
                        product_list_to_insert = list()
                        for item_params in obj_db_CaseApiParams:
                            product_list_to_insert.append(db_CaseApiParams(
                                testSet_id=save_db_CaseTestSet.id,
                                index=item_params.index,
                                key=item_params.key,
                                value=item_params.value,
                                remarks=item_params.remarks,
                                state=item_params.state,
                                is_del=0,
                            ))
                        db_CaseApiParams.objects.bulk_create(product_list_to_insert)
                        # endregion
                        # region body
                        obj_db_CaseApiBody = db_CaseApiBody.objects.filter(is_del=0, testSet_id=item_testSet.id)
                        product_list_to_insert = list()
                        for item_body in obj_db_CaseApiBody:
                            paramsType = item_body.paramsType
                            if paramsType == "Text":
                                filePath = None
                            else:
                                # region file文件处理
                                fileData = item_body.filePath
                                # 创建文件夹
                                newFolder = cls_FileOperations.new_folder(
                                    f'{settings.CASEFILE_PATH}{save_db_CaseBaseData.id}/{save_db_CaseTestSet.id}')
                                if newFolder['state']:
                                    # 复制文件从临时目录到接口目录
                                    copyFile = cls_FileOperations.copy_file_to_dir(fileData, newFolder['path'])
                                    if copyFile['state']:
                                        filePath = copyFile['newFilePath']
                                    else:
                                        # 删除新增的文件夹
                                        cls_FileOperations.delete_folder(newFolder['path'])
                                        raise FileExistsError(copyFile['errorMsg'])
                                else:
                                    raise FileExistsError(newFolder['errorMsg'])
                                # endregion
                            product_list_to_insert.append(db_CaseApiBody(
                                testSet_id=save_db_CaseTestSet.id,
                                index=item_body.index,
                                key=item_body.key,
                                paramsType=paramsType,
                                value=item_body.value,
                                filePath=filePath,
                                remarks=item_body.remarks,
                                state=item_body.state,
                                is_del=0,
                            ))
                        db_CaseApiBody.objects.bulk_create(product_list_to_insert)
                        # endregion
                        # region 提取
                        obj_db_CaseApiExtract = db_CaseApiExtract.objects.filter(is_del=0, testSet_id=item_testSet.id)
                        product_list_to_insert = list()
                        for item_extract in obj_db_CaseApiExtract:
                            product_list_to_insert.append(db_CaseApiExtract(
                                testSet_id=save_db_CaseTestSet.id,
                                index=item_extract.index,
                                key=item_extract.key,
                                value=item_extract.value,
                                remarks=item_extract.remarks,
                                state=item_extract.state,
                                is_del=0,
                            ))
                        db_CaseApiExtract.objects.bulk_create(product_list_to_insert)
                        # endregion
                        # region 断言
                        obj_db_CaseApiValidate = db_CaseApiValidate.objects.filter(is_del=0, testSet_id=item_testSet.id)
                        product_list_to_insert = list()
                        for item_validate in obj_db_CaseApiValidate:
                            product_list_to_insert.append(db_CaseApiValidate(
                                testSet_id=save_db_CaseTestSet.id,
                                index=item_validate.index,
                                checkName=item_validate.checkName,
                                validateType=item_validate.validateType,
                                valueType=item_validate.valueType,
                                expectedResults=item_validate.expectedResults,
                                remarks=item_validate.remarks,
                                state=item_validate.state,
                                is_del=0,
                            ))
                        db_CaseApiValidate.objects.bulk_create(product_list_to_insert)
                        # endregion
                        # region 前后操作
                        obj_db_CaseApiOperation = db_CaseApiOperation.objects.filter(
                        is_del=0,testSet_id=item_testSet.id)
                        product_list_to_insert = list()
                        for item_operation in obj_db_CaseApiOperation:
                            product_list_to_insert.append(db_CaseApiOperation(
                                testSet_id=save_db_CaseTestSet.id,
                                index=item_operation.index,
                                location=item_operation.location,
                                operationType=item_operation.operationType,
                                methodsName=item_operation.methodsName,
                                dataBaseId=item_operation.dataBaseId,
                                sql=item_operation.sql,
                                remarks=item_operation.remarks,
                                state=item_operation.state,
                                is_del=0,
                            ))
                        db_CaseApiOperation.objects.bulk_create(product_list_to_insert)
                        # endregion
                    # endregion
            except BaseException as e:  # 自动回滚，不需要任何操作
                response['errorMsg'] = str(e)
            else:
                response['statusCode'] = 2000
        else:
            response['errorMsg'] = "当前选择的数据不存在,请刷新后在重新尝试!"
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

        caseId = objData.caseId
        pageId = objData.pageId
        funId = objData.funId
        caseName = objData.caseName
        operationType = objData.operationType

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_CaseMaintenance', 'select_history', errorMsg)
    else:
        if caseId:
            obj_db_ApiCaseHistory = db_ApiCaseHistory.objects.filter(case_id=caseId).order_by('-createTime')
        else:
            obj_db_ApiCaseHistory = db_ApiCaseHistory.objects.filter().order_by('-createTime')
            if pageId:
                obj_db_ApiCaseHistory = obj_db_ApiCaseHistory.filter(page_id=pageId).order_by('-createTime')
            if funId:
                obj_db_ApiCaseHistory = obj_db_ApiCaseHistory.filter(fun_id=funId).order_by('-createTime')
            if caseName:
                obj_db_ApiCaseHistory = obj_db_ApiCaseHistory.filter(
                    caseName__icontains=caseName).order_by('-createTime')
            if operationType:
                obj_db_ApiCaseHistory = obj_db_ApiCaseHistory.filter(
                    operationType=operationType).order_by('-createTime')
        select_obj_db_ApiCaseHistory = obj_db_ApiCaseHistory[minSize: maxSize]
        for i in select_obj_db_ApiCaseHistory:
            if i.restoreData:
                restoreData = json.dumps(
                    ast.literal_eval(i.restoreData),sort_keys=True, indent=4, separators=(",", ": "), ensure_ascii=False)
            else:
                restoreData = None
            if restoreData:
                tableItem = [{'restoreData': restoreData}]
            else:
                tableItem = []
            dataList.append({
                'id': i.id,
                'pageName': i.page.pageName,
                'funName': i.fun.funName,
                'caseName': i.caseName,
                'operationType': i.operationType,
                'tableItem': tableItem,
                'createTime': str(i.createTime.strftime('%Y-%m-%d %H:%M:%S')),
                "userName": f"{i.uid.userName}({i.uid.nickName})",
            })
        response['TableData'] = dataList
        response['Total'] = obj_db_ApiCaseHistory.count()
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
        historyId = request.POST['historyId']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_CaseMaintenance', 'restor_data', errorMsg)
    else:
        obj_db_ApiCaseHistory = db_ApiCaseHistory.objects.filter(id=historyId)
        if obj_db_ApiCaseHistory.exists():
            onlyCode = obj_db_ApiCaseHistory[0].onlyCode
            # 恢复时是管理员或是 当前项目的创建人时才可恢复
            if is_admin or obj_db_ApiCaseHistory[0].case.cuid == userId:
                try:
                    with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                        obj_db_ProManagement = db_ProManagement.objects.filter(
                            is_del=0, id=obj_db_ApiCaseHistory[0].pid_id)
                        if obj_db_ProManagement.exists():
                            obj_db_PageManagement = db_PageManagement.objects.filter(
                                is_del=0, id=obj_db_ApiCaseHistory[0].page_id)
                            if obj_db_PageManagement.exists():
                                obj_db_FunManagement = db_FunManagement.objects.filter(
                                    is_del=0, id=obj_db_ApiCaseHistory[0].fun_id)
                                if obj_db_FunManagement.exists():
                                    caseId = obj_db_ApiCaseHistory[0].case_id
                                    restoreData = obj_db_ApiCaseHistory[0].restoreData
                                    if obj_db_ApiCaseHistory[0].operationType in ["Add", "Edit"]:
                                        obj_db_CaseBaseData = db_CaseBaseData.objects.filter(id=caseId)
                                        if obj_db_CaseBaseData.exists():
                                            # region 操作记录
                                            cls_Logging.record_operation_info(
                                                'API', 'Manual', 3, 'Update',
                                                cls_FindTable.get_pro_name(obj_db_ApiCaseHistory[0].pid_id),
                                                cls_FindTable.get_page_name(obj_db_ApiCaseHistory[0].page_id),
                                                cls_FindTable.get_fun_name(obj_db_ApiCaseHistory[0].fun_id),
                                                userId,
                                                f'【恢复用例维护】 '
                                                f'ID:{obj_db_ApiCaseHistory[0].case_id}:'
                                                f"{obj_db_ApiCaseHistory[0].caseName}",
                                            )
                                            # endregion
                                            restoreData = ast.literal_eval(restoreData)
                                            # region 需要删除原附属数据，不会恢复时会出现原数据还在
                                            db_CaseTestSet.objects.filter(
                                                onlyCode=obj_db_CaseBaseData[0].onlyCode).update(
                                                is_del=1, updateTime=cls_Common.get_date_time())
                                            db_CaseApiBase.objects.filter(
                                                onlyCode=obj_db_CaseBaseData[0].onlyCode).update(
                                                is_del=1, updateTime=cls_Common.get_date_time())
                                            db_CaseApiHeaders.objects.filter(
                                                onlyCode=obj_db_CaseBaseData[0].onlyCode).update(
                                                is_del=1, updateTime=cls_Common.get_date_time())
                                            db_CaseApiParams.objects.filter(
                                                onlyCode=obj_db_CaseBaseData[0].onlyCode).update(
                                                is_del=1, updateTime=cls_Common.get_date_time())
                                            db_CaseApiBody.objects.filter(
                                                onlyCode=obj_db_CaseBaseData[0].onlyCode).update(
                                                is_del=1, updateTime=cls_Common.get_date_time())
                                            db_CaseApiExtract.objects.filter(
                                                onlyCode=obj_db_CaseBaseData[0].onlyCode).update(
                                                is_del=1, updateTime=cls_Common.get_date_time())
                                            db_CaseApiValidate.objects.filter(
                                                onlyCode=obj_db_CaseBaseData[0].onlyCode).update(
                                                is_del=1, updateTime=cls_Common.get_date_time())
                                            db_CaseApiOperation.objects.filter(
                                                onlyCode=obj_db_CaseBaseData[0].onlyCode).update(
                                                is_del=1, updateTime=cls_Common.get_date_time())
                                            # endregion
                                            # region 基础数据
                                            obj_db_CaseBaseData.update(
                                                pid_id=restoreData['BasicInfo']['proId'],
                                                page_id=restoreData['BasicInfo']['pageId'],
                                                fun_id=restoreData['BasicInfo']['funId'],
                                                environmentId_id=restoreData['BasicInfo']['environmentId'],
                                                testType=restoreData['BasicInfo']['testType'],
                                                label=restoreData['BasicInfo']['labelId'],
                                                priority=restoreData['BasicInfo']['priorityId'],
                                                caseName=restoreData['BasicInfo']['caseName'],
                                                caseState=restoreData['BasicInfo']['caseState'],
                                                createTime=restoreData['BasicInfo']['createTime'],
                                                updateTime=restoreData['BasicInfo']['updateTime'],
                                                cuid=restoreData['BasicInfo']['cuid'],
                                                uid_id=restoreData['BasicInfo']['uid_id'],
                                                is_del=0,
                                                onlyCode=restoreData['onlyCode'],
                                            )
                                            # endregion
                                            obj_db_CaseTestSet = db_CaseTestSet.objects.filter(onlyCode=onlyCode)
                                            obj_db_CaseTestSet.update(is_del=0)
                                            for item_testSet in obj_db_CaseTestSet:
                                                db_CaseApiBase.objects.filter(
                                                    is_del=1,testSet_id=item_testSet.id,onlyCode=onlyCode).update(
                                                    is_del=0)
                                                db_CaseApiHeaders.objects.filter(
                                                    is_del=1,testSet_id=item_testSet.id,onlyCode=onlyCode).update(
                                                    is_del=0)
                                                db_CaseApiParams.objects.filter(
                                                    is_del=1, testSet_id=item_testSet.id, onlyCode=onlyCode).update(
                                                    is_del=0)
                                                db_CaseApiBody.objects.filter(
                                                    is_del=1, testSet_id=item_testSet.id, onlyCode=onlyCode).update(
                                                    is_del=0,filePath=None) # 用例的FILE文件恢复时直接清空
                                                db_CaseApiExtract.objects.filter(
                                                    is_del=1, testSet_id=item_testSet.id, onlyCode=onlyCode).update(
                                                    is_del=0)
                                                db_CaseApiValidate.objects.filter(
                                                    is_del=1, testSet_id=item_testSet.id, onlyCode=onlyCode).update(
                                                    is_del=0)
                                                db_CaseApiOperation.objects.filter(
                                                    is_del=1, testSet_id=item_testSet.id, onlyCode=onlyCode).update(
                                                    is_del=0)
                                        else:
                                            raise ValueError('此数据原始数据在库中无法查询到!')
                                    else:
                                        raise ValueError('使用了未录入的操作类型!')
                                else:
                                    raise ValueError(f"当前恢复的数据上级所属功能不存在,恢复失败!")
                            else:
                                raise ValueError(f"当前恢复的数据上级所属页面不存在,恢复失败!")
                        else:
                            raise ValueError(f"当前恢复的数据上级所属项目不存在,恢复失败!")
                except BaseException as e:  # 自动回滚，不需要任何操作
                    response['errorMsg'] = f"数据恢复失败:{e}"
                else:
                    response['statusCode'] = 2002
            else:
                response['errorMsg'] = "您没有权限进行此操作,请联系项目的创建者或是管理员!"
        else:
            response['errorMsg'] = "当前选择的恢复数据不存在,请刷新后重新尝试!"
    return JsonResponse(response)
