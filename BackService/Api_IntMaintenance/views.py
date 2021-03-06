from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction
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
from Api_IntMaintenance.models import ApiExtract as db_ApiExtract
from Api_IntMaintenance.models import ApiValidate as db_ApiValidate
from Api_IntMaintenance.models import ApiOperation as db_ApiOperation
from Api_IntMaintenance.models import ApiAssociatedUser as db_ApiAssociatedUser
from Api_IntMaintenance.models import ApiDynamic as db_ApiDynamic
# from WorkorderManagement.models import WorkorderManagement as db_WorkorderManagement
# from WorkorderManagement.models import WorkBindPushToUsers as db_WorkBindPushToUsers
# from WorkorderManagement.models import WorkLifeCycle as db_WorkLifeCycle
from Api_IntMaintenance.models import ApiHistory as db_ApiHistory
from PageEnvironment.models import PageEnvironment as db_PageEnvironment
from Api_CaseMaintenance.models import CaseTestSet as db_CaseTestSet
from Api_TestReport.models import ApiReportItem as db_ApiReportItem

# Create reference here.
from ClassData.Logger import Logging
from ClassData.GlobalDecorator import GlobalDer
from ClassData.FindCommonTable import FindTable
from ClassData.Common import Common
from ClassData.ImageProcessing import ImageProcessing
from ClassData.ObjectMaker import object_maker as cls_object_maker
from ClassData.Request import RequstOperation
from ClassData.TestReport import ApiReport
from ClassData.OpenApi import Swagger
from ClassData.FileOperations import FileOperations

