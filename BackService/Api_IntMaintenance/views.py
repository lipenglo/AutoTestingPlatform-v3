from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction

import json

# Create your db here.
from login.models import UserTable as db_UserTable
from Api_IntMaintenance.models import ApiBaseData as db_ApiBaseData
from Api_IntMaintenance.models import ApiHeaders as db_ApiHeaders
from Api_IntMaintenance.models import ApiParams as db_ApiParams
from Api_IntMaintenance.models import ApiBody as db_ApiBody
from Api_IntMaintenance.models import ApiExtract as db_ApiExtract
from Api_IntMaintenance.models import ApiValidate as db_ApiValidate
from Api_IntMaintenance.models import ApiOperation as db_ApiOperation
from Api_IntMaintenance.models import ApiAssociatedUser as db_ApiAssociatedUser
from WorkorderManagement.models import WorkorderManagement as db_WorkorderManagement
from WorkorderManagement.models import WorkBindPushToUsers as db_WorkBindPushToUsers
from WorkorderManagement.models import WorkLifeCycle as db_WorkLifeCycle

# Create reference here.
from ClassData.Logger import Logging
from ClassData.GlobalDecorator import GlobalDer
from ClassData.FindCommonTable import FindTable
from ClassData.Common import Common
from ClassData.ImageProcessing import ImageProcessing
from ClassData.ObjectMaker import object_maker as cls_object_maker
from ClassData.Request import RequstOperation

