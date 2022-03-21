from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction

import json
import ast

# Create your db here.
from ProjectManagement.models import ProManagement as db_ProManagement
from PageManagement.models import PageManagement as db_PageManagement
from FunManagement.models import FunManagement as db_FunManagement
from Ui_ElementMaintenance.models import ElementBaseData as db_ElementBaseData
from Ui_ElementMaintenance.models import ElementLocation as db_ElementLocation
from Ui_ElementMaintenance.models import ElementHistory as db_ElementHistory
from Ui_ElementEvent.models import ElementEventComponent as db_ElementEventComponent
from Ui_ElementEvent.models import ElementEvent as db_ElementEvent
from Ui_CaseMaintenance.models import UiTestSet as db_TestSet
from Ui_ElementMaintenance.models import ElementDynamic as db_ElementDynamic

# Create reference here.
from ClassData.Logger import Logging
from ClassData.GlobalDecorator import GlobalDer
from ClassData.FindCommonTable import FindTable
from ClassData.Common import Common
from ClassData.ImageProcessing import ImageProcessing
from ClassData.ObjectMaker import object_maker as cls_object_maker
from ClassData.Redis import RedisHandle
from ClassData.Element import Element

# Create info here.
cls_Logging = Logging()
cls_GlobalDer = GlobalDer()
cls_FindTable = FindTable()
cls_Common = Common()
cls_ImageProcessing = ImageProcessing()
cls_RedisHandle = RedisHandle()
cls_Element = Element()

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
        pageId = objData.pageId
        funId = objData.funId
        elementName = objData.elementName

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('UI', 'Ui_ElementMaintenance', 'select_data', errorMsg)
    else:
        obj_db_ElementBaseData = db_ElementBaseData.objects.filter(is_del=0, pid_id=proId).order_by('-updateTime')
        if pageId:
            obj_db_ElementBaseData = obj_db_ElementBaseData.filter(page_id=pageId)
        if funId:
            obj_db_ElementBaseData = obj_db_ElementBaseData.filter(fun_id=funId)
        if elementName:
            obj_db_ElementBaseData = obj_db_ElementBaseData.filter(elementName__icontains=elementName)
        select_db_ElementBaseData = obj_db_ElementBaseData[minSize: maxSize]
        for i in select_db_ElementBaseData:
            tableItem = []
            obj_db_ElementLocation = db_ElementLocation.objects.filter(is_del=0, element_id=i.id).order_by('index')
            for item_location in obj_db_ElementLocation:
                tableItem.append({
                    'state': True if item_location.state == 1 else False,
                    'targetingType': item_location.targetingType,
                    'targetingPath': item_location.targetingPath,
                    'remarks': item_location.remarks,
                })
            elementType = ast.literal_eval(i.elementType) if i.elementType else []
            if elementType:
                obj_db_ElementEvent = db_ElementEvent.objects.filter(is_del=0, eventLogo=elementType[0])
                if obj_db_ElementEvent.exists():
                    obj_db_ElementEventComponent = db_ElementEventComponent.objects.filter(
                        is_del=0, event_id=obj_db_ElementEvent[0].id, value=elementType[1])
                    if obj_db_ElementEventComponent.exists():
                        elementTypeTxt = obj_db_ElementEventComponent[0].label
                    else:
                        elementTypeTxt = None
                else:
                    elementTypeTxt = None
            else:
                elementTypeTxt = None
            dataList.append({
                "id": i.id,
                "elementName": i.elementName,
                "pageName": i.page.pageName,
                "funName": i.fun.funName,
                "elementType": elementTypeTxt,
                "locationTotal": obj_db_ElementLocation.count(),
                "elementState": True if i.elementState == 1 else False,
                "updateTime": str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                "userName": f"{i.uid.userName}({i.uid.nickName})",
                "createUserName": cls_FindTable.get_userName(i.cuid),
                "tableItem": tableItem,
            })

        response['TableData'] = dataList
        response['Total'] = obj_db_ElementBaseData.count()
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def save_data(request):
    response = {}
    try:
        responseData = json.loads(request.body)
        objData = cls_object_maker(responseData)
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        proId = objData.baseData.proId
        pageId = objData.baseData.pageId
        funId = objData.baseData.funId
        elementName = objData.baseData.elementName
        elementType = objData.baseData.elementType
        elementState = 1 if objData.baseData.elementState else 0

        elementLocation = objData.elementLocation
        onlyCode = cls_Common.generate_only_code()
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('UI', 'Ui_ElementMaintenance', 'save_data', errorMsg)
    else:
        obj_db_ElementBaseData = db_ElementBaseData.objects.filter(
            is_del=0, pid_id=proId, fun_id=funId, page_id=pageId, elementName=elementName, elementType=elementType)
        if obj_db_ElementBaseData.exists():
            response['errorMsg'] = "当前所属功能下已有相同元素名称或元素类型,请更改!"
        else:
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    # region 添加操作信息
                    cls_Logging.record_operation_info(
                        'UI', 'Manual', 3, 'Add',
                        cls_FindTable.get_pro_name(proId),
                        cls_FindTable.get_page_name(pageId),
                        cls_FindTable.get_fun_name(funId),
                        userId,
                        '【新增元素】', CUFront=responseData
                    )
                    # endregion
                    # region 保存基本信息
                    save_db_ElementBaseData = db_ElementBaseData.objects.create(
                        pid_id=proId, page_id=pageId, fun_id=funId,
                        elementName=elementName, elementType=elementType, elementState=elementState,
                        uid_id=userId, cuid=userId, is_del=0, onlyCode=onlyCode,
                    )
                    # endregion
                    # region 定位表
                    product_list_to_insert = list()
                    for index, item_location in enumerate(elementLocation, 0):
                        product_list_to_insert.append(db_ElementLocation(
                            element_id=save_db_ElementBaseData.id,
                            index=index,
                            targetingType=item_location.targetingType,
                            targetingPath=item_location.targetingPath,
                            remarks=item_location.remarks,
                            state=1 if item_location.state else 0,
                            is_del=0,
                            onlyCode=onlyCode)
                        )
                    db_ElementLocation.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region 添加历史恢复
                    restoreData = json.loads(request.body)
                    restoreData['baseData']['updateTime'] = save_db_ElementBaseData.updateTime.strftime(
                        '%Y-%m-%d %H:%M:%S')
                    restoreData['baseData']['createTime'] = save_db_ElementBaseData.createTime.strftime(
                        '%Y-%m-%d %H:%M:%S')
                    restoreData['baseData']['uid_id'] = save_db_ElementBaseData.uid_id
                    restoreData['baseData']['cuid'] = save_db_ElementBaseData.cuid
                    restoreData['baseData']['onlyCode'] = onlyCode
                    db_ElementHistory.objects.create(
                        pid_id=proId,
                        page_id=pageId,
                        fun_id=funId,
                        element_id=save_db_ElementBaseData.id,
                        elementName=elementName,
                        onlyCode=onlyCode,
                        operationType='Add',
                        restoreData=restoreData,
                        uid_id=userId,
                    )
                    # endregion
            except BaseException as e:  # 自动回滚，不需要任何操作
                response['errorMsg'] = f'保存失败:{e}'
            else:
                response['elementId'] = save_db_ElementBaseData.id
                response['statusCode'] = 2001
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def load_data(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)

        elementId = objData.elementId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('UI', 'Ui_ElementMaintenance', 'load_data', errorMsg)
    else:
        obj_db_ElementBaseData = db_ElementBaseData.objects.filter(is_del=0, id=elementId)
        if obj_db_ElementBaseData.exists():
            baseData = {
                'pageId': obj_db_ElementBaseData[0].page_id,
                'funId': obj_db_ElementBaseData[0].fun_id,
                'elementName': obj_db_ElementBaseData[0].elementName,
                'elementType': ast.literal_eval(obj_db_ElementBaseData[0].elementType),
                'elementState': True if obj_db_ElementBaseData[0].elementState == 1 else False,
            }
            obj_db_ElementLocation = db_ElementLocation.objects.filter(is_del=0, element_id=elementId).order_by('index')
            locationTable = [{
                'state': True if i.state == 1 else False,
                'targetingType': i.targetingType,
                'targetingPath': i.targetingPath,
                'remarks': i.remarks
            }
                for i in obj_db_ElementLocation]

            response['statusCode'] = 2000
            response['baseData'] = baseData
            response['locationTable'] = locationTable
        else:
            response['errorMsg'] = "当前选择的数据不存在,请刷新列表后重新尝试!"
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def edit_data(request):
    response = {}
    is_Edit = False
    try:
        responseData = json.loads(request.body)
        objData = cls_object_maker(responseData)

        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        elementId = int(objData.baseData.elementId)
        proId = objData.baseData.proId
        pageId = objData.baseData.pageId
        funId = objData.baseData.funId
        elementName = objData.baseData.elementName
        elementType = objData.baseData.elementType
        elementState = 1 if objData.baseData.elementState else 0
        elementLocation = objData.elementLocation
        onlyCode = cls_Common.generate_only_code()
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('UI', 'Ui_ElementMaintenance', 'edit_data', errorMsg)
    else:
        obj_db_ElementBaseData = db_ElementBaseData.objects.filter(id=elementId, is_del=0)
        if obj_db_ElementBaseData.exists():
            select_db_ElementBaseData = db_ElementBaseData.objects.filter(
                pid_id=proId, page_id=pageId, fun_id=funId, elementName=elementName, elementType=elementType, is_del=0)
            if select_db_ElementBaseData.exists():
                if elementId == select_db_ElementBaseData[0].id:  # 自己修改自己
                    is_Edit = True
                else:
                    response['errorMsg'] = '当前所属功能下已有重复元素名称或元素类型,请更改!'
            else:
                is_Edit = True
            if is_Edit:
                try:
                    with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                        # region 添加操作信息
                        # region oldData
                        obj_db_ElementLocation = db_ElementLocation.objects.filter(
                            is_del=0,element_id=elementId).order_by('index')
                        oldElementLocation = [{
                            'state':i.state,
                            'targetingType':i.targetingType,
                            'targetingPath':i.targetingPath,
                            'remarks':i.remarks,
                        } for i in obj_db_ElementLocation]
                        oldData = {
                            'baseData':{
                                'proId':obj_db_ElementBaseData[0].pid_id,
                                'pageId':obj_db_ElementBaseData[0].page_id,
                                'funId':obj_db_ElementBaseData[0].fun_id,
                                'elementName':obj_db_ElementBaseData[0].elementName,
                                'elementType':ast.literal_eval(obj_db_ElementBaseData[0].elementType),
                                'elementState': True if obj_db_ElementBaseData[0].elementState==1 else False,
                            },
                            'elementLocation':oldElementLocation
                        }
                        # endregion
                        newData = json.loads(request.body)
                        cls_Logging.record_operation_info(
                            "UI", 'Manual', 3, 'Edit',
                            cls_FindTable.get_pro_name(proId),
                            cls_FindTable.get_page_name(pageId),
                            cls_FindTable.get_fun_name(funId),
                            userId,
                            '【修改元素】',
                            oldData, newData
                        )
                        # endregion
                        # region 对比新数据和老数据的差异
                        textInfo = cls_Element.select_edit_element_dfif(oldData,newData)

                        # endreigon
                        # region 删除原数据
                        db_ElementLocation.objects.filter(
                            is_del=0, element_id=elementId, onlyCode=obj_db_ElementBaseData[0].onlyCode).update(
                            updateTime=cls_Common.get_date_time(), is_del=1
                        )
                        # endregion
                        # region 基本信息
                        obj_db_ElementBaseData.update(
                            pid_id=proId,
                            page_id=pageId,
                            fun_id=funId,
                            elementName=elementName,
                            elementType=elementType,
                            elementState=elementState,
                            updateTime=cls_Common.get_date_time(),
                            onlyCode=onlyCode,
                            uid_id=userId)
                        # endregion
                        # region 定位表
                        product_list_to_insert = list()
                        for index, item_location in enumerate(elementLocation, 0):
                            product_list_to_insert.append(db_ElementLocation(
                                element_id=elementId,
                                index=index,
                                targetingType=item_location.targetingType,
                                targetingPath=item_location.targetingPath,
                                remarks=item_location.remarks,
                                state=1 if item_location.state else 0,
                                is_del=0,
                                onlyCode=onlyCode)
                            )
                        db_ElementLocation.objects.bulk_create(product_list_to_insert)
                        # endregion
                        # region 添加接口更变信息,用于用例中提醒使用
                        obj_db_TestSet = db_TestSet.objects.filter(is_del=0, elementId=elementId)
                        product_list_to_insert = list()
                        for item_testSet in obj_db_TestSet:
                            obj_db_ElementDynamic = db_ElementDynamic.objects.filter(
                                is_del=0, element_id=elementId, case_id=item_testSet.case_id, is_read=0)
                            if obj_db_ElementDynamic.exists():
                                obj_db_ElementDynamic.update(updateTime=cls_Common.get_date_time(), uid_id=userId)
                            else:
                                product_list_to_insert.append(db_ElementDynamic(
                                    element_id=elementId,
                                    case_id=item_testSet.case_id,
                                    uid_id=userId,
                                    cuid=userId,
                                    is_read=0,
                                    is_del=0,
                                ))
                        db_ElementDynamic.objects.bulk_create(product_list_to_insert)
                        # endregion
                        # region 添加历史恢复
                        restoreData = json.loads(request.body)
                        restoreData['baseData']['updateTime'] = obj_db_ElementBaseData[0].updateTime.strftime(
                            '%Y-%m-%d %H:%M:%S')
                        restoreData['baseData']['createTime'] = obj_db_ElementBaseData[0].createTime.strftime(
                            '%Y-%m-%d %H:%M:%S')
                        restoreData['baseData']['uid_id'] = obj_db_ElementBaseData[0].uid_id
                        restoreData['baseData']['cuid'] = obj_db_ElementBaseData[0].cuid
                        restoreData['baseData']['onlyCode'] = onlyCode
                        db_ElementHistory.objects.create(
                            pid_id=proId,
                            page_id=pageId,
                            fun_id=funId,
                            element_id=elementId,
                            elementName=elementName,
                            onlyCode=onlyCode,
                            operationType='Edit',
                            restoreData=restoreData,
                            textInfo=textInfo,
                            uid_id=userId,
                        )
                        # endregion
                except BaseException as e:  # 自动回滚，不需要任何操作
                    response['errorMsg'] = f'数据修改失败:{e}'
                else:
                    response['statusCode'] = 2002
        else:
            response['errorMsg'] = '未找当前所属页面,请刷新后重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def delete_data(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        elementId = request.POST['elementId']
        onlyCode = cls_Common.generate_only_code()
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('UI', 'Ui_ElementMaintenance', 'delete_data', errorMsg)
    else:
        obj_db_ElementBaseData = db_ElementBaseData.objects.filter(id=elementId)
        if obj_db_ElementBaseData.exists():
            obj_db_TestSet = db_TestSet.objects.filter(is_del=0,elementId=elementId)
            if obj_db_TestSet.exists():
                caseTable = [i.case.caseName for i in obj_db_TestSet]
                caseTable = set(caseTable)
                response['errorMsg'] = '当前元素已绑定用例,请解除绑定后在进行删除操作!' \
                                       f'用例列表:{caseTable}'
            else:
                try:
                    with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                        # region 添加历史恢复
                        db_ElementHistory.objects.create(
                            pid_id=obj_db_ElementBaseData[0].pid_id,
                            page_id=obj_db_ElementBaseData[0].page_id,
                            fun_id=obj_db_ElementBaseData[0].fun_id,
                            element_id=elementId,
                            elementName=obj_db_ElementBaseData[0].elementName,
                            operationType='Delete',
                            onlyCode=onlyCode,
                            uid_id=userId,
                        )
                        # endregion
                        # region 删除关联信息
                        db_ElementLocation.objects.filter(
                            is_del=0, element_id=elementId, onlyCode=obj_db_ElementBaseData[0].onlyCode).update(
                            is_del=1, updateTime=cls_Common.get_date_time())
                        obj_db_ElementBaseData.update(
                            is_del=1, updateTime=cls_Common.get_date_time(), uid_id=userId
                        )
                        # endregion
                        # region 添加操作信息
                        cls_Logging.record_operation_info(
                            'UI', 'Manual', 3, 'Delete',
                            cls_FindTable.get_pro_name(obj_db_ElementBaseData[0].pid_id),
                            cls_FindTable.get_page_name(obj_db_ElementBaseData[0].page_id),
                            cls_FindTable.get_fun_name(obj_db_ElementBaseData[0].fun_id),
                            userId,
                            f'【删除元素】 ID:{elementId}:{obj_db_ElementBaseData[0].elementName}',
                            CUFront=json.dumps(request.POST)
                        )
                        # endregion
                except BaseException as e:  # 自动回滚，不需要任何操作
                    response['errorMsg'] = f'数据删除失败:{e}'
                else:
                    response['statusCode'] = 2003
        else:
            response['errorMsg'] = '未找到当前数据,请刷新后重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 效验数据的完成性