# Create info here.
cls_Logging = Logging()
cls_GlobalDer = GlobalDer()
cls_FindTable = FindTable()
cls_Common = Common()
cls_ImageProcessing = ImageProcessing()
cls_RequstOperation = RequstOperation()
cls_ApiReport = ApiReport()
cls_Swagger = Swagger()
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
        apiName = objData.apiName
        requestUrl = objData.requestUrl
        apiState = objData.apiState
        associations = objData.associations

        current = int(objData.current)  # ????????????
        pageSize = int(objData.pageSize)  # ???????????????
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"????????????:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_IntMaintenance', 'select_data', errorMsg)
    else:
        obj_db_ApiBaseData = db_ApiBaseData.objects.filter(is_del=0, pid_id=proId).order_by('-updateTime')
        if pageId:
            obj_db_ApiBaseData = obj_db_ApiBaseData.filter(page_id=pageId)
        if funId:
            obj_db_ApiBaseData = obj_db_ApiBaseData.filter(fun_id=funId)
        if apiName:
            obj_db_ApiBaseData = obj_db_ApiBaseData.filter(apiName__icontains=apiName)
        if requestUrl:
            obj_db_ApiBaseData = obj_db_ApiBaseData.filter(requestUrl__icontains=requestUrl)
        if apiState:
            obj_db_ApiBaseData = obj_db_ApiBaseData.filter(apiState=apiState)
        select_db_ApiBaseData = obj_db_ApiBaseData[minSize: maxSize]
        for i in select_db_ApiBaseData:
            obj_db_ApiAssociatedUser = db_ApiAssociatedUser.objects.filter(is_del=0, apiId_id=i.id, uid_id=userId)
            if obj_db_ApiAssociatedUser or userId == i.cuid:
                associationMy = True
            else:
                associationMy = False
            url = ast.literal_eval(i.requestUrl)
            callIndex = f'url{i.requestUrlRadio}'
            # region ??????????????? = ???????????? / ??????+???????????? * 100
            passTotal = 0
            failTotal = 0
            errorTotal = 0
            obj_db_ApiReportItem = db_ApiReportItem.objects.filter(is_del=0, apiId_id=i.id)
            for item in obj_db_ApiReportItem:
                passTotal += item.successTotal
                failTotal += item.failTotal
                errorTotal += item.errorTotal
            allTotal = passTotal + failTotal + errorTotal
            if allTotal == 0:
                passRate = 0
            else:
                passRate = round(passTotal / allTotal * 100, 2)
            # endregion
            if associations == 'My':
                if associationMy:
                    dataList.append({
                        'id': i.id,
                        'pageId': i.page_id,
                        'pageName': i.page.pageName,
                        'funId': i.fun_id,
                        'funName': i.fun.funName,
                        'apiName': i.apiName,
                        'requestType': i.requestType,
                        'requestUrl': url[f'{callIndex}'],  # ????????????json?????????URl
                        'apiState': i.apiState,
                        'associationMy': associationMy,  # ????????????
                        'passRate': passRate,
                        'updateTime': str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                        "userName": f"{i.uid.userName}({i.uid.nickName})",
                        'createUserId': [[cls_FindTable.get_roleId(i.cuid), i.cuid]],
                        'createUserName': cls_FindTable.get_userName(i.cuid)
                    })
            else:
                dataList.append({
                    'id': i.id,
                    'pageId': i.page_id,
                    'pageName': i.page.pageName,
                    'funId': i.fun_id,
                    'funName': i.fun.funName,
                    'apiName': i.apiName,
                    'requestType': i.requestType,
                    'requestUrl': url[f'{callIndex}'],  # ????????????json?????????URl
                    'apiState': i.apiState,
                    'associationMy': associationMy,  # ????????????
                    'passRate': passRate,
                    'updateTime': str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                    "userName": f"{i.uid.userName}({i.uid.nickName})",
                    'createUserId': [[cls_FindTable.get_roleId(i.cuid), i.cuid]],
                    'createUserName': cls_FindTable.get_userName(i.cuid)
                })
        response['TableData'] = dataList
        response['Total'] = obj_db_ApiBaseData.count()
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # ??????????????????????????????
def charm_api_data(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(request.body)
        objData = cls_object_maker(responseData)
        charmType = objData.CharmType  # true ?????????false ??????
        basicInfo = objData.BasicInfo
        apiInfo = objData.ApiInfo
    except BaseException as e:
        errorMsg = f"????????????:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_IntMaintenance', 'charm_api_data', errorMsg)
    else:
        # region ?????? ????????????,????????????,????????????
        requestUrlRadio = apiInfo.requestUrlRadio
        requestUrl = responseData['ApiInfo']['requestUrl'][f'url{requestUrlRadio}']
        obj_db_ApiBaseData = db_ApiBaseData.objects.filter(
            is_del=0, pid_id=basicInfo.proId, page_id=basicInfo.pageId, fun_id=basicInfo.funId,
            apiName=basicInfo.apiName, requestType=apiInfo.requestType, requestUrl=requestUrl)
        if obj_db_ApiBaseData.exists():
            if charmType:
                dataList.append({
                    'stepsName': '????????????',
                    'errorMsg': '?????????????????????????????????????????????,??????,????????????,?????????!',
                    'updateTime': cls_Common.get_date_time()})
            else:
                if obj_db_ApiBaseData.exists():
                    if basicInfo.apiId == obj_db_ApiBaseData[0].id:
                        pass
                    else:
                        dataList.append({
                            'stepsName': '????????????',
                            'errorMsg': '?????????????????????????????????????????????,??????,????????????,?????????!',
                            'updateTime': cls_Common.get_date_time()})
        else:
            obj_db_ApiBaseData = db_ApiBaseData.objects.filter(
                is_del=0, pid_id=basicInfo.proId, page_id=basicInfo.pageId, fun_id=basicInfo.funId,
                apiName=basicInfo.apiName, requestType=apiInfo.requestType)
            if obj_db_ApiBaseData.exists():
                if charmType:
                    dataList.append({
                        'stepsName': '????????????',
                        'errorMsg': '?????????????????????????????????????????????,??????,?????????!',
                        'updateTime': cls_Common.get_date_time()})
                else:
                    if obj_db_ApiBaseData.exists():
                        if basicInfo.apiId == obj_db_ApiBaseData[0].id:
                            pass
                        else:
                            dataList.append({
                                'stepsName': '????????????',
                                'errorMsg': '?????????????????????????????????????????????,??????,?????????!',
                                'updateTime': cls_Common.get_date_time()})
        # endregion
        # region ????????????URl

        if not requestUrl:
            dataList.append({
                'stepsName': '????????????',
                'errorMsg': f"??????{f'url{requestUrlRadio}'},????????????????????????!",
                'updateTime': cls_Common.get_date_time()})
        # endregion
        # region ?????? headers
        if apiInfo.request.headers:
            for index, item_headers in enumerate(apiInfo.request.headers, 1):
                if item_headers.state:
                    if not item_headers.key:
                        dataList.append({
                            'stepsName': '????????????-Headers',
                            'errorMsg': f'???{index}???:????????????????????????!',
                            'updateTime': cls_Common.get_date_time()})
        # endregion
        # region ?????? params
        if apiInfo.request.params:
            for index, item_params in enumerate(apiInfo.request.params, 1):
                if item_params.state:
                    if not item_params.key:
                        dataList.append({
                            'stepsName': '????????????-Params',
                            'errorMsg': f'???{index}???:????????????????????????!',
                            'updateTime': cls_Common.get_date_time()})
        # endregion
        # region ?????? body
        if apiInfo.request.body.requestSaveType == 'form-data':
            for index, item_body in enumerate(apiInfo.request.body.formData, 1):
                if item_body.state:
                    if item_body.paramsType == 'Text':
                        if not item_body.key:
                            dataList.append({
                                'stepsName': '????????????-Body',
                                'errorMsg': f'???{index}???:????????????????????????!',
                                'updateTime': cls_Common.get_date_time()})
                    else:  # ????????????
                        if not item_body.key:
                            dataList.append({
                                'stepsName': '????????????-Body',
                                'errorMsg': f'???{index}???:????????????????????????!',
                                'updateTime': cls_Common.get_date_time()})
                        if not item_body.fileList:
                            dataList.append({
                                'stepsName': '????????????-Body',
                                'errorMsg': f'???{index}???:????????????????????????!',
                                'updateTime': cls_Common.get_date_time()})

        elif apiInfo.request.body.requestSaveType == 'raw':
            if not apiInfo.request.body.raw:
                dataList.append({
                    'stepsName': '????????????-Body',
                    'errorMsg': f'Raw??????????????????!',
                    'updateTime': cls_Common.get_date_time()})
        elif apiInfo.request.body.requestSaveType == 'json':
            if not apiInfo.request.body.json:
                dataList.append({
                    'stepsName': '????????????-Body',
                    'errorMsg': f'Json??????????????????!',
                    'updateTime': cls_Common.get_date_time()})
        # endregion
        # region ?????? ??????
        if apiInfo.request.extract:
            for index, item_extract in enumerate(apiInfo.request.extract, 1):
                if item_extract.state:
                    if not item_extract.key:
                        dataList.append({
                            'stepsName': '????????????-Extract',
                            'errorMsg': f'???{index}???:????????????????????????!',
                            'updateTime': cls_Common.get_date_time()})
                    if not item_extract.value:
                        dataList.append({
                            'stepsName': '????????????-Extract',
                            'errorMsg': f'???{index}???:???????????????????????????!',
                            'updateTime': cls_Common.get_date_time()})
        # endregion
        # region ?????? ??????
        if apiInfo.request.validate:
            for index, item_validate in enumerate(apiInfo.request.validate, 1):
                if item_validate.state:
                    if not item_validate.checkName:
                        dataList.append({
                            'stepsName': '????????????-Validate',
                            'errorMsg': f'???{index}???:??????????????????????????????!',
                            'updateTime': cls_Common.get_date_time()})
                    if not item_validate.validateType:
                        dataList.append({
                            'stepsName': '????????????-Validate',
                            'errorMsg': f'???{index}???:????????????????????????!',
                            'updateTime': cls_Common.get_date_time()})
                    if not item_validate.valueType:
                        dataList.append({
                            'stepsName': '????????????-Validate',
                            'errorMsg': f'???{index}???:???????????????????????????!',
                            'updateTime': cls_Common.get_date_time()})
        # endregion
        # region ?????? ????????????
        if apiInfo.request.preOperation:
            for index, item_preOperation in enumerate(apiInfo.request.preOperation, 1):
                if item_preOperation.state:
                    if item_preOperation.operationType == 'Methods':
                        if not item_preOperation.methodsName:
                            dataList.append({
                                'stepsName': '????????????-????????????',
                                'errorMsg': f'???{index}???:??????????????????????????????!',
                                'updateTime': cls_Common.get_date_time()})
                        if '(' not in item_preOperation.methodsName or ')' not in item_preOperation.methodsName:
                            dataList.append({
                                'stepsName': '????????????-????????????',
                                'errorMsg': f'???{index}???:?????????????????????????????? ()',
                                'updateTime': cls_Common.get_date_time()})
                    elif item_preOperation.operationType == 'DataBase':
                        if not item_preOperation.dataBase:
                            dataList.append({
                                'stepsName': '????????????-????????????',
                                'errorMsg': f'???{index}???:??????????????????????????????????????????!',
                                'updateTime': cls_Common.get_date_time()})
                        if not item_preOperation.sql:
                            dataList.append({
                                'stepsName': '????????????-????????????',
                                'errorMsg': f'???{index}???:?????????SQL??????!',
                                'updateTime': cls_Common.get_date_time()})
        # endregion
        # region ?????? ????????????
        if apiInfo.request.rearOperation:
            for index, item_rearOperation in enumerate(apiInfo.request.rearOperation, 1):
                if item_rearOperation.state:
                    if item_rearOperation.operationType == 'Methods':
                        if not item_rearOperation.methodsName:
                            dataList.append({
                                'stepsName': '????????????-????????????',
                                'errorMsg': f'???{index}???:??????????????????????????????!',
                                'updateTime': cls_Common.get_date_time()})
                        if '(' not in item_rearOperation.methodsName or ')' not in item_rearOperation.methodsName:
                            dataList.append({
                                'stepsName': '????????????-????????????',
                                'errorMsg': f'???{index}???:?????????????????????????????? ()',
                                'updateTime': cls_Common.get_date_time()})
                    elif item_rearOperation.operationType == 'DataBase':
                        if not item_rearOperation.dataBase:
                            dataList.append({
                                'stepsName': '????????????-????????????',
                                'errorMsg': f'???{index}???:??????????????????????????????????????????!',
                                'updateTime': cls_Common.get_date_time()})
                        if not item_rearOperation.sql:
                            dataList.append({
                                'stepsName': '????????????-????????????',
                                'errorMsg': f'???{index}???:?????????SQL??????!',
                                'updateTime': cls_Common.get_date_time()})
        # endregion
        # region ??????params ???body ?????????1????????????
        if not apiInfo.request.params and \
                not apiInfo.request.body.formData and \
                not apiInfo.request.body.raw and \
                not apiInfo.request.body.json and \
                not apiInfo.request.body.requestSaveType == 'none':
            dataList.append({
                'stepsName': '????????????-????????????',
                'errorMsg': f'???????????????????????????,Params???Body??????????????????1???????????????!',
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
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])  # ???????????????
        basicInfo = objData.BasicInfo
        apiInfo = objData.ApiInfo
        if basicInfo.assignedUserId:
            assignedUserId = basicInfo.assignedUserId[1]
        else:
            assignedUserId = userId
        onlyCode = cls_Common.generate_only_code()
    except BaseException as e:
        errorMsg = f"????????????:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_IntMaintenance', 'data_save', errorMsg)
    else:
        obj_db_ApiBaseData = db_ApiBaseData.objects.filter(
            is_del=0, pid_id=basicInfo.proId, page_id=basicInfo.pageId, fun_id=basicInfo.funId,
            apiName=basicInfo.apiName, requestType=apiInfo.requestType,
            requestUrl=apiInfo.requestUrl._object_maker__data)
        if obj_db_ApiBaseData.exists():
            response['errorMsg'] = f'???????????????????????????????????????,???????????????????????????!'
        else:
            try:
                with transaction.atomic():  # ???????????????????????????python???????????????????????????
                    # region ????????????????????????
                    requestParamsType = cls_RequstOperation.for_data_get_requset_params_type(
                        apiInfo.request.params,
                        apiInfo.request.body.formData,
                        apiInfo.request.body.raw,
                        apiInfo.request.body.json)
                    # endregion
                    # region ??????????????????
                    operationInfoId = cls_Logging.record_operation_info(
                        'API', 'Manual', 3, 'Add',
                        cls_FindTable.get_pro_name(basicInfo.proId),
                        cls_FindTable.get_page_name(basicInfo.pageId),
                        cls_FindTable.get_fun_name(basicInfo.funId),
                        userId,
                        '??????????????????', CUFront=responseData
                    )
                    # endregion
                    # region ??????????????????
                    save_db_ApiBaseData = db_ApiBaseData.objects.create(
                        pid_id=basicInfo.proId, page_id=basicInfo.pageId, fun_id=basicInfo.funId,
                        apiName=basicInfo.apiName, environment_id=basicInfo.environmentId, apiState=basicInfo.apiState,
                        requestType=apiInfo.requestType, requestUrl=apiInfo.requestUrl._object_maker__data,
                        requestUrlRadio=apiInfo.requestUrlRadio,
                        requestParamsType='Body' if apiInfo.request.body.requestSaveType == 'none' else requestParamsType,
                        bodyRequestSaveType=apiInfo.request.body.requestSaveType,
                        uid_id=userId, cuid=userId, assignedToUser=assignedUserId, is_del=0, onlyCode=onlyCode,
                    )
                    # ??????????????????
                    product_list_to_insert = list()
                    for item_userId in basicInfo.pushTo:
                        product_list_to_insert.append(db_ApiAssociatedUser(
                            apiId_id=save_db_ApiBaseData.id,
                            opertateInfo_id=operationInfoId,
                            uid_id=item_userId[1],
                            is_del=0,
                            onlyCode=onlyCode)
                        )
                    db_ApiAssociatedUser.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region ??????????????????
                    restoreData = responseData
                    restoreData['BasicInfo']['updateTime'] = save_db_ApiBaseData.updateTime.strftime(
                        '%Y-%m-%d %H:%M:%S')
                    restoreData['BasicInfo']['createTime'] = save_db_ApiBaseData.createTime.strftime(
                        '%Y-%m-%d %H:%M:%S')
                    restoreData['BasicInfo']['uid_id'] = save_db_ApiBaseData.uid_id
                    restoreData['BasicInfo']['cuid'] = save_db_ApiBaseData.cuid
                    restoreData['onlyCode'] = onlyCode
                    db_ApiHistory.objects.create(
                        pid_id=basicInfo.proId,
                        page_id=basicInfo.pageId,
                        fun_id=basicInfo.funId,
                        api_id=save_db_ApiBaseData.id,
                        apiName=basicInfo.apiName,
                        operationType='Add',
                        restoreData=restoreData,
                        onlyCode=onlyCode,
                        uid_id=userId,
                    )
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
                            is_del=0,
                            onlyCode=onlyCode)
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
                            is_del=0,
                            onlyCode=onlyCode)
                        )
                    db_ApiParams.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region Body
                    # region ?????????????????????????????????????????????
                    deleteFileList = apiInfo.request.body.deleteFileList
                    for item_delFile in deleteFileList:
                        if item_delFile.dirName == 'Temp':
                            filePath = settings.TEMP_PATH
                        else:
                            filePath = f"{settings.APIFILE_PATH}{item_delFile.dirName}"
                        cls_FileOperations.delete_file(f"{filePath}{item_delFile.fileName}")
                    # endregion
                    if apiInfo.request.body.requestSaveType == 'form-data':
                        product_list_to_insert = list()
                        for item_body in apiInfo.request.body.formData:
                            paramsType = item_body.paramsType
                            if paramsType == 'Text':
                                pass
                            else:  # file
                                # region file????????????
                                filePath = None
                                # fileMD5 = None
                                fileData = item_body.fileList[0]._object_maker__data
                                fileName = fileData['name']
                                # ???????????????
                                newFolder = cls_FileOperations.new_folder(
                                    f'{settings.APIFILE_PATH}{save_db_ApiBaseData.id}')
                                if newFolder['state']:
                                    # ??????????????????????????????????????????
                                    copyFile = cls_FileOperations.copy_file_to_dir(
                                        f'{settings.TEMP_PATH}{fileName}', newFolder['path'])
                                    if copyFile['state']:
                                        filePath = copyFile['newFilePath']
                                        # fileMD5 = cls_Common.get_file_md5(filePath)
                                    else:
                                        response['errorMsg'] = copyFile['errorMsg']
                                        # ????????????????????????
                                        cls_FileOperations.delete_folder(newFolder['path'])
                                        return response
                                else:
                                    response['errorMsg'] = newFolder['errorMsg']
                                    return response
                                # endregion
                            product_list_to_insert.append(db_ApiBody(
                                apiId_id=save_db_ApiBaseData.id,
                                index=item_body.index,
                                key=item_body.key,
                                paramsType=item_body.paramsType,
                                value=item_body.value,
                                filePath=filePath,
                                # fileMD5=fileMD5,
                                remarks=item_body.remarks,
                                state=1 if item_body.state else 0,
                                is_del=0,
                                onlyCode=onlyCode)
                            )
                        db_ApiBody.objects.bulk_create(product_list_to_insert)
                    elif apiInfo.request.body.requestSaveType in ['raw', 'json']:
                        if apiInfo.request.body.requestSaveType == 'raw':
                            value = apiInfo.request.body.raw
                        elif apiInfo.request.body.requestSaveType == 'json':
                            value = apiInfo.request.body.json
                        else:
                            value = None
                        db_ApiBody.objects.create(
                            apiId_id=save_db_ApiBaseData.id,
                            index=0,
                            key=None,
                            value=value,
                            state=1,
                            is_del=0,
                            onlyCode=onlyCode
                        )
                    # file ????????????
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
                            is_del=0,
                            onlyCode=onlyCode)
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
                            is_del=0,
                            onlyCode=onlyCode)
                        )
                    db_ApiValidate.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region ??????
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
                            is_del=0,
                            onlyCode=onlyCode)
                        )
                    db_ApiOperation.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region ??????
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
                            is_del=0,
                            onlyCode=onlyCode)
                        )
                    db_ApiOperation.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region ????????????????????????????????????
                    obj_db_ApiAssociatedUser = db_ApiAssociatedUser.objects.filter(
                        is_del=0, apiId_id=save_db_ApiBaseData.id, onlyCode=onlyCode)
                    for item_associatedUser in obj_db_ApiAssociatedUser:
                        cls_Logging.push_to_user(operationInfoId, item_associatedUser.uid_id)
                    # endregion
            except BaseException as e:  # ????????????????????????????????????
                response['errorMsg'] = f'????????????:{e}'
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
        requestUrlRadio = apiInfo.requestUrlRadio
        if basicInfo.assignedUserId:
            assignedUserId = basicInfo.assignedUserId[1]
        else:
            assignedUserId = userId
        onlyCode = cls_Common.generate_only_code()
    except BaseException as e:
        errorMsg = f"????????????:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_IntMaintenance', 'edit_data', errorMsg)
    else:
        obj_db_ApiBaseData = db_ApiBaseData.objects.filter(id=basicInfo.apiId, is_del=0)
        if obj_db_ApiBaseData.exists():
            try:
                with transaction.atomic():  # ???????????????????????????python???????????????????????????
                    requestParamsType = cls_RequstOperation.for_data_get_requset_params_type(
                        apiInfo.request.params, apiInfo.request.body.formData,
                        apiInfo.request.body.raw, apiInfo.request.body.json)
                    # region ??????????????????
                    # region ?????????????????????
                    headers = []
                    params = []
                    body = []
                    extract = []
                    validate = []
                    preOperation = []
                    rearOperation = []
                    # region ????????????
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
                    elif obj_db_ApiBaseData[0].bodyRequestSaveType in ['raw', 'json']:
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
                    # region ????????????
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
                    # region ????????????
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
                    obj_db_ApiAssociatedUser = db_ApiAssociatedUser.objects.filter(is_del=0, apiId_id=basicInfo.apiId)
                    pushTo = [i.uid_id for i in obj_db_ApiAssociatedUser]
                    oldData = {
                        'BasicInfo': {
                            'apiId': basicInfo.apiId,
                            'proId': str(obj_db_ApiBaseData[0].pid_id),
                            'pageId': obj_db_ApiBaseData[0].page_id,
                            'funId': obj_db_ApiBaseData[0].fun_id,
                            'environmentId': obj_db_ApiBaseData[0].environment_id,
                            'apiName': obj_db_ApiBaseData[0].apiName,
                            'apiState': obj_db_ApiBaseData[0].apiState,
                            'assignedUserId': obj_db_ApiBaseData[0].uid_id,
                            'pushTo': pushTo,
                        },
                        'ApiInfo': {
                            'requestType': obj_db_ApiBaseData[0].requestType,
                            'requestUrlRadio': obj_db_ApiBaseData[0].requestUrlRadio,
                            'requestUrl': ast.literal_eval(obj_db_ApiBaseData[0].requestUrl),
                            'request': {
                                'headers': headers,
                                'params': params,
                                'body': {
                                    'requestSaveType': obj_db_ApiBaseData[0].bodyRequestSaveType,
                                    'formData': bodyData,
                                    'raw': bodyData if obj_db_ApiBaseData[0].bodyRequestSaveType == 'raw' else '',
                                    'json': bodyData if obj_db_ApiBaseData[0].bodyRequestSaveType == 'json' else '',
                                },
                                'extract': extract,
                                'validate': validate,
                                'preOperation': preOperation,
                                'rearOperation': rearOperation,
                            }
                        },
                        # 'cuid': obj_db_ApiBaseData[0].cuid
                    }
                    # endregion
                    operationInfoId = cls_Logging.record_operation_info(
                        'API', 'Manual', 3, 'Edit',
                        cls_FindTable.get_pro_name(basicInfo.proId),
                        cls_FindTable.get_page_name(basicInfo.pageId),
                        cls_FindTable.get_fun_name(basicInfo.funId),
                        userId,
                        f'?????????????????? ID{obj_db_ApiBaseData[0].id}:{obj_db_ApiBaseData[0].apiName}',
                        CUFront=oldData, CURear=responseData
                    )
                    # region ??????????????????????????? -?????????

                    # save_db_WorkorderManagement = db_WorkorderManagement.objects.create(
                    #     sysType='API', pid_id=basicInfo.proId, page_id=basicInfo.pageId, fun_id=basicInfo.funId,
                    #     workSource=1, workType='Edit', workState=0, workName=f'????????????:{basicInfo.apiName}',
                    #     message=apiEditDfif,
                    #     # message=f"{oldData}\n\n{responseData}",
                    #     uid_id=userId,
                    #     cuid=userId,
                    #     is_del=0,
                    # )
                    # ????????????????????????
                    # db_WorkLifeCycle.objects.create(
                    #     work_id=save_db_WorkorderManagement.id, workState=1, operationType='Add',
                    #     operationInfo=None, uid_id=userId, is_del=0,
                    # )
                    # endregion
                    # endregion
                    # region ?????? ???????????????
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
                    # region ??????????????????
                    obj_db_ApiBaseData.update(
                        pid_id=basicInfo.proId, page_id=basicInfo.pageId, fun_id=basicInfo.funId,
                        apiName=basicInfo.apiName, environment_id=basicInfo.environmentId, apiState=basicInfo.apiState,
                        requestType=apiInfo.requestType, requestUrl=apiInfo.requestUrl._object_maker__data,
                        requestUrlRadio=requestUrlRadio,
                        requestParamsType='Body' if apiInfo.request.body.requestSaveType == 'none' else requestParamsType,
                        bodyRequestSaveType=apiInfo.request.body.requestSaveType,
                        uid_id=userId, assignedToUser=assignedUserId,
                        is_del=0, updateTime=cls_Common.get_date_time(), onlyCode=onlyCode
                    )
                    product_list_to_insert = list()
                    for item_userId in basicInfo.pushTo:
                        product_list_to_insert.append(db_ApiAssociatedUser(
                            apiId_id=basicInfo.apiId,
                            opertateInfo_id=operationInfoId,
                            uid_id=item_userId[1],
                            is_del=0,
                            onlyCode=onlyCode)
                        )
                    db_ApiAssociatedUser.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region ??????????????????
                    apiEditDfif = cls_RequstOperation.api_edit_dfif(oldData, responseData)
                    restoreData = responseData
                    restoreData['BasicInfo']['updateTime'] = obj_db_ApiBaseData[0].updateTime.strftime(
                        '%Y-%m-%d %H:%M:%S')
                    restoreData['BasicInfo']['createTime'] = obj_db_ApiBaseData[0].createTime.strftime(
                        '%Y-%m-%d %H:%M:%S')
                    restoreData['BasicInfo']['uid_id'] = obj_db_ApiBaseData[0].uid_id
                    restoreData['BasicInfo']['cuid'] = obj_db_ApiBaseData[0].cuid
                    restoreData['onlyCode'] = onlyCode
                    db_ApiHistory.objects.create(
                        pid_id=basicInfo.proId,
                        page_id=basicInfo.pageId,
                        fun_id=basicInfo.funId,
                        api_id=basicInfo.apiId,
                        apiName=basicInfo.apiName,
                        operationType='Edit',
                        restoreData=restoreData,
                        textInfo=apiEditDfif,
                        onlyCode=onlyCode,
                        uid_id=userId,
                    )
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
                            is_del=0,
                            onlyCode=onlyCode)
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
                            is_del=0,
                            onlyCode=onlyCode)
                        )
                    db_ApiParams.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region Body
                    # region ?????????????????????????????????????????????
                    deleteFileList = apiInfo.request.body.deleteFileList
                    for item_delFile in deleteFileList:
                        if item_delFile.dirName == 'Temp':
                            filePath = settings.TEMP_PATH
                        else:
                            filePath = f"{settings.APIFILE_PATH}{item_delFile.dirName}/"
                        cls_FileOperations.delete_file(f"{filePath}{item_delFile.fileName}")
                    # endregion
                    if apiInfo.request.body.requestSaveType == 'form-data':
                        product_list_to_insert = list()
                        for item_body in apiInfo.request.body.formData:
                            paramsType = item_body.paramsType
                            if paramsType == 'Text':
                                filePath = None
                            else:  # file
                                # region file????????????
                                fileData = item_body.fileList[0]._object_maker__data
                                fileName = fileData['name']
                                tempUrl = fileData['url'].replace(
                                    settings.NGINX_SERVER, f"{settings.BASE_DIR._str}/_DataFiles/")
                                dirType = 'Temp' if 'Temp' in tempUrl else 'Case'
                                if dirType == 'Temp':  # ????????????
                                    # ???????????????
                                    newFolder = cls_FileOperations.new_folder(
                                        f'{settings.APIFILE_PATH}{basicInfo.apiId}')
                                    if newFolder['state']:
                                        # ??????????????????????????????????????????
                                        copyFile = cls_FileOperations.copy_file_to_dir(
                                            f'{settings.TEMP_PATH}{fileName}', newFolder['path'])
                                        if copyFile['state']:
                                            filePath = copyFile['newFilePath']
                                        else:
                                            response['errorMsg'] = copyFile['errorMsg']
                                            # ????????????????????????
                                            cls_FileOperations.delete_folder(newFolder['path'])
                                            raise FileExistsError(copyFile['errorMsg'])
                                    else:
                                        response['errorMsg'] = newFolder['errorMsg']
                                        raise FileExistsError(newFolder['errorMsg'])
                                else:
                                    filePath = tempUrl

                                # endregion
                            product_list_to_insert.append(db_ApiBody(
                                apiId_id=basicInfo.apiId,
                                index=item_body.index,
                                key=item_body.key,
                                paramsType=item_body.paramsType,
                                value=item_body.value,
                                filePath=filePath,
                                # fileMD5=fileMD5,
                                remarks=item_body.remarks,
                                state=1 if item_body.state else 0,
                                is_del=0,
                                onlyCode=onlyCode)
                            )
                        db_ApiBody.objects.bulk_create(product_list_to_insert)
                    elif apiInfo.request.body.requestSaveType in ['raw', 'json']:
                        db_ApiBody.objects.filter(is_del=0, apiId_id=basicInfo.apiId).update(
                            updateTime=cls_Common.get_date_time(), is_del=1
                        )
                        if apiInfo.request.body.requestSaveType == 'raw':
                            value = apiInfo.request.body.raw
                        elif apiInfo.request.body.requestSaveType == 'json':
                            value = apiInfo.request.body.json
                        else:
                            value = None
                        db_ApiBody.objects.create(
                            apiId_id=basicInfo.apiId,
                            index=0,
                            key=None,
                            value=value,
                            state=1,
                            is_del=0,
                            onlyCode=onlyCode
                        )
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
                            is_del=0,
                            onlyCode=onlyCode)
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
                            is_del=0,
                            onlyCode=onlyCode)
                        )
                    db_ApiValidate.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region ??????
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
                            is_del=0,
                            onlyCode=onlyCode)
                        )
                    db_ApiOperation.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region ??????
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
                            is_del=0,
                            onlyCode=onlyCode)
                        )
                    db_ApiOperation.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region ????????????????????????????????????
                    obj_db_ApiAssociatedUser = db_ApiAssociatedUser.objects.filter(
                        is_del=0, apiId_id=basicInfo.apiId)
                    for item_associatedUser in obj_db_ApiAssociatedUser:
                        # db_WorkBindPushToUsers.objects.create(
                        #     work_id=save_db_WorkorderManagement.id,
                        #     uid_id=item_associatedUser.uid_id,
                        #     is_del=0
                        # )
                        cls_Logging.push_to_user(operationInfoId, item_associatedUser.uid_id)
                    # endregion
                    # region ????????????????????????,???????????????????????????
                    obj_db_CaseTestSet = db_CaseTestSet.objects.filter(
                        is_del=0, apiId_id=basicInfo.apiId, is_synchronous=1)
                    product_list_to_insert = list()
                    for item_testSet in obj_db_CaseTestSet:
                        obj_db_ApiDynamic = db_ApiDynamic.objects.filter(
                            is_del=0, apiId_id=basicInfo.apiId, case_id=item_testSet.caseId_id, is_read=0)
                        if obj_db_ApiDynamic.exists():
                            obj_db_ApiDynamic.update(updateTime=cls_Common.get_date_time(), uid_id=userId)
                        else:
                            product_list_to_insert.append(db_ApiDynamic(
                                apiId_id=basicInfo.apiId,
                                case_id=item_testSet.caseId_id,
                                uid_id=userId,
                                cuid=userId,
                                is_read=0,
                                is_del=0,
                            ))
                    db_ApiDynamic.objects.bulk_create(product_list_to_insert)
                    # endregion
            except BaseException as e:  # ????????????????????????????????????
                response['errorMsg'] = f'??????????????????:{e}'
            else:
                response['statusCode'] = 2002
        else:
            response['errorMsg'] = '????????????????????????,????????????????????????!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def delete_data(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        apiId = request.POST['apiId']
        onlyCode = cls_Common.generate_only_code()
    except BaseException as e:
        errorMsg = f"????????????:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_IntMaintenance', 'delete_data', errorMsg)
    else:
        obj_db_ApiBaseData = db_ApiBaseData.objects.filter(id=apiId)
        if obj_db_ApiBaseData.exists():
            obj_db_CaseTestSet = db_CaseTestSet.objects.filter(is_del=0, apiId_id=apiId)
            if obj_db_CaseTestSet.exists():
                caseTable = [i.caseId.caseName for i in obj_db_CaseTestSet]
                caseTable = set(caseTable)
                response['errorMsg'] = '???????????????????????????,???????????????????????????????????????!' \
                                       f'????????????:{caseTable}'
            else:
                try:
                    with transaction.atomic():  # ???????????????????????????python???????????????????????????
                        # region ??????????????????
                        db_ApiHistory.objects.create(
                            pid_id=obj_db_ApiBaseData[0].pid_id,
                            page_id=obj_db_ApiBaseData[0].page_id,
                            fun_id=obj_db_ApiBaseData[0].fun_id,
                            api_id=apiId,
                            apiName=obj_db_ApiBaseData[0].apiName,
                            operationType='Delete',
                            onlyCode=onlyCode,
                            uid_id=userId,
                        )
                        # endregion
                        # region ??????????????????
                        obj_db_ApiBaseData.update(
                            is_del=1, updateTime=cls_Common.get_date_time(), uid_id=userId)
                        db_ApiAssociatedUser.objects.filter(is_del=0, apiId_id=apiId).update(
                            is_del=1, updateTime=cls_Common.get_date_time())
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
                        # endregion
                        # region ??????File????????????????????????
                        sourcePath = f"{settings.APIFILE_PATH}{apiId}"
                        targetPath = f"{settings.BAKDATA_PATH}ApiFile/{apiId}"
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
                        # region ??????????????????
                        cls_Logging.record_operation_info(
                            'API', 'Manual', 3, 'Delete',
                            cls_FindTable.get_pro_name(obj_db_ApiBaseData[0].pid_id),
                            cls_FindTable.get_page_name(obj_db_ApiBaseData[0].page_id),
                            cls_FindTable.get_fun_name(obj_db_ApiBaseData[0].fun_id),
                            userId,
                            f'?????????????????? ID:{apiId}:{obj_db_ApiBaseData[0].apiName}',
                            CUFront=json.dumps(request.POST)
                        )
                        # endregion
                except BaseException as e:  # ????????????????????????????????????
                    response['errorMsg'] = f'??????????????????:{e}'
                else:
                    response['statusCode'] = 2003
        else:
            response['errorMsg'] = '???????????????????????????,????????????????????????!'
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
    preOperation = []  # ????????????
    rearOperation = []  # ????????????
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        apiId = objData.apiId
    except BaseException as e:
        errorMsg = f"????????????:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_IntMaintenance', 'load_data', errorMsg)
    else:
        obj_db_ApiBaseData = db_ApiBaseData.objects.filter(is_del=0, id=apiId)
        if obj_db_ApiBaseData.exists():
            # region ????????????
            roleId = cls_FindTable.get_roleId(obj_db_ApiBaseData[0].assignedToUser)
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
                'assignedUserId': [roleId, obj_db_ApiBaseData[0].assignedToUser],
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
            elif obj_db_ApiBaseData[0].bodyRequestSaveType in ['raw', 'json']:
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
            # region ????????????
            obj_db_ApiOperation = db_ApiOperation.objects.filter(
                is_del=0, apiId_id=apiId, location='Pre').order_by('index')
            for item_preOperation in obj_db_ApiOperation:
                preOperation.append({
                    'index': item_preOperation.index,
                    'operationType': item_preOperation.operationType,
                    'methodsName': item_preOperation.methodsName,
                    'dataBase': ast.literal_eval(
                        item_preOperation.dataBaseId) if item_preOperation.dataBaseId else None,
                    'sql': item_preOperation.sql,
                    'remarks': item_preOperation.remarks,
                    'state': True if item_preOperation.state else False,
                })
            # endregion
            # region ????????????
            obj_db_ApiOperation = db_ApiOperation.objects.filter(
                is_del=0, apiId_id=apiId, location='Rear').order_by('index')
            for item_rearOperation in obj_db_ApiOperation:
                rearOperation.append({
                    'index': item_rearOperation.index,
                    'operationType': item_rearOperation.operationType,
                    'methodsName': item_rearOperation.methodsName,
                    'dataBase': ast.literal_eval(
                        item_rearOperation.dataBaseId) if item_rearOperation.dataBaseId else None,
                    'sql': item_rearOperation.sql,
                    'remarks': item_rearOperation.remarks,
                    'state': True if item_rearOperation.state else False,
                })
            # endregion
            # region apiInfo
            requestUrlRadio = obj_db_ApiBaseData[0].requestUrlRadio
            requestUrl = ast.literal_eval(obj_db_ApiBaseData[0].requestUrl)
            currentRequestUrl = requestUrl[f'url{requestUrlRadio}']
            apiInfo = {
                'requestType': obj_db_ApiBaseData[0].requestType,
                'requestUrlRadio': requestUrlRadio,
                'currentRequestUrl': currentRequestUrl,
                'requestUrl1': requestUrl['url1'],
                'requestUrl2': requestUrl['url2'],
                'requestUrl3': requestUrl['url3'],
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
            response['errorMsg'] = "????????????????????????????????????,????????????????????????!"
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
        errorMsg = f"????????????:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_IntMaintenance', 'request_api', errorMsg)
    else:
        cls_Logging.print_log('info', 'send_request', '-----------------------------start-----------------------------')
        obj_db_ApiBaseData = db_ApiBaseData.objects.filter(id=apiId)
        if obj_db_ApiBaseData.exists():
            queueState = cls_FindTable.get_queue_state('API', apiId)
            if queueState:
                response['errorMsg'] = '?????????????????????????????????,??????????????????!???????????????????????????????????????????????????!' \
                                       '???????????????????????????????????????????????????!'
            else:
                remindLabel = f"?????????:{obj_db_ApiBaseData[0].apiName}???:"  # ???????????????
                # region ??????1????????????
                createTestReport = cls_ApiReport.create_test_report(
                    obj_db_ApiBaseData[0].pid_id,
                    obj_db_ApiBaseData[0].apiName,
                    'API', apiId, 1, userId
                )
                # endregion
                if createTestReport['state']:
                    # region  ??????2?????????
                    testReportId = createTestReport['testReportId']
                    # region ????????????
                    queueId = cls_ApiReport.create_queue(
                        obj_db_ApiBaseData[0].pid_id, obj_db_ApiBaseData[0].page_id, obj_db_ApiBaseData[0].fun_id
                        , 'API', apiId, testReportId, userId)
                    # endregion
                    apiName = obj_db_ApiBaseData[0].apiName
                    createReportItems = cls_ApiReport.create_report_items(testReportId, apiId, apiName)
                    if createReportItems['state']:
                        reportItemId = createReportItems['reportItemId']
                        cls_ApiReport.update_queue(queueId, 1, userId)
                        # ????????????
                        response = cls_RequstOperation.execute_api(
                            False, onlyCode, userId,
                            apiId=apiId, environmentId=environmentId,
                            testReportId=testReportId, reportItemId=reportItemId, labelName=remindLabel)
                        if response['state']:
                            response['statusCode'] = 2000
                        else:
                            response['errorMsg'] = response['errorMsg']
                        cls_ApiReport.update_report_items(testReportId, reportItemId)  # ??????2?????????
                        cls_ApiReport.update_queue(queueId, 2, userId)  # ????????????
                    else:
                        response['errorMsg'] = createReportItems['errorMsg']
                    # endregion
                else:
                    response['errorMsg'] = createTestReport['errorMsg']
        else:
            response['errorMsg'] = '??????????????????????????????,???????????????????????????'
        cls_Logging.print_log('info', 'send_request', '-----------------------------END-----------------------------')
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def send_test_request(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        responseData = json.loads(request.body)
        # ???????????????????????????,???????????????????????????
        # objData = cls_object_maker(responseData)
        onlyCode = cls_Common.generate_only_code()
        testSendData = responseData['testSendData']
    except BaseException as e:
        errorMsg = f"????????????:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_IntMaintenance', 'request_api', errorMsg)
    else:
        cls_Logging.print_log('info', 'send_request', '-----------------------------start-----------------------------')
        # ????????????URl
        obj_db_PageEnvironment = db_PageEnvironment.objects.filter(id=testSendData['BasicInfo']['environmentId'])
        if obj_db_PageEnvironment.exists():
            environmentUrl = obj_db_PageEnvironment[0].environmentUrl
            request = cls_object_maker(testSendData['ApiInfo']['request'])
            requestParamsType = cls_RequstOperation.for_data_get_requset_params_type(
                request.params, request.body.formData, request.body.raw, request.body.json,
            )
            requestParamsType = 'Body' if testSendData['ApiInfo']['request']['body'][
                                              'requestSaveType'] == 'none' else requestParamsType
            bodyRequestType = testSendData['ApiInfo']['request']['body']['requestSaveType']
            if bodyRequestType == 'form-data':
                bodyData = testSendData['ApiInfo']['request']['body']['formData']
            elif bodyRequestType == 'raw':
                bodyData = testSendData['ApiInfo']['request']['body']['raw']
            elif bodyRequestType == 'json':
                bodyData = testSendData['ApiInfo']['request']['body']['json']
            else:
                bodyData = []
            requestUrlRadio = testSendData["ApiInfo"]["requestUrlRadio"]
            requestUrl = testSendData["ApiInfo"]["requestUrl"][f'url{requestUrlRadio}']
            requestData = {
                'state': True,
                'proId': testSendData['BasicInfo']['proId'],
                'requestType': testSendData['ApiInfo']['requestType'],
                'requestUrl': f'{environmentUrl}{requestUrl}',
                'environmentUrl': environmentUrl,
                'apiUrl': requestUrl,
                'requestParamsType': requestParamsType,
                'bodyRequestType': bodyRequestType,
                'headersData': testSendData['ApiInfo']['request']['headers'],
                'paramsData': testSendData['ApiInfo']['request']['params'],
                'bodyData': bodyData,
                'extractData': testSendData['ApiInfo']['request']['extract'],
                'validateData': testSendData['ApiInfo']['request']['validate'],
                'PreOperation': testSendData['ApiInfo']['request']['preOperation'],
                'RearOperation': testSendData['ApiInfo']['request']['rearOperation'],
            }
            response = cls_RequstOperation.execute_api(True, onlyCode, userId, requestData=requestData)
            if response['state']:
                response['statusCode'] = 2000
        else:
            response['errorMsg'] = f"????????????????????????ID???????????????!"
        cls_Logging.print_log('info', 'send_request', '-----------------------------END-----------------------------')
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def copy_api(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])  # ???????????????
        apiId = objData.apiId
    except BaseException as e:
        errorMsg = f"????????????:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_IntMaintenance', 'copy_api', errorMsg)
    else:
        obj_db_ApiBaseData = db_ApiBaseData.objects.filter(is_del=0, id=apiId)
        if obj_db_ApiBaseData.exists():
            try:
                with transaction.atomic():  # ???????????????????????????python???????????????????????????
                    # region ??????????????????
                    operationInfoId = cls_Logging.record_operation_info(
                        'API', 'Manual', 3, 'Add',
                        cls_FindTable.get_pro_name(obj_db_ApiBaseData[0].pid_id),
                        cls_FindTable.get_page_name(obj_db_ApiBaseData[0].page_id),
                        cls_FindTable.get_fun_name(obj_db_ApiBaseData[0].fun_id),
                        userId,
                        '??????????????????', CUFront=f"ID:{apiId},{obj_db_ApiBaseData[0].apiName}"
                    )
                    # endregion
                    # region ??????????????????
                    save_db_ApiBaseData = db_ApiBaseData.objects.create(
                        pid_id=obj_db_ApiBaseData[0].pid_id,
                        page_id=obj_db_ApiBaseData[0].page_id,
                        fun_id=obj_db_ApiBaseData[0].fun_id,
                        apiName=f"{obj_db_ApiBaseData[0].apiName}-??????{operationInfoId}",
                        environment_id=obj_db_ApiBaseData[0].environment_id,
                        apiState=obj_db_ApiBaseData[0].apiState,
                        requestType=obj_db_ApiBaseData[0].requestType,
                        requestUrl=obj_db_ApiBaseData[0].requestUrl,
                        requestParamsType=obj_db_ApiBaseData[0].requestParamsType,
                        bodyRequestSaveType=obj_db_ApiBaseData[0].bodyRequestSaveType,
                        uid_id=userId, cuid=userId, is_del=0,
                    )
                    obj_db_ApiAssociatedUser = db_ApiAssociatedUser.objects.filter(apiId_id=apiId, is_del=0)
                    product_list_to_insert = list()
                    for item_userId in obj_db_ApiAssociatedUser:
                        product_list_to_insert.append(db_ApiAssociatedUser(
                            apiId_id=save_db_ApiBaseData.id,
                            opertateInfo_id=item_userId.opertateInfo_id,
                            uid_id=item_userId.uid_id,
                            is_del=0)
                        )
                    db_ApiAssociatedUser.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region Headers
                    obj_db_ApiHeaders = db_ApiHeaders.objects.filter(apiId_id=apiId, is_del=0)
                    product_list_to_insert = list()
                    for item_headers in obj_db_ApiHeaders:
                        product_list_to_insert.append(db_ApiHeaders(
                            apiId_id=save_db_ApiBaseData.id,
                            index=item_headers.index,
                            key=item_headers.key,
                            value=item_headers.value,
                            remarks=item_headers.remarks,
                            state=item_headers.state,
                            is_del=0)
                        )
                    db_ApiHeaders.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region Params
                    obj_db_ApiParams = db_ApiParams.objects.filter(apiId_id=apiId, is_del=0)
                    product_list_to_insert = list()
                    for item_params in obj_db_ApiParams:
                        product_list_to_insert.append(db_ApiParams(
                            apiId_id=save_db_ApiBaseData.id,
                            index=item_params.index,
                            key=item_params.key,
                            value=item_params.value,
                            remarks=item_params.remarks,
                            state=item_params.state,
                            is_del=0)
                        )
                    db_ApiParams.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region Body
                    obj_db_ApiBody = db_ApiBody.objects.filter(apiId_id=apiId, is_del=0)
                    if obj_db_ApiBaseData[0].bodyRequestSaveType == 'form-data':
                        product_list_to_insert = list()
                        for item_body in obj_db_ApiBody:
                            product_list_to_insert.append(db_ApiBody(
                                apiId_id=save_db_ApiBaseData.id,
                                index=item_body.index,
                                key=item_body.key,
                                value=item_body.value,
                                remarks=item_body.remarks,
                                state=item_body.state,
                                is_del=0)
                            )
                        db_ApiBody.objects.bulk_create(product_list_to_insert)
                    elif obj_db_ApiBaseData[0].bodyRequestSaveType == 'raw':
                        if obj_db_ApiBody.exists():
                            db_ApiBody.objects.create(
                                apiId_id=save_db_ApiBaseData.id,
                                index=0,
                                key=None,
                                value=obj_db_ApiBody[0].value,
                                state=1,
                                is_del=0
                            )
                    # file ????????????
                    # endregion
                    # region Extract
                    obj_db_ApiExtract = db_ApiExtract.objects.filter(apiId_id=apiId, is_del=0)
                    product_list_to_insert = list()
                    for item_extract in obj_db_ApiExtract:
                        product_list_to_insert.append(db_ApiExtract(
                            apiId_id=save_db_ApiBaseData.id,
                            index=item_extract.index,
                            key=item_extract.key,
                            value=item_extract.value,
                            remarks=item_extract.remarks,
                            state=item_extract.state,
                            is_del=0)
                        )
                    db_ApiExtract.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region Validate
                    obj_db_ApiValidate = db_ApiValidate.objects.filter(apiId_id=apiId, is_del=0)
                    product_list_to_insert = list()
                    for item_validate in obj_db_ApiValidate:
                        product_list_to_insert.append(db_ApiValidate(
                            apiId_id=save_db_ApiBaseData.id,
                            index=item_validate.index,
                            checkName=item_validate.checkName,
                            validateType=item_validate.validateType,
                            valueType=item_validate.valueType,
                            expectedResults=item_validate.expectedResults,
                            remarks=item_validate.remarks,
                            state=item_validate.state,
                            is_del=0)
                        )
                    db_ApiValidate.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region ?????????
                    obj_db_ApiOperation = db_ApiOperation.objects.filter(apiId_id=apiId, is_del=0)
                    product_list_to_insert = list()
                    for item_preOperation in obj_db_ApiOperation:
                        product_list_to_insert.append(db_ApiOperation(
                            apiId_id=save_db_ApiBaseData.id,
                            index=item_preOperation.index,
                            location=item_preOperation.location,
                            operationType=item_preOperation.operationType,
                            methodsName=item_preOperation.methodsName,
                            dataBaseId=item_preOperation.dataBaseId,
                            sql=item_preOperation.sql,
                            remarks=item_preOperation.remarks,
                            state=item_preOperation.state,
                            is_del=0)
                        )
                    db_ApiOperation.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # # region ????????????????????????????????????
                    # obj_db_ApiAssociatedUser = db_ApiAssociatedUser.objects.filter(
                    #     is_del=0, apiId_id=save_db_ApiBaseData.id)
                    # for item_associatedUser in obj_db_ApiAssociatedUser:
                    #     cls_Logging.push_to_user(operationInfoId, item_associatedUser.uid_id)
                    # # endregion
            except BaseException as e:  # ????????????????????????????????????
                response['errorMsg'] = f"??????????????????:{e}"
            else:
                response['statusCode'] = 2000
        else:
            response['errorMsg'] = "????????????????????????????????????,????????????????????????!"
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # ??????????????????
def select_history(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)

        apiId = objData.apiId
        pageId = objData.pageId
        funId = objData.funId
        apiName = objData.apiName
        operationType = objData.operationType

        current = int(objData.current)  # ????????????
        pageSize = int(objData.pageSize)  # ???????????????
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"????????????:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_IntMaintenance', 'select_history', errorMsg)
    else:
        if apiId:
            obj_db_ApiHistory = db_ApiHistory.objects.filter(api_id=apiId).order_by('-createTime')
        else:
            obj_db_ApiHistory = db_ApiHistory.objects.filter().order_by('-createTime')
        if pageId:
            obj_db_ApiHistory = obj_db_ApiHistory.filter(page_id=pageId).order_by('-createTime')
        if funId:
            obj_db_ApiHistory = obj_db_ApiHistory.filter(fun_id=funId).order_by('-createTime')
        if apiName:
            obj_db_ApiHistory = obj_db_ApiHistory.filter(apiName__icontains=apiName).order_by('-createTime')
        if operationType:
            obj_db_ApiHistory = obj_db_ApiHistory.filter(operationType=operationType).order_by('-createTime')
        select_db_ApiHistory = obj_db_ApiHistory[minSize: maxSize]
        for i in select_db_ApiHistory:
            if i.restoreData:
                restoreData = json.dumps(ast.literal_eval(i.restoreData),
                                         sort_keys=True, indent=4, separators=(",", ": "), ensure_ascii=False)
            else:
                restoreData = None
            if restoreData:
                tableItem = [{'restoreData': restoreData, 'textInfo': i.textInfo}]
            else:
                tableItem = []
            dataList.append({
                'id': i.id,
                'pageName': i.page.pageName,
                'funName': i.fun.funName,
                'apiName': i.apiName,
                'operationType': i.operationType,
                'tableItem': tableItem,
                'createTime': str(i.createTime.strftime('%Y-%m-%d %H:%M:%S')),
                "userName": f"{i.uid.userName}({i.uid.nickName})",
            })
        response['TableData'] = dataList
        response['Total'] = obj_db_ApiHistory.count()
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # ???????????? ??????????????????????????????????????????????????????
def restor_data(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        roleId = cls_FindTable.get_roleId(userId)
        is_admin = cls_FindTable.get_role_is_admin(roleId)
        historyId = request.POST['historyId']
    except BaseException as e:
        errorMsg = f"????????????:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_IntMaintenance', 'restor_data', errorMsg)
    else:
        obj_db_ApiHistory = db_ApiHistory.objects.filter(id=historyId)
        if obj_db_ApiHistory.exists():
            onlyCode = obj_db_ApiHistory[0].onlyCode
            # ??????????????????????????? ???????????????????????????????????????
            if is_admin or obj_db_ApiHistory[0].api.cuid == userId:
                try:
                    with transaction.atomic():  # ???????????????????????????python???????????????????????????
                        obj_db_ProManagement = db_ProManagement.objects.filter(is_del=0, id=obj_db_ApiHistory[0].pid_id)
                        if obj_db_ProManagement.exists():
                            obj_db_PageManagement = db_PageManagement.objects.filter(
                                is_del=0, id=obj_db_ApiHistory[0].page_id)
                            if obj_db_PageManagement.exists():
                                obj_db_FunManagement = db_FunManagement.objects.filter(
                                    is_del=0, id=obj_db_ApiHistory[0].fun_id)
                                if obj_db_FunManagement.exists():
                                    apiId = obj_db_ApiHistory[0].api_id
                                    restoreData = obj_db_ApiHistory[0].restoreData
                                    if obj_db_ApiHistory[0].operationType in ["Add", "Edit"]:
                                        obj_db_ApiBaseData = db_ApiBaseData.objects.filter(id=apiId)
                                        if obj_db_ApiBaseData.exists():
                                            # region ????????????
                                            cls_Logging.record_operation_info(
                                                'API', 'Manual', 3, 'Update',
                                                cls_FindTable.get_pro_name(obj_db_ApiHistory[0].pid_id),
                                                cls_FindTable.get_page_name(obj_db_ApiHistory[0].page_id),
                                                cls_FindTable.get_fun_name(obj_db_ApiHistory[0].fun_id),
                                                userId,
                                                f'???????????????????????? '
                                                f'ID:{obj_db_ApiHistory[0].api_id}:'
                                                f"{obj_db_ApiHistory[0].apiName}",
                                            )
                                            # endregion
                                            restoreData = ast.literal_eval(restoreData)
                                            # region ?????????????????????????????????????????????????????????????????????
                                            db_ApiAssociatedUser.objects.filter(
                                                apiId_id=apiId,
                                                onlyCode=obj_db_ApiBaseData[0].onlyCode).update(
                                                is_del=1, updateTime=cls_Common.get_date_time())
                                            db_ApiHeaders.objects.filter(
                                                apiId_id=apiId,
                                                onlyCode=obj_db_ApiBaseData[0].onlyCode).update(
                                                is_del=1, updateTime=cls_Common.get_date_time())
                                            db_ApiParams.objects.filter(
                                                apiId_id=apiId,
                                                onlyCode=obj_db_ApiBaseData[0].onlyCode).update(
                                                is_del=1, updateTime=cls_Common.get_date_time())
                                            db_ApiBody.objects.filter(
                                                apiId_id=apiId,
                                                onlyCode=obj_db_ApiBaseData[0].onlyCode).update(
                                                is_del=1, updateTime=cls_Common.get_date_time())
                                            db_ApiExtract.objects.filter(
                                                apiId_id=apiId,
                                                onlyCode=obj_db_ApiBaseData[0].onlyCode).update(
                                                is_del=1, updateTime=cls_Common.get_date_time())
                                            db_ApiValidate.objects.filter(
                                                apiId_id=apiId,
                                                onlyCode=obj_db_ApiBaseData[0].onlyCode).update(
                                                is_del=1, updateTime=cls_Common.get_date_time())
                                            db_ApiOperation.objects.filter(
                                                apiId_id=apiId,
                                                onlyCode=obj_db_ApiBaseData[0].onlyCode).update(
                                                is_del=1, updateTime=cls_Common.get_date_time())
                                            # endregion
                                            # region ????????????
                                            if restoreData['ApiInfo']['request']['params']:
                                                requestParamsType = 'Params'
                                            else:
                                                requestParamsType = 'Body'
                                            requestSaveType = restoreData['ApiInfo']['request']['body'][
                                                'requestSaveType']
                                            obj_db_ApiBaseData.update(
                                                pid_id=restoreData['BasicInfo']['proId'],
                                                page_id=restoreData['BasicInfo']['pageId'],
                                                fun_id=restoreData['BasicInfo']['funId'],
                                                apiName=restoreData['BasicInfo']['apiName'],
                                                environment_id=restoreData['BasicInfo']['environmentId'],
                                                apiState=restoreData['BasicInfo']['apiState'],
                                                requestType=restoreData['ApiInfo']['requestType'],
                                                requestUrl=restoreData['ApiInfo']['requestUrl'],
                                                requestParamsType='Body' if requestSaveType == 'none' else requestParamsType,
                                                bodyRequestSaveType=requestSaveType,
                                                updateTime=restoreData['BasicInfo']['updateTime'],
                                                createTime=restoreData['BasicInfo']['createTime'],
                                                uid_id=restoreData['BasicInfo']['uid_id'],
                                                cuid=restoreData['BasicInfo']['cuid'],
                                                is_del=0,
                                                onlyCode=restoreData['onlyCode'],
                                            )
                                            # ????????????to
                                            db_ApiAssociatedUser.objects.filter(
                                                apiId_id=apiId, onlyCode=onlyCode, is_del=1).update(is_del=0)
                                            # endregion
                                            # region Headers
                                            db_ApiHeaders.objects.filter(
                                                is_del=1, onlyCode=onlyCode, apiId_id=apiId).update(is_del=0)
                                            # endregion
                                            # region Params
                                            db_ApiParams.objects.filter(
                                                is_del=1, onlyCode=onlyCode, apiId_id=apiId).update(is_del=0)
                                            # endregion
                                            # region Body ??????File????????????????????????
                                            db_ApiBody.objects.filter(
                                                is_del=1, onlyCode=onlyCode, apiId_id=apiId).update(is_del=0)
                                            # endregion
                                            # region Extract
                                            db_ApiExtract.objects.filter(
                                                is_del=1, onlyCode=onlyCode, apiId_id=apiId).update(is_del=0)
                                            # endregion
                                            # region Validate
                                            db_ApiValidate.objects.filter(
                                                is_del=1, onlyCode=onlyCode, apiId_id=apiId).update(is_del=0)
                                            # endregion
                                            # region ?????????
                                            db_ApiOperation.objects.filter(
                                                is_del=1, onlyCode=onlyCode, apiId_id=apiId).update(is_del=0)
                                            # endregion
                                        else:
                                            raise ValueError('?????????????????????????????????????????????!')
                                    else:
                                        raise ValueError('?????????????????????????????????!')
                                else:
                                    raise ValueError(f"????????????????????????????????????????????????,????????????!")
                            else:
                                raise ValueError(f"????????????????????????????????????????????????,????????????!")
                        else:
                            raise ValueError(f"????????????????????????????????????????????????,????????????!")
                except BaseException as e:  # ????????????????????????????????????
                    response['errorMsg'] = f"??????????????????:{e}"
                else:
                    response['statusCode'] = 2002
            else:
                response['errorMsg'] = "??????????????????????????????,??????????????????????????????????????????!"
        else:
            response['errorMsg'] = "????????????????????????????????????,????????????????????????!"
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # ???????????????????????????
def select_life_cycle(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        apiId = objData.apiId
    except BaseException as e:
        errorMsg = f"????????????:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_IntMaintenance', 'select_life_cycle', errorMsg)
    else:
        obj_db_ApiHistory = db_ApiHistory.objects.filter(api_id=apiId).order_by('-createTime')
        for i in obj_db_ApiHistory:
            content = ""
            operationType = i.operationType
            if operationType == "Add":
                title = f'?????????????????? {i.uid.userName}({i.uid.nickName})'
            elif operationType == "Edit":
                title = f'?????????????????? {i.uid.userName}({i.uid.nickName})'
                content = i.textInfo
            else:
                title = f'?????????????????? {i.uid.userName}({i.uid.nickName})'
            dataList.append({
                'title': title,
                'content': content,
                'timestamp': str(i.createTime.strftime('%Y-%m-%d %H:%M:%S')),
            })

        response['TableData'] = dataList
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # ??????JSON?????? ????????????
def analysis_json_data(request):
    response = {}
    dataTable = []
    try:
        responseData = json.loads(request.body)
        objData = cls_object_maker(responseData)
        proId = objData.proId
        pageId = objData.pageId
        funId = objData.funId
        file = objData.file
    except BaseException as e:
        errorMsg = f"????????????:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_IntMaintenance', 'delete_data', errorMsg)
    else:
        fileName = file[0].name
        JsonData = cls_Swagger.analysisJsonData(f'{settings.TEMP_PATH}{fileName}')
        if JsonData['state']:
            for item in JsonData['dataTable']:
                apiName = item['apiName']
                requestType = item['requestType']
                jsonUrl = {
                    'url1': item['requestUrl'],
                    'url2': '',
                    'url3': '',
                }
                obj_db_ApiBaseData = db_ApiBaseData.objects.filter(
                    pid_id=proId, page_id=pageId, fun_id=funId,
                    apiName=apiName, requestType=requestType, requestUrl=jsonUrl, is_del=0)
                if obj_db_ApiBaseData.exists():
                    isImport = True
                else:
                    isImport = False
                item['isImport'] = isImport
                dataTable.append(item)
            response['statusCode'] = 2000
            response['dataTable'] = JsonData['dataTable']
        else:
            response['errorMsg'] = JsonData['errorMsg']
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # ??????JSON?????? ????????????
def import_api_data(request):
    response = {}
    try:
        responseData = json.loads(request.body)
        objData = cls_object_maker(responseData)

        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        roleId = cls_FindTable.get_roleId(userId)
        proId = objData.proId
        pageId = objData.pageId
        funId = objData.funId
        environmentId = objData.environmentId
        tableData = objData.tableData
        historyCode = cls_Common.generate_only_code()
    except BaseException as e:
        errorMsg = f"????????????:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_IntMaintenance', 'import_api_data', errorMsg)
        cls_Logging.print_log('error', 'import_api_data', errorMsg)
    else:
        # ???????????????????????????api????????????
        apiTable = cls_Swagger.conversion_swagger_table_to_api_table(
            proId, pageId, funId, environmentId, roleId, userId, tableData)
        if apiTable['state']:
            try:
                with transaction.atomic():  # ???????????????????????????python???????????????????????????
                    for item_api in apiTable['tableData']:
                        apiName = item_api['BasicInfo']['apiName']
                        requestType = item_api['ApiInfo']['requestType']
                        requestUrl = item_api['ApiInfo']['requestUrl']
                        obj_db_ApiBaseData = db_ApiBaseData.objects.filter(
                            pid_id=proId, page_id=pageId, fun_id=funId,
                            apiName=apiName, requestType=requestType, requestUrl=requestUrl, is_del=0)
                        if obj_db_ApiBaseData.exists():
                            pass
                        else:
                            # region ??????????????????
                            operationInfoId = cls_Logging.record_operation_info(
                                'API', 'Manual', 3, 'Add',
                                cls_FindTable.get_pro_name(proId),
                                cls_FindTable.get_page_name(pageId),
                                cls_FindTable.get_fun_name(funId),
                                userId,
                                '??????????????????', CUFront=item_api
                            )
                            # endregion
                            # region ??????????????????
                            save_db_ApiBaseData = db_ApiBaseData.objects.create(
                                pid_id=proId, page_id=pageId, fun_id=funId,
                                apiName=apiName,
                                environment_id=item_api['BasicInfo']['environmentId'],
                                apiState=item_api['BasicInfo']['apiState'],
                                requestType=requestType,
                                requestUrl=requestUrl,
                                requestUrlRadio=item_api['ApiInfo']['requestUrlRadio'],
                                requestParamsType=item_api['ApiInfo']['requestParamsType'],
                                bodyRequestSaveType=item_api['ApiInfo']['request']['body']['requestSaveType'],
                                uid_id=userId, cuid=userId,
                                assignedToUser=item_api['BasicInfo']['assignedUserId'],
                                is_del=0,
                            )
                            # endregion
                            # region ??????????????????
                            db_ApiHistory.objects.create(
                                pid_id=proId,
                                page_id=pageId,
                                fun_id=funId,
                                api_id=save_db_ApiBaseData.id,
                                apiName=apiName,
                                operationType='Add',
                                restoreData=None,
                                textInfo=None,
                                onlyCode=historyCode,
                            )
                            # endregion
                            # region Headers
                            product_list_to_insert = list()
                            for item_headers in item_api['ApiInfo']['request']['headers']:
                                product_list_to_insert.append(db_ApiHeaders(
                                    apiId_id=save_db_ApiBaseData.id,
                                    index=item_headers['index'],
                                    key=item_headers['key'],
                                    value=item_headers['value'],
                                    remarks=item_headers['remarks'],
                                    state=1 if item_headers['state'] else 0,
                                    is_del=0,
                                    historyCode=historyCode)
                                )
                            db_ApiHeaders.objects.bulk_create(product_list_to_insert)
                            # endregion
                            # region Params
                            product_list_to_insert = list()
                            for item_params in item_api['ApiInfo']['request']['params']:
                                product_list_to_insert.append(db_ApiParams(
                                    apiId_id=save_db_ApiBaseData.id,
                                    index=item_params['index'],
                                    key=item_params['key'],
                                    value=item_params['value'],
                                    remarks=item_params['remarks'],
                                    state=1 if item_params['state'] else 0,
                                    is_del=0,
                                    historyCode=historyCode)
                                )
                            db_ApiParams.objects.bulk_create(product_list_to_insert)
                            # endregion
                            # region Body
                            requestSaveType = item_api['ApiInfo']['request']['body']['requestSaveType']
                            if requestSaveType == 'form-data':
                                product_list_to_insert = list()
                                for item_body in item_api['ApiInfo']['request']['body']['formData']:
                                    product_list_to_insert.append(db_ApiBody(
                                        apiId_id=save_db_ApiBaseData.id,
                                        index=item_body['index'],
                                        key=item_body['key'],
                                        value=item_body['value'],
                                        remarks=item_body['remarks'],
                                        state=1 if item_body['state'] else 0,
                                        is_del=0,
                                        historyCode=historyCode)
                                    )
                                db_ApiBody.objects.bulk_create(product_list_to_insert)
                            elif requestSaveType in ['raw', 'json']:
                                if requestSaveType == 'raw':
                                    value = item_api['ApiInfo']['request']['body']['raw']['value']
                                elif requestSaveType == 'json':
                                    value = item_api['ApiInfo']['request']['body']['json']['value']
                                else:
                                    value = None
                                db_ApiBody.objects.create(
                                    apiId_id=save_db_ApiBaseData.id,
                                    index=0,
                                    key=None,
                                    value=value,
                                    state=1,
                                    is_del=0,
                                    historyCode=historyCode
                                )
                            # file ????????????
                            # endregion
            except BaseException as e:  # ????????????????????????????????????
                errorMsg = f'????????????:{e}'
                response['errorMsg'] = errorMsg
                cls_Logging.record_error_info('API', 'Api_IntMaintenance', 'import_api_data', errorMsg)
                cls_Logging.print_log('error', 'import_api_data', errorMsg)
            else:
                response['statusCode'] = 2001
        else:
            response['errorMsg'] = apiTable['errorMsg']
    return JsonResponse(response)