# Create info here.
cls_Logging = Logging()
cls_GlobalDer = GlobalDer()
cls_FindTable = FindTable()
cls_Common = Common()
cls_ImageProcessing = ImageProcessing()
cls_RequstOperation = RequstOperation()


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
        apiName = objData.apiName
        requestUrl = objData.requestUrl
        apiState = objData.apiState
        associations= objData.associations
        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_IntMaintenance', 'select_data', errorMsg)
    else:
        obj_db_ApiBaseData = db_ApiBaseData.objects.filter(is_del=0, pid_id=proId).order_by('-updateTime')
        select_db_ApiBaseData = obj_db_ApiBaseData[minSize: maxSize]
        if pageId:
            obj_db_ApiBaseData = obj_db_ApiBaseData.filter(page_id=pageId)
            select_db_ApiBaseData = obj_db_ApiBaseData[minSize: maxSize]
        if funId:
            obj_db_ApiBaseData = obj_db_ApiBaseData.filter(fun_id=funId)
            select_db_ApiBaseData = obj_db_ApiBaseData[minSize: maxSize]
        if apiName:
            obj_db_ApiBaseData = obj_db_ApiBaseData.filter(apiName__icontains=apiName)
            select_db_ApiBaseData = obj_db_ApiBaseData[minSize: maxSize]
        if requestUrl:
            obj_db_ApiBaseData = obj_db_ApiBaseData.filter(requestUrl__icontains=requestUrl)
            select_db_ApiBaseData = obj_db_ApiBaseData[minSize: maxSize]
        if apiState:
            obj_db_ApiBaseData = obj_db_ApiBaseData.filter(apiState=apiState)
            select_db_ApiBaseData = obj_db_ApiBaseData[minSize: maxSize]

        for i in select_db_ApiBaseData:
            obj_db_ApiAssociatedUser = db_ApiAssociatedUser.objects.filter(is_del=0,apiId_id=i.id,uid_id=userId)
            if obj_db_ApiAssociatedUser:
                associationMy = True
            else:
                associationMy = False
            if associations == 'My':
                if associationMy:
                    dataList.append({
                        'id': i.id,
                        'pageName': i.page.pageName,
                        'funName': i.fun.funName,
                        'apiName': i.apiName,
                        'requestType': i.requestType,
                        'requestUrl': i.requestUrl,
                        'apiState': i.apiState,
                        'associationMy':associationMy,
                        'updateTime': str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                        'userName': i.uid.userName
                    })
            else:
                dataList.append({
                    'id': i.id,
                    'pageName': i.page.pageName,
                    'funName': i.fun.funName,
                    'apiName': i.apiName,
                    'requestType': i.requestType,
                    'requestUrl': i.requestUrl,
                    'apiState': i.apiState,
                    'associationMy': associationMy,
                    'updateTime': str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                    'userName': i.uid.userName
                })
        response['TableData'] = dataList
        response['Total'] = obj_db_ApiBaseData.count()
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 效验接口数据的完成性
def charm_api_data(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(request.body)
        objData = cls_object_maker(responseData)
        charmType = objData.CharmType  # true 新增，false 修改
        basicInfo = objData.BasicInfo
        apiInfo = objData.ApiInfo
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_IntMaintenance', 'charm_api_data', errorMsg)
    else:
        # region 验证 接口名称,请求类型,请求地址
        obj_db_ApiBaseData = db_ApiBaseData.objects.filter(
            is_del=0, pid_id=basicInfo.proId, page_id=basicInfo.pageId, fun_id=basicInfo.funId,
            apiName=basicInfo.apiName, requestType=apiInfo.requestType, requestUrl=apiInfo.requestUrl)
        if obj_db_ApiBaseData:
            if charmType:
                dataList.append({
                    'stepsName': '基本信息',
                    'errorMsg': '当前所属功能下已有相同接口名称,类型,请求地址,请更改!',
                    'updateTime': cls_Common.get_date_time()})
            else:
                if obj_db_ApiBaseData:
                    if basicInfo.apiId == obj_db_ApiBaseData[0].id:
                        pass
                    else:
                        dataList.append({
                            'stepsName': '基本信息',
                            'errorMsg': '当前所属功能下已有相同接口名称,类型,请求地址,请更改!',
                            'updateTime': cls_Common.get_date_time()})
        else:
            obj_db_ApiBaseData = db_ApiBaseData.objects.filter(
                is_del=0, pid_id=basicInfo.proId, page_id=basicInfo.pageId, fun_id=basicInfo.funId,
                apiName=basicInfo.apiName, requestType=apiInfo.requestType)
            if obj_db_ApiBaseData:
                if charmType:
                    dataList.append({
                        'stepsName': '基本信息',
                        'errorMsg': '当前所属功能下已有相同接口名称,类型,请更改!',
                        'updateTime': cls_Common.get_date_time()})
                else:
                    if obj_db_ApiBaseData:
                        if basicInfo.apiId == obj_db_ApiBaseData[0].id:
                            pass
                        else:
                            dataList.append({
                                'stepsName': '基本信息',
                                'errorMsg': '当前所属功能下已有相同接口名称,类型,请更改!',
                                'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证请求URl
        if not apiInfo.requestUrl:
            dataList.append({
                'stepsName': '接口信息',
                'errorMsg': '不可新增接口请求地址为空的接口数据!',
                'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证 headers
        if apiInfo.request.headers:
            for index, item_headers in enumerate(apiInfo.request.headers, 1):
                if item_headers.state:
                    if not item_headers.key:
                        dataList.append({
                            'stepsName': '接口信息-Headers',
                            'errorMsg': f'第{index}行:参数名称不可为空!',
                            'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证 params
        if apiInfo.request.params:
            for index, item_params in enumerate(apiInfo.request.params, 1):
                if item_params.state:
                    if not item_params.key:
                        dataList.append({
                            'stepsName': '接口信息-Params',
                            'errorMsg': f'第{index}行:参数名称不可为空!',
                            'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证 body
        if apiInfo.request.body.requestSaveType == 'form-data':
            for index, item_body in enumerate(apiInfo.request.body.formData, 1):
                if item_body.state:
                    if not item_body.key:
                        dataList.append({
                            'stepsName': '接口信息-Body',
                            'errorMsg': f'第{index}行:参数名称不可为空!',
                            'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证 提取
        if apiInfo.request.extract:
            for index, item_extract in enumerate(apiInfo.request.extract, 1):
                if item_extract.state:
                    if not item_extract.key:
                        dataList.append({
                            'stepsName': '接口信息-Extract',
                            'errorMsg': f'第{index}行:变量名称不可为空!',
                            'updateTime': cls_Common.get_date_time()})
                    if not item_extract.value:
                        dataList.append({
                            'stepsName': '接口信息-Extract',
                            'errorMsg': f'第{index}行:提取表达式不可为空!',
                            'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证 断言
        if apiInfo.request.validate:
            for index, item_validate in enumerate(apiInfo.request.validate, 1):
                if item_validate.state:
                    if not item_validate.checkName:
                        dataList.append({
                            'stepsName': '接口信息-Validate',
                            'errorMsg': f'第{index}行:提取变量名称不可为空!',
                            'updateTime': cls_Common.get_date_time()})
                    if not item_validate.validateType:
                        dataList.append({
                            'stepsName': '接口信息-Validate',
                            'errorMsg': f'第{index}行:断言类型不可为空!',
                            'updateTime': cls_Common.get_date_time()})
                    if not item_validate.valueType:
                        dataList.append({
                            'stepsName': '接口信息-Validate',
                            'errorMsg': f'第{index}行:断言值类型不可为空!',
                            'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证 前置操作
        if apiInfo.request.preOperation:
            for index, item_preOperation in enumerate(apiInfo.request.preOperation, 1):
                if item_preOperation.state:
                    if item_preOperation.operationType == 'Methods':
                        if not item_preOperation.methodsName:
                            dataList.append({
                                'stepsName': '接口信息-前置操作',
                                'errorMsg': f'第{index}行:函数方法名称不可为空!',
                                'updateTime': cls_Common.get_date_time()})
                        if '(' not in item_preOperation.methodsName or ')' not in item_preOperation.methodsName:
                            dataList.append({
                                'stepsName': '接口信息-前置操作',
                                'errorMsg': f'第{index}行:函数方法名称未检测到 ()',
                                'updateTime': cls_Common.get_date_time()})

                    elif item_preOperation.operationType == 'DataBase':
                        if not item_preOperation.dataBase:
                            dataList.append({
                                'stepsName': '接口信息-前置操作',
                                'errorMsg': f'第{index}行:当前没有选择需要执行的数据库!',
                                'updateTime': cls_Common.get_date_time()})
                        if not item_preOperation.sql:
                            dataList.append({
                                'stepsName': '接口信息-前置操作',
                                'errorMsg': f'第{index}行:请输入SQL语句!',
                                'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证 后置操作
        if apiInfo.request.rearOperation:
            for index, item_rearOperation in enumerate(apiInfo.request.rearOperation, 1):
                if item_rearOperation.state:
                    if item_rearOperation.operationType == 'Methods':
                        if not item_rearOperation.methodsName:
                            dataList.append({
                                'stepsName': '接口信息-后置操作',
                                'errorMsg': f'第{index}行:函数方法名称不可为空!',
                                'updateTime': cls_Common.get_date_time()})
                        if '(' not in item_rearOperation.methodsName or ')' not in item_rearOperation.methodsName:
                            dataList.append({
                                'stepsName': '接口信息-后置操作',
                                'errorMsg': f'第{index}行:函数方法名称未检测到 ()',
                                'updateTime': cls_Common.get_date_time()})
                    elif item_rearOperation.operationType == 'DataBase':
                        if not item_rearOperation.dataBase:
                            dataList.append({
                                'stepsName': '接口信息-后置操作',
                                'errorMsg': f'第{index}行:当前没有选择需要执行的数据库!',
                                'updateTime': cls_Common.get_date_time()})
                        if not item_rearOperation.sql:
                            dataList.append({
                                'stepsName': '接口信息-后置操作',
                                'errorMsg': f'第{index}行:请输入SQL语句!',
                                'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证params 和body 至少有1个有参数
        if not apiInfo.request.params and \
                not apiInfo.request.body.formData and \
                not apiInfo.request.body.raw and not apiInfo.request.body.requestSaveType == 'none':
            dataList.append({
                'stepsName': '接口信息-参数请求',
                'errorMsg': f'不可创建空参数请求,Params或Body请求中至少有1个不可为空!',
                'updateTime': cls_Common.get_date_time()})
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
        apiInfo = objData.ApiInfo
        if basicInfo.assignedUserId:
            assignedUserId = basicInfo.assignedUserId[1]
        else:
            assignedUserId = userId
        requestParamsType = cls_RequstOperation.for_data_get_requset_params_type(
            apiInfo.request.params, apiInfo.request.body.formData, apiInfo.request.body.raw)
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_IntMaintenance', 'data_save', errorMsg)
    else:
        obj_db_ApiBaseData = db_ApiBaseData.objects.filter(
            is_del=0, pid_id=basicInfo.proId, page_id=basicInfo.pageId, fun_id=basicInfo.funId,
            apiName=basicInfo.apiName, requestType=apiInfo.requestType, requestUrl=apiInfo.requestUrl)
        if obj_db_ApiBaseData:
            response['errorMsg'] = f'当前所属功能下已有相同数据,请修改后在继续保存!'
        else:
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    # region 添加操作信息
                    operationInfoId = cls_Logging.record_operation_info(
                        'API', 'Manual', 3, 'Add',
                        cls_FindTable.get_pro_name(basicInfo.proId),
                        cls_FindTable.get_page_name(basicInfo.pageId),
                        cls_FindTable.get_fun_name(basicInfo.funId),
                        userId,
                        '【新增接口】', CUFront=responseData
                    )
                    # endregion
                    # region 保存基本信息
                    save_db_ApiBaseData = db_ApiBaseData.objects.create(
                        pid_id=basicInfo.proId, page_id=basicInfo.pageId, fun_id=basicInfo.funId,
                        apiName=basicInfo.apiName, environment_id=basicInfo.environmentId, apiState=basicInfo.apiState,
                        requestType=apiInfo.requestType, requestUrl=apiInfo.requestUrl,
                        requestParamsType='Body' if apiInfo.request.body.requestSaveType == 'none' else requestParamsType,
                        bodyRequestSaveType=apiInfo.request.body.requestSaveType,
                        uid_id=assignedUserId, cuid=userId, is_del=0,
                    )
                    product_list_to_insert = list()
                    for item_userId in basicInfo.pushTo:
                        product_list_to_insert.append(db_ApiAssociatedUser(
                            apiId_id=save_db_ApiBaseData.id,
                            opertateInfo_id=operationInfoId,
                            uid_id=item_userId[1],
                            is_del=0)
                        )
                    db_ApiAssociatedUser.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region Headers
                    product_list_to_insert = list()
                    for item_headers in apiInfo.request.headers:
                        product_list_to_insert.append(db_ApiHeaders(
                            apiId_id=save_db_ApiBaseData.id,
                            index=item_headers.index,
                            key=item_headers.key,
                            value=item_headers.value,
                            remarks=item_headers.remarks,
                            state=1 if item_headers.state else 0,
                            is_del=0, )
                        )
                    db_ApiHeaders.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region Params
                    product_list_to_insert = list()
                    for item_params in apiInfo.request.params:
                        product_list_to_insert.append(db_ApiParams(
                            apiId_id=save_db_ApiBaseData.id,
                            index=item_params.index,
                            key=item_params.key,
                            value=item_params.value,
                            remarks=item_params.remarks,
                            state=1 if item_params.state else 0,
                            is_del=0, )
                        )
                    db_ApiParams.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region Body
                    if apiInfo.request.body.requestSaveType == 'form-data':
                        product_list_to_insert = list()
                        for item_body in apiInfo.request.body.formData:
                            product_list_to_insert.append(db_ApiBody(
                                apiId_id=save_db_ApiBaseData.id,
                                index=item_body.index,
                                key=item_body.key,
                                value=item_body.value,
                                remarks=item_body.remarks,
                                state=1 if item_body.state else 0,
                                is_del=0, )
                            )
                        db_ApiBody.objects.bulk_create(product_list_to_insert)
                    elif apiInfo.request.body.requestSaveType == 'raw':
                        db_ApiBody.objects.create(
                            apiId_id=save_db_ApiBaseData.id,
                            index=0,
                            key=None,
                            value=apiInfo.request.body.raw,
                            state=1,
                            is_del=0
                        )
                    # file 之后在做
                    # endregion
                    # region Extract
                    product_list_to_insert = list()
                    for item_extract in apiInfo.request.extract:
                        product_list_to_insert.append(db_ApiExtract(
                            apiId_id=save_db_ApiBaseData.id,
                            index=item_extract.index,
                            key=item_extract.key,
                            value=item_extract.value,
                            remarks=item_extract.remarks,
                            state=1 if item_extract.state else 0,
                            is_del=0, )
                        )
                    db_ApiExtract.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region Validate
                    product_list_to_insert = list()
                    for item_validate in apiInfo.request.validate:
                        product_list_to_insert.append(db_ApiValidate(
                            apiId_id=save_db_ApiBaseData.id,
                            index=item_validate.index,
                            checkName=item_validate.checkName,
                            validateType=item_validate.validateType,
                            valueType=item_validate.valueType,
                            expectedResults=item_validate.expectedResults,
                            remarks=item_validate.remarks,
                            state=1 if item_validate.state else 0,
                            is_del=0, )
                        )
                    db_ApiValidate.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region 前置
                    product_list_to_insert = list()
                    for item_preOperation in apiInfo.request.preOperation:
                        product_list_to_insert.append(db_ApiOperation(
                            apiId_id=save_db_ApiBaseData.id,
                            index=item_preOperation.index,
                            location='Pre',
                            operationType=item_preOperation.operationType,
                            methodsName=item_preOperation.methodsName,
                            dataBaseId=item_preOperation.dataBase,
                            sql=item_preOperation.sql,
                            remarks=item_preOperation.remarks,
                            state=1 if item_preOperation.state else 0,
                            is_del=0)
                        )
                    db_ApiOperation.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region 后置
                    product_list_to_insert = list()
                    for item_rearOperation in apiInfo.request.rearOperation:
                        product_list_to_insert.append(db_ApiOperation(
                            apiId_id=save_db_ApiBaseData.id,
                            index=item_rearOperation.index,
                            location='Rear',
                            operationType=item_rearOperation.operationType,
                            methodsName=item_rearOperation.methodsName,
                            dataBaseId=item_rearOperation.dataBase,
                            sql=item_rearOperation.sql,
                            remarks=item_rearOperation.remarks,
                            state=1 if item_rearOperation.state else 0,
                            is_del=0)
                        )
                    db_ApiOperation.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region 创建被关联用户的新增提醒
                    obj_db_ApiAssociatedUser = db_ApiAssociatedUser.objects.filter(
                        is_del=0, apiId_id=save_db_ApiBaseData.id)
                    for item_associatedUser in obj_db_ApiAssociatedUser:
                        cls_Logging.push_to_user(operationInfoId, item_associatedUser.uid_id)
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
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        responseData = json.loads(request.body)
        objData = cls_object_maker(responseData)
        basicInfo = objData.BasicInfo
        apiInfo = objData.ApiInfo
        if basicInfo.assignedUserId:
            assignedUserId = basicInfo.assignedUserId[1]
        else:
            assignedUserId = userId
        requestParamsType = cls_RequstOperation.for_data_get_requset_params_type(
            apiInfo.request.params, apiInfo.request.body.formData, apiInfo.request.body.raw)
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_IntMaintenance', 'edit_data', errorMsg)
    else:
        obj_db_ApiBaseData = db_ApiBaseData.objects.filter(id=basicInfo.apiId, is_del=0)
        if obj_db_ApiBaseData:
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    # region 添加操作信息
                    # region 查询以前的数据
                    headers = []
                    params = []
                    body = []
                    extract = []
                    validate = []
                    preOperation = []
                    rearOperation = []
                    # region 基本信息
                    # region headers
                    obj_db_ApiHeaders = db_ApiHeaders.objects.filter(is_del=0, apiId_id=basicInfo.apiId).order_by(
                        'index')
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
                    obj_db_ApiParams = db_ApiParams.objects.filter(is_del=0, apiId_id=basicInfo.apiId).order_by('index')
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
                    obj_db_ApiBody = db_ApiBody.objects.filter(is_del=0, apiId_id=basicInfo.apiId).order_by('index')
                    if obj_db_ApiBaseData[0].bodyRequestSaveType == 'form-data':
                        for item_body in obj_db_ApiBody:
                            body.append({
                                'index': item_body.index,
                                'key': item_body.key,
                                'value': item_body.value,
                                'remarks': item_body.remarks,
                                'state': True if item_body.state else False,
                            })
                        bodyData = body
                    elif obj_db_ApiBaseData[0].bodyRequestSaveType == 'raw':
                        bodyData = obj_db_ApiBody[0].value
                    # endregion
                    # region extract
                    obj_db_ApiExtract = db_ApiExtract.objects.filter(is_del=0, apiId_id=basicInfo.apiId).order_by(
                        'index')
                    for item_extract in obj_db_ApiExtract:
                        extract.append({
                            'index': item_extract.index,
                            'key': item_extract.key,
                            'value': item_extract.value,
                            'remarks': item_extract.remarks,
                            'state': True if item_extract.state else False,
                        })
                    # endregion
                    # region validate
                    obj_db_ApiValidate = db_ApiValidate.objects.filter(is_del=0, apiId_id=basicInfo.apiId).order_by(
                        'index')
                    for item_validate in obj_db_ApiValidate:
                        validate.append({
                            'index': item_validate.index,
                            'checkName': item_validate.checkName,
                            'validateType': item_validate.validateType,
                            'valueType': item_validate.valueType,
                            'expectedResults': item_validate.expectedResults,
                            'remarks': item_validate.remarks,
                            'state': True if item_validate.state else False,
                        })
                    # endregion
                    # region 前置操作
                    obj_db_ApiOperation = db_ApiOperation.objects.filter(
                        is_del=0, apiId_id=basicInfo.apiId, location='Pre').order_by('index')
                    for item_preOperation in obj_db_ApiOperation:
                        preOperation.append({
                            'index': item_preOperation.index,
                            'operationType': item_preOperation.operationType,
                            'methodsName': item_preOperation.methodsName,
                            'dataBase': item_preOperation.dataBaseId,
                            'sql': item_preOperation.sql,
                            'remarks': item_preOperation.remarks,
                            'state': True if item_preOperation.state else False,
                        })
                    # endregion
                    # region 后置操作
                    obj_db_ApiOperation = db_ApiOperation.objects.filter(
                        is_del=0, apiId_id=basicInfo.apiId, location='Rear').order_by('index')
                    for item_rearOperation in obj_db_ApiOperation:
                        rearOperation.append({
                            'index': item_rearOperation.index,
                            'operationType': item_rearOperation.operationType,
                            'methodsName': item_rearOperation.methodsName,
                            'dataBase': item_rearOperation.dataBaseId,
                            'sql': item_rearOperation.sql,
                            'remarks': item_rearOperation.remarks,
                            'state': True if item_rearOperation.state else False,
                        })
                    # endregion
                    # endregion
                    oldData = {
                        'basicInfo': {
                            'apiId': basicInfo.apiId,
                            'proId': obj_db_ApiBaseData[0].pid_id,
                            'pageId': obj_db_ApiBaseData[0].page_id,
                            'funId': obj_db_ApiBaseData[0].fun_id,
                            'environmentId': obj_db_ApiBaseData[0].environment_id,
                            'apiName': obj_db_ApiBaseData[0].apiName,
                            'apiState': obj_db_ApiBaseData[0].apiState,
                            'assignedUserId': obj_db_ApiBaseData[0].uid_id},
                        'apiInfo': {
                            'requestType': obj_db_ApiBaseData[0].requestType,
                            'requestUrl': obj_db_ApiBaseData[0].requestUrl,
                            'request': {
                                'headers': headers,
                                'params': params,
                                'body': {
                                    'requestSaveType': obj_db_ApiBaseData[0].bodyRequestSaveType,
                                    'bodyData': bodyData
                                },
                                'extract': extract,
                                'validate': validate,
                                'preOperation': preOperation,
                                'rearOperation': rearOperation,
                            }
                        }
                    }
                    # endregion
                    operationInfoId = cls_Logging.record_operation_info(
                        'API', 'Manual', 3, 'Edit',
                        cls_FindTable.get_pro_name(basicInfo.proId),
                        cls_FindTable.get_page_name(basicInfo.pageId),
                        cls_FindTable.get_fun_name(basicInfo.funId),
                        userId,
                        f'【修改接口】 ID{obj_db_ApiBaseData[0].id}:{obj_db_ApiBaseData[0].apiName}',
                        CUFront=oldData, CURear=responseData
                    )
                    # region 创建系统级别的工单
                    save_db_WorkorderManagement = db_WorkorderManagement.objects.create(
                        sysType='API', pid_id=basicInfo.proId, page_id=basicInfo.pageId, fun_id=basicInfo.funId,
                        workSource=1, workType='Edit', workState=0, workName=basicInfo.apiName,
                        message=f"{oldData}\n\n{responseData}",
                        uid_id=userId,
                        cuid=userId,
                        is_del=0,
                    )
                    # 创建工单生命周期
                    db_WorkLifeCycle.objects.create(
                        work_id=save_db_WorkorderManagement.id,workState=1,operationType='Add',
                        operationInfo=None,uid_id=userId,is_del=0,
                    )
                    # endregion
                    # endregion
                    # region 删除 各类原数据
                    db_ApiHeaders.objects.filter(is_del=0, apiId_id=basicInfo.apiId).update(
                        updateTime=cls_Common.get_date_time(), is_del=1
                    )
                    db_ApiParams.objects.filter(is_del=0, apiId_id=basicInfo.apiId).update(
                        updateTime=cls_Common.get_date_time(), is_del=1
                    )
                    db_ApiBody.objects.filter(is_del=0, apiId_id=basicInfo.apiId).update(
                        updateTime=cls_Common.get_date_time(), is_del=1
                    )
                    db_ApiExtract.objects.filter(is_del=0, apiId_id=basicInfo.apiId).update(
                        updateTime=cls_Common.get_date_time(), is_del=1
                    )
                    db_ApiValidate.objects.filter(is_del=0, apiId_id=basicInfo.apiId).update(
                        updateTime=cls_Common.get_date_time(), is_del=1
                    )
                    db_ApiOperation.objects.filter(is_del=0, apiId_id=basicInfo.apiId).update(
                        updateTime=cls_Common.get_date_time(), is_del=1
                    )
                    db_ApiAssociatedUser.objects.filter(is_del=0, apiId_id=basicInfo.apiId).update(
                        updateTime=cls_Common.get_date_time(), is_del=1
                    )
                    # endregion
                    # region 更新基本信息
                    obj_db_ApiBaseData.update(
                        pid_id=basicInfo.proId, page_id=basicInfo.pageId, fun_id=basicInfo.funId,
                        apiName=basicInfo.apiName, environment_id=basicInfo.environmentId, apiState=basicInfo.apiState,
                        requestType=apiInfo.requestType, requestUrl=apiInfo.requestUrl,
                        requestParamsType='Body' if apiInfo.request.body.requestSaveType == 'none' else requestParamsType,
                        bodyRequestSaveType=apiInfo.request.body.requestSaveType,
                        uid_id=assignedUserId, cuid=userId, is_del=0, updateTime=cls_Common.get_date_time()
                    )
                    product_list_to_insert = list()
                    for item_userId in basicInfo.pushTo:
                        product_list_to_insert.append(db_ApiAssociatedUser(
                            apiId_id=basicInfo.apiId,
                            opertateInfo_id=operationInfoId,
                            uid_id=item_userId[1],
                            is_del=0)
                        )
                    db_ApiAssociatedUser.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region Headers
                    product_list_to_insert = list()
                    for item_headers in apiInfo.request.headers:
                        product_list_to_insert.append(db_ApiHeaders(
                            apiId_id=basicInfo.apiId,
                            index=item_headers.index,
                            key=item_headers.key,
                            value=item_headers.value,
                            remarks=item_headers.remarks,
                            state=1 if item_headers.state else 0,
                            is_del=0, )
                        )
                    db_ApiHeaders.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region Params
                    product_list_to_insert = list()
                    for item_params in apiInfo.request.params:
                        product_list_to_insert.append(db_ApiParams(
                            apiId_id=basicInfo.apiId,
                            index=item_params.index,
                            key=item_params.key,
                            value=item_params.value,
                            remarks=item_params.remarks,
                            state=1 if item_params.state else 0,
                            is_del=0, )
                        )
                    db_ApiParams.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region Body
                    if apiInfo.request.body.requestSaveType == 'form-data':
                        product_list_to_insert = list()
                        for item_body in apiInfo.request.body.formData:
                            product_list_to_insert.append(db_ApiBody(
                                apiId_id=basicInfo.apiId,
                                index=item_body.index,
                                key=item_body.key,
                                value=item_body.value,
                                remarks=item_body.remarks,
                                state=1 if item_body.state else 0,
                                is_del=0, )
                            )
                        db_ApiBody.objects.bulk_create(product_list_to_insert)
                    elif apiInfo.request.body.requestSaveType == 'raw':
                        db_ApiBody.objects.create(
                            apiId_id=basicInfo.apiId,
                            index=0,
                            key=None,
                            value=apiInfo.request.body.raw,
                            state=1,
                            is_del=0
                        )
                    # file 之后在做
                    # endregion
                    # region Extract
                    product_list_to_insert = list()
                    for item_extract in apiInfo.request.extract:
                        product_list_to_insert.append(db_ApiExtract(
                            apiId_id=basicInfo.apiId,
                            index=item_extract.index,
                            key=item_extract.key,
                            value=item_extract.value,
                            remarks=item_extract.remarks,
                            state=1 if item_extract.state else 0,
                            is_del=0, )
                        )
                    db_ApiExtract.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region Validate
                    product_list_to_insert = list()
                    for item_validate in apiInfo.request.validate:
                        product_list_to_insert.append(db_ApiValidate(
                            apiId_id=basicInfo.apiId,
                            index=item_validate.index,
                            checkName=item_validate.checkName,
                            validateType=item_validate.validateType,
                            valueType=item_validate.valueType,
                            expectedResults=item_validate.expectedResults,
                            remarks=item_validate.remarks,
                            state=1 if item_validate.state else 0,
                            is_del=0, )
                        )
                    db_ApiValidate.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region 前置
                    product_list_to_insert = list()
                    for item_preOperation in apiInfo.request.preOperation:
                        product_list_to_insert.append(db_ApiOperation(
                            apiId_id=basicInfo.apiId,
                            index=item_preOperation.index,
                            location='Pre',
                            operationType=item_preOperation.operationType,
                            methodsName=item_preOperation.methodsName,
                            dataBaseId=item_preOperation.dataBase,
                            sql=item_preOperation.sql,
                            remarks=item_preOperation.remarks,
                            state=1 if item_preOperation.state else 0,
                            is_del=0)
                        )
                    db_ApiOperation.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region 后置
                    product_list_to_insert = list()
                    for item_rearOperation in apiInfo.request.rearOperation:
                        product_list_to_insert.append(db_ApiOperation(
                            apiId_id=basicInfo.apiId,
                            index=item_rearOperation.index,
                            location='Rear',
                            operationType=item_rearOperation.operationType,
                            methodsName=item_rearOperation.methodsName,
                            dataBaseId=item_rearOperation.dataBase,
                            sql=item_rearOperation.sql,
                            remarks=item_rearOperation.remarks,
                            state=1 if item_rearOperation.state else 0,
                            is_del=0)
                        )
                    db_ApiOperation.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region 创建被关联用户的新增提醒
                    obj_db_ApiAssociatedUser = db_ApiAssociatedUser.objects.filter(
                        is_del=0, apiId_id=basicInfo.apiId)
                    for item_associatedUser in obj_db_ApiAssociatedUser:
                        db_WorkBindPushToUsers.objects.create(
                            work_id=save_db_WorkorderManagement.id,
                            uid_id=item_associatedUser.uid_id,
                            is_del=0
                        )
                        cls_Logging.push_to_user(operationInfoId, item_associatedUser.uid_id)
                    # endregion
            except BaseException as e:  # 自动回滚，不需要任何操作
                response['errorMsg'] = f'数据修改失败:{e}'
            else:
                response['statusCode'] = 2002
        else:
            response['errorMsg'] = '未找当前接口数据,请刷新后重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def delete_data(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        apiId = request.POST['apiId']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_IntMaintenance', 'delete_data', errorMsg)
    else:
        obj_db_ApiBaseData = db_ApiBaseData.objects.filter(id=apiId)
        if obj_db_ApiBaseData:
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    obj_db_ApiBaseData.update(is_del=1, updateTime=cls_Common.get_date_time(), uid_id=userId)
                    db_ApiHeaders.objects.filter(is_del=0, apiId_id=apiId).update(
                        is_del=1, updateTime=cls_Common.get_date_time())
                    db_ApiParams.objects.filter(is_del=0, apiId_id=apiId).update(
                        is_del=1, updateTime=cls_Common.get_date_time())
                    db_ApiBody.objects.filter(is_del=0, apiId_id=apiId).update(
                        is_del=1, updateTime=cls_Common.get_date_time())
                    db_ApiExtract.objects.filter(is_del=0, apiId_id=apiId).update(
                        is_del=1, updateTime=cls_Common.get_date_time())
                    db_ApiValidate.objects.filter(is_del=0, apiId_id=apiId).update(
                        is_del=1, updateTime=cls_Common.get_date_time())
                    db_ApiOperation.objects.filter(is_del=0, apiId_id=apiId).update(
                        is_del=1, updateTime=cls_Common.get_date_time())
                    # region 添加操作信息
                    cls_Logging.record_operation_info(
                        'API', 'Manual', 3, 'Delete',
                        cls_FindTable.get_pro_name(obj_db_ApiBaseData[0].pid_id),
                        cls_FindTable.get_page_name(obj_db_ApiBaseData[0].page_id),
                        cls_FindTable.get_fun_name(obj_db_ApiBaseData[0].fun_id),
                        userId,
                        f'【删除接口】 ID:{apiId}:{obj_db_ApiBaseData[0].apiName}',
                        CUFront=json.dumps(request.POST)
                    )
                    # endregion
            except BaseException as e:  # 自动回滚，不需要任何操作
                response['errorMsg'] = f'数据删除失败:{e}'
            else:
                response['statusCode'] = 2003
        else:
            response['errorMsg'] = '未找到当前接口数据,请刷新后重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def load_data(request):
    response = {}
    headers = []
    params = []
    body = []
    extract = []
    validate = []
    preOperation = []  # 前置操作
    rearOperation = []  # 后置操作
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        apiId = objData.apiId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_IntMaintenance', 'load_data', errorMsg)
    else:
        obj_db_ApiBaseData = db_ApiBaseData.objects.filter(is_del=0, id=apiId)
        if obj_db_ApiBaseData:
            # region 基本信息
            roleId = cls_FindTable.get_roleId(obj_db_ApiBaseData[0].uid_id)
            pushTo = []
            obj_db_ApiAssociatedUser = db_ApiAssociatedUser.objects.filter(is_del=0, apiId_id=apiId)
            for item_associateUser in obj_db_ApiAssociatedUser:
                pushTo.append([cls_FindTable.get_roleId(item_associateUser.uid_id), item_associateUser.uid_id])
            basicInfo = {
                'pageId': obj_db_ApiBaseData[0].page_id,
                'funId': obj_db_ApiBaseData[0].fun_id,
                'environmentId': obj_db_ApiBaseData[0].environment_id,
                'apiName': obj_db_ApiBaseData[0].apiName,
                'apiState': obj_db_ApiBaseData[0].apiState,
                'assignedUserId': [roleId, obj_db_ApiBaseData[0].uid_id],
                'pushTo': pushTo,
            }
            # endregion
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
            if obj_db_ApiBaseData[0].bodyRequestSaveType == 'form-data':
                for item_body in obj_db_ApiBody:
                    body.append({
                        'index': item_body.index,
                        'key': item_body.key,
                        'value': item_body.value,
                        'remarks': item_body.remarks,
                        'state': True if item_body.state else False,
                    })
                bodyData = body
            elif obj_db_ApiBaseData[0].bodyRequestSaveType == 'raw':
                bodyData = obj_db_ApiBody[0].value
            # endregion
            # region extract
            obj_db_ApiExtract = db_ApiExtract.objects.filter(is_del=0, apiId_id=apiId).order_by('index')
            for item_extract in obj_db_ApiExtract:
                extract.append({
                    'index': item_extract.index,
                    'key': item_extract.key,
                    'value': item_extract.value,
                    'remarks': item_extract.remarks,
                    'state': True if item_extract.state else False,
                })
            # endregion
            # region validate
            obj_db_ApiValidate = db_ApiValidate.objects.filter(is_del=0, apiId_id=apiId).order_by('index')
            for item_validate in obj_db_ApiValidate:
                validate.append({
                    'index': item_validate.index,
                    'checkName': item_validate.checkName,
                    'validateType': item_validate.validateType,
                    'valueType': item_validate.valueType,
                    'expectedResults': item_validate.expectedResults,
                    'remarks': item_validate.remarks,
                    'state': True if item_validate.state else False,
                })
            # endregion
            # region 前置操作
            obj_db_ApiOperation = db_ApiOperation.objects.filter(
                is_del=0, apiId_id=apiId, location='Pre').order_by('index')
            for item_preOperation in obj_db_ApiOperation:
                preOperation.append({
                    'index': item_preOperation.index,
                    'operationType': item_preOperation.operationType,
                    'methodsName': item_preOperation.methodsName,
                    'dataBase': item_preOperation.dataBaseId,
                    'sql': item_preOperation.sql,
                    'remarks': item_preOperation.remarks,
                    'state': True if item_preOperation.state else False,
                })
            # endregion
            # region 后置操作
            obj_db_ApiOperation = db_ApiOperation.objects.filter(
                is_del=0, apiId_id=apiId, location='Rear').order_by('index')
            for item_rearOperation in obj_db_ApiOperation:
                rearOperation.append({
                    'index': item_rearOperation.index,
                    'operationType': item_rearOperation.operationType,
                    'methodsName': item_rearOperation.methodsName,
                    'dataBase': item_rearOperation.dataBaseId,
                    'sql': item_rearOperation.sql,
                    'remarks': item_rearOperation.remarks,
                    'state': True if item_rearOperation.state else False,
                })
            # endregion
            # region apiInfo
            apiInfo = {
                'requestType': obj_db_ApiBaseData[0].requestType,
                'requestUrl': obj_db_ApiBaseData[0].requestUrl,
                'request': {
                    'headers': headers,
                    'params': params,
                    'body': {
                        'requestSaveType': obj_db_ApiBaseData[0].bodyRequestSaveType,
                        'bodyData': bodyData
                    },
                    'extract': extract,
                    'validate': validate,
                    'preOperation': preOperation,
                    'rearOperation': rearOperation,
                }
            }
            # endregion

            response['basicInfo'] = basicInfo
            response['apiInfo'] = apiInfo
            response['statusCode'] = 2000
        else:
            response['errorMsg'] = "未找到当前选择的接口数据,请刷新后重新尝试!"
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def send_request(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        apiId = request.POST['apiId']
        environmentId = request.POST['environmentId']
        onlyCode = cls_Common.generate_only_code()
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_IntMaintenance', 'request_api', errorMsg)
    else:
        cls_Logging.print_log('info', 'send_request', '-----------------------------start-----------------------------')
        response = cls_RequstOperation.run_request(apiId, environmentId, onlyCode, userId)
        if response['state']:
            response['statusCode'] = 2000
        cls_Logging.print_log('info', 'send_request', '-----------------------------END-----------------------------')
    return JsonResponse(response)