def charm_element_data(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(request.body)
        objData = cls_object_maker(responseData)
        charmType = objData.CharmType  # true 新增，false 修改
        baseData = objData.baseData
        locationData = objData.locationData
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('UI', 'Ui_ElementMaintenance', 'charm_element_data', errorMsg)
    else:
        # region 验证 基本信息
        obj_db_ElementBaseData = db_ElementBaseData.objects.filter(
            is_del=0, pid_id=baseData.proId, fun_id=baseData.funId, page_id=baseData.pageId,
            elementName=baseData.elementName, elementType=baseData.elementType)
        if obj_db_ElementBaseData.exists():
            if charmType:
                dataList.append({
                    'stepsName': '基本信息',
                    'errorMsg': "当前所属功能下已有相同元素名称或元素类型,请更改!",
                    'updateTime': cls_Common.get_date_time()})
            else:
                if obj_db_ElementBaseData.exists():
                    if baseData.elementId == obj_db_ElementBaseData[0].id:
                        pass
                    else:
                        dataList.append({
                            'stepsName': '基本信息',
                            'errorMsg': "当前所属功能下已有相同元素名称或元素类型,请更改!",
                            'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证 定位信息
        if locationData:
            stateList = []
            for index, item_location in enumerate(locationData, 1):
                stateList.append(item_location.state)
                if item_location.state:
                    if not item_location.targetingType:
                        dataList.append({
                            'stepsName': '定位信息',
                            'errorMsg': f'第{index}行:定位类型不可为空!',
                            'updateTime': cls_Common.get_date_time()})
                    if not item_location.targetingPath:
                        dataList.append({
                            'stepsName': '定位信息',
                            'errorMsg': f'第{index}行:定位地址不可为空!',
                            'updateTime': cls_Common.get_date_time()})
            if True not in stateList:
                dataList.append({
                    'stepsName': '定位信息',
                    'errorMsg': f'请至少保存或启用1条定位信息!',
                    'updateTime': cls_Common.get_date_time()})

        else:
            dataList.append({
                'stepsName': '定位信息',
                'errorMsg': f'请至少保存或启用1条定位信息!',
                'updateTime': cls_Common.get_date_time()})
        # endregion
        response['statusCode'] = 2000
        response['TableData'] = dataList
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

        elementId = objData.elementId
        pageId = objData.pageId
        funId = objData.funId
        elementName = objData.elementName

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('UI', 'Ui_ElementMaintenance', 'select_history', errorMsg)
    else:
        if elementId:
            obj_db_ElementHistory = db_ElementHistory.objects.filter(element_id=elementId).order_by('-createTime')
        else:
            obj_db_ElementHistory = db_ElementHistory.objects.filter().order_by('-createTime')
        if pageId:
            obj_db_ElementHistory = obj_db_ElementHistory.filter(page_id=pageId).order_by('-createTime')
        if funId:
            obj_db_ElementHistory = obj_db_ElementHistory.filter(fun_id=funId).order_by('-createTime')
        if elementName:
            obj_db_ElementHistory = obj_db_ElementHistory.filter(
                elementName__icontains=elementName).order_by('-createTime')
        select_db_ElementHistory = obj_db_ElementHistory[minSize: maxSize]
        for i in select_db_ElementHistory:
            if i.restoreData:
                restoreData = json.dumps(ast.literal_eval(i.restoreData),
                                         sort_keys=True, indent=4, separators=(",", ": "), ensure_ascii=False)
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
                'elementName': i.elementName,
                'operationType': i.operationType,
                'tableItem': tableItem,
                'createTime': str(i.createTime.strftime('%Y-%m-%d %H:%M:%S')),
                "userName": f"{i.uid.userName}({i.uid.nickName})",
            })
        response['TableData'] = dataList
        response['Total'] = obj_db_ElementHistory.count()
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
        cls_Logging.record_error_info('UI', 'Ui_ElementMaintenance', 'restor_data', errorMsg)
    else:
        obj_db_ElementHistory = db_ElementHistory.objects.filter(id=historyId)
        if obj_db_ElementHistory.exists():
            # 恢复时是管理员或是 当前项目的创建人时才可恢复
            if is_admin or obj_db_ElementHistory[0].element.cuid == userId:
                try:
                    with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                        obj_db_ProManagement = db_ProManagement.objects.filter(
                            is_del=0, id=obj_db_ElementHistory[0].pid_id)
                        if obj_db_ProManagement.exists():
                            obj_db_PageManagement = db_PageManagement.objects.filter(
                                is_del=0, id=obj_db_ElementHistory[0].page_id)
                            if obj_db_PageManagement.exists():
                                obj_db_FunManagement = db_FunManagement.objects.filter(
                                    is_del=0, id=obj_db_ElementHistory[0].fun_id)
                                if obj_db_FunManagement.exists():
                                    elementId = obj_db_ElementHistory[0].element_id
                                    restoreData = obj_db_ElementHistory[0].restoreData
                                    if obj_db_ElementHistory[0].operationType in ["Add", "Edit"]:
                                        obj_db_ElementBaseData = db_ElementBaseData.objects.filter(id=elementId)
                                        if obj_db_ElementBaseData.exists():
                                            restoreData = ast.literal_eval(restoreData)
                                            # region 操作记录
                                            cls_Logging.record_operation_info(
                                                'UI', 'Manual', 3, 'Update',
                                                cls_FindTable.get_pro_name(obj_db_ElementHistory[0].pid_id),
                                                cls_FindTable.get_page_name(obj_db_ElementHistory[0].page_id),
                                                cls_FindTable.get_fun_name(obj_db_ElementHistory[0].fun_id),
                                                userId,
                                                f'【恢复元素维护】:'
                                                f'ID:{elementId}:'
                                                f"{obj_db_ElementHistory[0].elementName}",
                                            )
                                            # endregion
                                            # region 需要删除原附属数据，不会恢复时会出现原数据还在
                                            db_ElementLocation.objects.filter(
                                                element_id=elementId,
                                                onlyCode=obj_db_ElementBaseData[0].onlyCode).update(
                                                is_del=1, updateTime=cls_Common.get_date_time())
                                            # endregion
                                            # region 基本数据
                                            obj_db_ElementBaseData.update(
                                                pid_id=restoreData['baseData']['proId'],
                                                page_id=restoreData['baseData']['pageId'],
                                                fun_id=restoreData['baseData']['funId'],
                                                elementName=restoreData['baseData']['elementName'],
                                                elementType=restoreData['baseData']['elementType'],
                                                elementState=restoreData['baseData']['elementState'],
                                                updateTime=restoreData['baseData']['updateTime'],
                                                createTime=restoreData['baseData']['createTime'],
                                                uid_id=restoreData['baseData']['uid_id'],
                                                cuid=restoreData['baseData']['cuid'],
                                                is_del=0,
                                                onlyCode=restoreData['baseData']['onlyCode'],
                                            )
                                            # endregion
                                            # region 定位表
                                            db_ElementLocation.objects.filter(
                                                is_del=1,
                                                onlyCode=obj_db_ElementHistory[0].onlyCode,
                                                element_id=elementId).update(is_del=0)
                                            # endregion
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


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def copy_element(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        elementId = request.POST['elementId']
        onlyCode = cls_Common.generate_only_code()
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('UI', 'Ui_ElementMaintenance', 'copy_element', errorMsg)
    else:
        obj_db_ElementBaseData = db_ElementBaseData.objects.filter(is_del=0, id=elementId)
        if obj_db_ElementBaseData.exists():
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    # region 添加操作信息
                    cls_Logging.record_operation_info(
                        'UI', 'Manual', 3, 'Add',
                        cls_FindTable.get_pro_name(obj_db_ElementBaseData[0].pid_id),
                        cls_FindTable.get_page_name(obj_db_ElementBaseData[0].page_id),
                        cls_FindTable.get_fun_name(obj_db_ElementBaseData[0].fun_id),
                        userId,
                        '【复制元素】', CUFront=f"ID:{elementId},{obj_db_ElementBaseData[0].elementName}"
                    )
                    # endregion
                    # region 基础信息
                    elementName = f"副本-{obj_db_ElementBaseData[0].elementName}"
                    save_db_ElementBaseData = db_ElementBaseData.objects.create(
                        pid_id=obj_db_ElementBaseData[0].pid_id,
                        page_id=obj_db_ElementBaseData[0].page_id,
                        fun_id=obj_db_ElementBaseData[0].fun_id,
                        elementName=elementName,
                        elementType=obj_db_ElementBaseData[0].elementType,
                        elementState=obj_db_ElementBaseData[0].elementState,
                        uid_id=userId,
                        cuid=userId,
                        is_del=0,
                        onlyCode=onlyCode,
                    )
                    # endregion
                    # region 定位
                    obj_db_ElementLocation = db_ElementLocation.objects.filter(is_del=0, element_id=elementId)
                    elementLocation = []
                    product_list_to_insert = list()
                    for item in obj_db_ElementLocation:
                        product_list_to_insert.append(db_ElementLocation(
                            element_id=save_db_ElementBaseData.id,
                            index=item.index,
                            targetingType=item.targetingType,
                            targetingPath=item.targetingPath,
                            remarks=item.remarks,
                            state=item.state,
                            is_del=0,
                            onlyCode=onlyCode,
                        ))
                        elementLocation.append({
                            'state': item.state,
                            'targetingType': item.targetingType,
                            'targetingPath': item.targetingPath,
                            'remarks': item.remarks,
                        })
                    db_ElementLocation.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region 添加历史恢复
                    restoreData = {
                        'baseData': {
                            'proId': obj_db_ElementBaseData[0].pid_id,
                            'pageId': obj_db_ElementBaseData[0].page_id,
                            'funId': obj_db_ElementBaseData[0].fun_id,
                            'elementName': elementName,
                            'elementType': obj_db_ElementBaseData[0].elementType,
                            'elementState': True if obj_db_ElementBaseData[0].elementState == 1 else False,
                            'uid_id': userId,
                            'cuid': userId,
                            'onlyCode': onlyCode,
                            'updateTime': save_db_ElementBaseData.updateTime.strftime('%Y-%m-%d %H:%M:%S'),
                            'createTime': save_db_ElementBaseData.createTime.strftime('%Y-%m-%d %H:%M:%S')
                        },
                        'elementLocation': elementLocation
                    }
                    db_ElementHistory.objects.create(
                        pid_id=obj_db_ElementBaseData[0].pid_id,
                        page_id=obj_db_ElementBaseData[0].page_id,
                        fun_id=obj_db_ElementBaseData[0].fun_id,
                        element_id=save_db_ElementBaseData.id,
                        elementName=elementName,
                        onlyCode=onlyCode,
                        operationType='Add',
                        restoreData=restoreData,
                        uid_id=userId,
                    )
                    # endregion
            except BaseException as e:  # 自动回滚，不需要任何操作
                errorMsg = f"保存失败:{e}"
                response['errorMsg'] = errorMsg
                cls_Logging.print_log('error', 'copy_element', errorMsg)
                cls_Logging.record_error_info('UI', 'Ui_ElementMaintenance', 'copy_element', errorMsg)
            else:
                response['statusCode'] = 2001
        else:
            response['errorMsg'] = "当前选择的数据不存在,请刷新后重新尝试!"
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 查询所属页面列表为条件下的元素
def get_element_name_items(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)

        pageIdList = objData.pageIdList.split(',')
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('UI', 'Ui_ElementMaintenance', 'get_element_name_items', errorMsg)
    else:
        obj_db_PageManagement = db_PageManagement.objects.filter(is_del=0, id__in=pageIdList)
        for item_page in obj_db_PageManagement:
            obj_db_FunManagement = db_FunManagement.objects.filter(is_del=0, page_id=item_page.id)
            for item_fun in obj_db_FunManagement:
                options = []
                obj_db_ElementBaseData = db_ElementBaseData.objects.filter(
                    is_del=0, page_id=item_page.id, fun_id=item_fun.id)
                for item_element in obj_db_ElementBaseData:
                    options.append({'label': item_element.elementName, 'value': item_element.id})
                dataList.append({
                    'label': f"{item_page.pageName}>{item_fun.funName}",
                    'options': options,
                })
        response['statusCode'] = 2000
        response['dataList'] = dataList
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 根据元素ID查询 元素类型
def select_element_type(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)

        elementId = objData.elementId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('UI', 'Ui_ElementMaintenance', 'select_element_type', errorMsg)
    else:
        obj_db_ElementBaseData = db_ElementBaseData.objects.filter(is_del=0,id=elementId)
        if obj_db_ElementBaseData.exists():
            elementType = obj_db_ElementBaseData[0].elementType
            response['statusCode'] = 2000
            response['elementType'] = ast.literal_eval(elementType) if elementType else []
        else:
            response['errorMsg'] = "当前选择的元素不存在,请重新下拉刷新元素列表!"
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 查询元素的生命周期
def select_life_cycle(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        elementId = objData.elementId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Ui_ElementMaintenance', 'select_life_cycle', errorMsg)
    else:
        obj_db_ElementHistory = db_ElementHistory.objects.filter(element_id=elementId).order_by('-createTime')
        for i in obj_db_ElementHistory:
            content = ""
            operationType = i.operationType
            if operationType == "Add":
                title = f'【创建元素】 {i.uid.userName}({i.uid.nickName})'
            elif operationType == "Edit":
                title = f'【修改元素】 {i.uid.userName}({i.uid.nickName})'
                content = i.textInfo
            else:
                title = f'【删除元素】 {i.uid.userName}({i.uid.nickName})'
            dataList.append({
                'title': title,
                'content': content,
                'timestamp': str(i.createTime.strftime('%Y-%m-%d %H:%M:%S')),
            })

        response['TableData'] = dataList
        response['statusCode'] = 2000
    return JsonResponse(response)
