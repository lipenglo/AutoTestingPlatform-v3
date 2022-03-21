from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction

import json
import ast

# Create your db here.
from PageEnvironment.models import PageEnvironment as db_PageEnvironment
from Ui_CaseMaintenance.models import UiCaseBaseData as db_CaseBaseData
from Ui_CaseMaintenance.models import UiAssociatedPage as db_AssociatedPage
from Ui_CaseMaintenance.models import UiTestSet as db_TestSet
from Ui_ElementMaintenance.models import ElementDynamic as db_ElementDynamic
from PageManagement.models import PageManagement as db_PageManagement
from Ui_CaseMaintenance.models import UiOperationSet as db_OperationSet

# Create reference here.
from ClassData.Logger import Logging
from ClassData.GlobalDecorator import GlobalDer
from ClassData.FindCommonTable import FindTable
from ClassData.Common import Common
from ClassData.ImageProcessing import ImageProcessing
from ClassData.ObjectMaker import object_maker as cls_object_maker
from ClassData.Redis import RedisHandle

# Create info here.
cls_Logging = Logging()
cls_GlobalDer = GlobalDer()
cls_FindTable = FindTable()
cls_Common = Common()
cls_ImageProcessing = ImageProcessing()
cls_RedisHandle = RedisHandle()


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
        cls_Logging.record_error_info('UI', 'Ui_CaseMaintenance', 'select_data', errorMsg)
    else:
        obj_db_CaseBaseData = db_CaseBaseData.objects.filter(is_del=0, pid_id=proId).order_by('-updateTime')
        if pageId:
            obj_db_CaseBaseData = obj_db_CaseBaseData.filter(page_id=pageId)
        if funId:
            obj_db_CaseBaseData = obj_db_CaseBaseData.filter(fun_id=funId)
        # if testType:
        #     obj_db_CaseBaseData = obj_db_CaseBaseData.filter(testType=testType)
        if labelId:
            obj_db_CaseBaseData = obj_db_CaseBaseData.filter(label=labelId)
        if caseState:
            obj_db_CaseBaseData = obj_db_CaseBaseData.filter(caseState=caseState)
        if caseName:
            obj_db_CaseBaseData = obj_db_CaseBaseData.filter(caseName__icontains=caseName)
        select_db_CaseBaseData = obj_db_CaseBaseData[minSize: maxSize]
        for i in select_db_CaseBaseData:
            tableItem = []
            obj_db_TestSet = db_TestSet.objects.filter(is_del=0, case_id=i.id)
            # region 步骤排序
            for item_testSet in obj_db_TestSet:
                elementType = ast.literal_eval(item_testSet.elementType)
                elementTypeTxt = cls_FindTable.get_element_label_name(elementType)
                tableItem.append({
                    'index': item_testSet.index,
                    'eventName': item_testSet.eventName,
                    'elementTypeTxt': elementTypeTxt,
                    'inputData': item_testSet.inputData,
                    # 'requestParamsType': requestParamsType,
                    'state': True if item_testSet.state == 1 else False,
                    'updateTime': str(item_testSet.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                })
            # endregion
            # region 元素动态
            obj_db_ElementDynamic = db_ElementDynamic.objects.filter(is_del=0, case_id=i.id, is_read=0)
            if obj_db_ElementDynamic.exists():
                apidynamic = True
            else:
                apidynamic = False
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
                        'elementdynamic': apidynamic,
                        'caseState': i.caseState,
                        'passRate': 0,
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
                    'elementdynamic': apidynamic,
                    'caseState': i.caseState,
                    'passRate': 0,
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
@require_http_methods(["POST"])  # 效验接用例数据的完成性
def charm_case_data(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(request.body)
        objData = cls_object_maker(responseData)
        charmType = objData.CharmType  # true 新增，false 修改
        basicData = objData.BasicData
        testSet = objData.TestSet
        operationSet = objData.OperationSet
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Ui_CaseMaintenance', 'charm_case_data', errorMsg)
    else:
        # region 验证基本信息
        obj_db_CaseBaseData = db_CaseBaseData.objects.filter(
            is_del=0, pid_id=basicData.proId, page_id=basicData.pageId, fun_id=basicData.funId,
            label=basicData.labelId, testType=basicData.testType, caseName=basicData.caseName
        )
        if obj_db_CaseBaseData.exists():
            if charmType:
                dataList.append({
                    'stepsName': '基本信息',
                    'errorMsg': '当前所属功能及同标签同类型下已有相同用例名称,请更改!',
                    'updateTime': cls_Common.get_date_time()})
            else:
                if obj_db_CaseBaseData.exists():
                    if basicData.caseId == obj_db_CaseBaseData[0].id:
                        pass
                    else:
                        dataList.append({
                            'stepsName': '基本信息',
                            'errorMsg': '当前所属功能及同标签同类型下已有相同用例名称,请更改!',
                            'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证页面环境
        obj_db_PageEnvironment = db_PageEnvironment.objects.filter(is_del=0, id=basicData.environmentId)
        if not obj_db_PageEnvironment.exists():
            dataList.append({
                'stepsName': '基本信息',
                'errorMsg': '选择的页面环境不存在,请更改!',
                'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证测试集
        for index_testSet, item_testSet in enumerate(testSet, 1):
            elementId = item_testSet.elementId
            if item_testSet.state:
                if item_testSet.elementType == ['InputEvent', 'Input']:
                    pass
                elif item_testSet.elementType in [['ClickEvent', 'Click'], ['DisplayEvent', 'Label']]:
                    if not elementId:
                        dataList.append({
                            'stepsName': f'测试集',
                            'errorMsg': f'第{index_testSet}行:选择元素不可为空!',
                            'updateTime': cls_Common.get_date_time()})
                if item_testSet.assertType:
                    if not item_testSet.assertValueType:
                        dataList.append({
                            'stepsName': f'测试集',
                            'errorMsg': f'第{index_testSet}行:断言值类型不可为空!',
                            'updateTime': cls_Common.get_date_time()})
                if item_testSet.assertValueType:
                    if not item_testSet.assertType:
                        dataList.append({
                            'stepsName': f'测试集',
                            'errorMsg': f'第{index_testSet}行:断言类型类型不可为空!',
                            'updateTime': cls_Common.get_date_time()})

        # endregion
        # region 验证操作集
        for item_index, item_operationSet in enumerate(operationSet, 1):
            if item_operationSet.state:
                if not item_operationSet.operationType:
                    dataList.append({
                        'stepsName': f'操作集',
                        'errorMsg': f'第{item_index}行:操作类型不可为空!',
                        'updateTime': cls_Common.get_date_time()})
                if not item_operationSet.location:
                    dataList.append({
                        'stepsName': f'操作集',
                        'errorMsg': f'第{item_index}行:操作位置不可为空!',
                        'updateTime': cls_Common.get_date_time()})
                if item_operationSet.operationType == 'TestCase':
                    if not item_operationSet.caseId:
                        dataList.append({
                            'stepsName': f'操作集',
                            'errorMsg': f'第{item_index}行:当前操作类型为用例,选择用例不可为空!',
                            'updateTime': cls_Common.get_date_time()})
                elif item_operationSet.operationType == 'Methods':
                    if not item_operationSet.methodsName:
                        dataList.append({
                            'stepsName': f'操作集',
                            'errorMsg': f'第{item_index}行:当前操作类型为函数方法,调用函数名称不可为空!',
                            'updateTime': cls_Common.get_date_time()})
                elif item_operationSet.operationType == 'DataBase':
                    if not item_operationSet.dataBaseId:
                        dataList.append({
                            'stepsName': f'操作集',
                            'errorMsg': f'第{item_index}行:当前操作类型为数据库,调用数据库地址不可为空!',
                            'updateTime': cls_Common.get_date_time()})
                    if not item_operationSet.sql:
                        dataList.append({
                            'stepsName': f'操作集',
                            'errorMsg': f'第{item_index}行:当前操作类型为数据库,SQL语句不可为空!',
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
        basicData = objData.BasicData
        testSet = objData.TestSet
        operationSet = objData.OperationSet
        onlyCode = cls_Common.generate_only_code()
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('UI', 'Ui_CaseMaintenance', 'data_save', errorMsg)
    else:
        obj_db_CaseBaseData = db_CaseBaseData.objects.filter(
            is_del=0, pid_id=basicData.proId, page_id=basicData.pageId, fun_id=basicData.funId,
            label=basicData.labelId, testType=basicData.testType, caseName=basicData.caseName
        )
        if obj_db_CaseBaseData.exists():
            response['errorMsg'] = f'当前所属功能及同标签同类型下已有相同用例名称,请更改!'
        else:
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    # region 添加操作信息
                    cls_Logging.record_operation_info(
                        'UI', 'Manual', 3, 'Add',
                        cls_FindTable.get_pro_name(basicData.proId),
                        cls_FindTable.get_page_name(basicData.pageId),
                        cls_FindTable.get_fun_name(basicData.funId),
                        userId,
                        '【新增用例】', CUFront=responseData
                    )
                    # endregion
                    # region 保存基本信息
                    save_db_CaseBaseData = db_CaseBaseData.objects.create(
                        pid_id=basicData.proId, page_id=basicData.pageId, fun_id=basicData.funId,
                        environmentId_id=basicData.environmentId, testType=basicData.testType,
                        label=basicData.labelId, priority=basicData.priorityId, caseName=basicData.caseName,
                        caseState=basicData.caseState, cuid=userId, uid_id=userId, is_del=0, onlyCode=onlyCode
                    )
                    # endregion
                    # region 历史恢复
                    # restoreData = responseData
                    # restoreData['BasicInfo']['updateTime'] = save_db_CaseBaseData.updateTime.strftime(
                    #     '%Y-%m-%d %H:%M:%S')
                    # restoreData['BasicInfo']['createTime'] = save_db_CaseBaseData.createTime.strftime(
                    #     '%Y-%m-%d %H:%M:%S')
                    # restoreData['BasicInfo']['uid_id'] = save_db_CaseBaseData.uid_id
                    # restoreData['BasicInfo']['cuid'] = save_db_CaseBaseData.cuid
                    # restoreData['onlyCode'] = onlyCode
                    # db_ApiCaseHistory.objects.create(
                    #     pid_id=basicInfo.proId,
                    #     page_id=basicInfo.pageId,
                    #     fun_id=basicInfo.funId,
                    #     case_id=save_db_CaseBaseData.id,
                    #     caseName=basicInfo.caseName,
                    #     onlyCode=onlyCode,
                    #     operationType='Add',
                    #     restoreData=restoreData,
                    #     uid_id=userId
                    # )
                    # endregion
                    # region 关联页面
                    product_list_to_insert = list()
                    for item_page in basicData.associatedPage:
                        product_list_to_insert.append(db_AssociatedPage(
                            case_id=save_db_CaseBaseData.id,
                            page_id=item_page,
                            is_del=0,
                            onlyCode=onlyCode
                        ))
                    db_AssociatedPage.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region 测试集
                    product_list_to_insert = list()
                    for item_index, item_testSet in enumerate(testSet, 0):
                        product_list_to_insert.append(db_TestSet(
                            case_id=save_db_CaseBaseData.id,
                            index=item_index,
                            state=1 if item_testSet.state else 0,
                            eventName=item_testSet.eventName,
                            elementId=item_testSet.elementId if item_testSet.elementId else None,
                            elementType=item_testSet.elementType,
                            inputData=item_testSet.inputData if item_testSet.inputData else None,
                            assertType=item_testSet.assertType if item_testSet.assertType else None,
                            assertValueType=item_testSet.assertValueType if item_testSet.assertValueType else None,
                            assertValue=item_testSet.assertValue if item_testSet.assertValue else None,
                            is_del=0,
                            onlyCode=onlyCode
                        ))
                    db_TestSet.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region 操作集
                    product_list_to_insert = list()
                    for item_index, item_operationSet in enumerate(operationSet, 1):
                        product_list_to_insert.append(db_OperationSet(
                            case_id=save_db_CaseBaseData.id,
                            index=item_index,
                            state=1 if item_operationSet.state else 0,
                            location=item_operationSet.location,
                            operationType=item_operationSet.operationType,
                            methodsName=item_operationSet.methodsName,
                            caseId=item_operationSet.caseId,
                            dataBaseId=item_operationSet.dataBaseId,
                            sql=item_operationSet.sql,
                            remarks=item_operationSet.remarks,
                            is_del=0,
                            onlyCode=onlyCode
                        ))
                    db_OperationSet.objects.bulk_create(product_list_to_insert)
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
        basicData = objData.BasicData
        testSet = objData.TestSet
        operationSet = objData.OperationSet
        onlyCode = cls_Common.generate_only_code()
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Ui_CaseMaintenance', 'edit_data', errorMsg)
    else:
        obj_db_CaseBaseData = db_CaseBaseData.objects.filter(is_del=0, id=basicData.caseId)
        if obj_db_CaseBaseData.exists():
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    # region 添加操作信息
                    # region 查询以前的数据
                    # region 测试集
                    oldTestSet = []
                    obj_db_TestSet = db_TestSet.objects.filter(is_del=0, case_id=basicData.caseId).order_by('index')
                    for item_testSet in obj_db_TestSet:
                        elementType = ast.literal_eval(item_testSet.elementType)
                        oldTestSet.append({
                            'state': True if item_testSet.state == 1 else False,
                            'index': item_testSet.index,
                            'eventName': item_testSet.eventName,
                            'elementId': item_testSet.elementId,
                            'elementType': elementType,
                            'elementTypeTxt': cls_FindTable.get_element_label_name(elementType),
                            'inputData': item_testSet.inputData,
                            'assertType': item_testSet.assertType,
                            'assertValueType': item_testSet.assertValueType,
                            'assertValue': item_testSet.assertValue,
                        })
                    # endregion
                    # region 操作集
                    oldOperationSet = []
                    obj_db_OperationSet = db_OperationSet.objects.filter(
                        is_del=0, case_id=basicData.caseId).order_by('index')
                    for item_operationSet in obj_db_OperationSet:
                        oldOperationSet.append({
                            'state': True if item_operationSet.state == 1 else False,
                            'index': item_operationSet.index,
                            'location': item_operationSet.location,
                            'operationType': item_operationSet.operationType,
                            'methodsName': item_operationSet.methodsName,
                            'dataBaseId': item_operationSet.dataBaseId,
                            'caseId': item_operationSet.caseId,
                            'remarks': item_operationSet.remarks,
                        })
                    # endregion
                    # region 关联页面
                    obj_db_AssociatedPage = db_AssociatedPage.objects.filter(is_del=0, case_id=basicData.caseId)
                    oldAssociatedPage = [i.page_id for i in obj_db_AssociatedPage]
                    # endregion
                    oldData = {
                        'BasicData': {
                            'caseId': basicData.caseId,
                            'proId': obj_db_CaseBaseData[0].pid_id,
                            'pageId': obj_db_CaseBaseData[0].page_id,
                            'funId': obj_db_CaseBaseData[0].fun_id,
                            'environmentId': obj_db_CaseBaseData[0].environmentId_id,
                            'testType': obj_db_CaseBaseData[0].testType,
                            'labelId': obj_db_CaseBaseData[0].label,
                            'priorityId': obj_db_CaseBaseData[0].priority,
                            'caseName': obj_db_CaseBaseData[0].caseName,
                            'caseState': obj_db_CaseBaseData[0].caseState,
                            'associatedPage': oldAssociatedPage,
                        },
                        'TestSet': oldTestSet,
                        'OperationSet':oldOperationSet,

                    }
                    cls_Logging.record_operation_info(
                        'UI', 'Manual', 3, 'Edit',
                        cls_FindTable.get_pro_name(basicData.proId),
                        cls_FindTable.get_page_name(basicData.pageId),
                        cls_FindTable.get_fun_name(basicData.funId),
                        userId,
                        f'【修改用例】 ID{obj_db_CaseBaseData[0].id}:{obj_db_CaseBaseData[0].caseName}',
                        CUFront=oldData, CURear=responseData
                    )

                    # endregion
                    # endregion
                    # region 历史恢复!!!
                    # restoreData = responseData
                    # restoreData['BasicInfo']['updateTime'] = obj_db_CaseBaseData[0].updateTime.strftime(
                    #     '%Y-%m-%d %H:%M:%S')
                    # restoreData['BasicInfo']['createTime'] = obj_db_CaseBaseData[0].createTime.strftime(
                    #     '%Y-%m-%d %H:%M:%S')
                    # restoreData['BasicInfo']['uid_id'] = obj_db_CaseBaseData[0].uid_id
                    # restoreData['BasicInfo']['cuid'] = obj_db_CaseBaseData[0].cuid
                    # restoreData['onlyCode'] = onlyCode
                    # db_ApiCaseHistory.objects.create(
                    #     pid_id=basicInfo.proId,
                    #     page_id=basicInfo.pageId,
                    #     fun_id=basicInfo.funId,
                    #     case_id=basicInfo.caseId,
                    #     caseName=basicInfo.caseName,
                    #     onlyCode=onlyCode,
                    #     operationType='Edit',
                    #     restoreData=restoreData,
                    #     uid_id=userId
                    # )
                    # endregion
                    # region 删除 各类原数据
                    db_TestSet.objects.filter(
                        is_del=0, case_id=basicData.caseId, onlyCode=obj_db_CaseBaseData[0].onlyCode).update(
                        is_del=1, updateTime=cls_Common.get_date_time()
                    )
                    db_AssociatedPage.objects.filter(
                        is_del=0, case_id=basicData.caseId, onlyCode=obj_db_CaseBaseData[0].onlyCode).update(
                        is_del=1, updateTime=cls_Common.get_date_time()
                    )
                    db_OperationSet.objects.filter(
                        is_del=0, case_id=basicData.caseId, onlyCode=obj_db_CaseBaseData[0].onlyCode).update(
                        is_del=1, updateTime=cls_Common.get_date_time()
                    )
                    # endregion
                    # region 更新基本信息
                    obj_db_CaseBaseData.update(
                        pid_id=basicData.proId, page_id=basicData.pageId, fun_id=basicData.funId,
                        environmentId_id=basicData.environmentId, testType=basicData.testType,
                        label=basicData.labelId, priority=basicData.priorityId, caseName=basicData.caseName,
                        caseState=basicData.caseState, uid_id=userId, updateTime=cls_Common.get_date_time(),
                        onlyCode=onlyCode
                    )
                    # endregion
                    # region 关联页面
                    product_list_to_insert = list()
                    for item_page in basicData.associatedPage:
                        product_list_to_insert.append(db_AssociatedPage(
                            case_id=basicData.caseId,
                            page_id=item_page,
                            is_del=0,
                            onlyCode=onlyCode
                        ))
                    db_AssociatedPage.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region 测试集
                    product_list_to_insert = list()
                    for item_index, item_testSet in enumerate(testSet, 0):
                        product_list_to_insert.append(db_TestSet(
                            case_id=basicData.caseId,
                            index=item_index,
                            state=1 if item_testSet.state else 0,
                            eventName=item_testSet.eventName,
                            elementId=item_testSet.elementId if item_testSet.elementId else None,
                            elementType=item_testSet.elementType,
                            inputData=item_testSet.inputData if item_testSet.inputData else None,
                            assertType=item_testSet.assertType if item_testSet.assertType else None,
                            assertValueType=item_testSet.assertValueType if item_testSet.assertValueType else None,
                            assertValue=item_testSet.assertValue if item_testSet.assertValue else None,
                            is_del=0,
                            onlyCode=onlyCode
                        ))
                    db_TestSet.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region 操作集
                    product_list_to_insert = list()
                    for item_index, item_operationSet in enumerate(operationSet, 1):
                        product_list_to_insert.append(db_OperationSet(
                            case_id=basicData.caseId,
                            index=item_index,
                            state=1 if item_operationSet.state else 0,
                            location=item_operationSet.location,
                            operationType=item_operationSet.operationType,
                            methodsName=item_operationSet.methodsName,
                            caseId=item_operationSet.caseId,
                            dataBaseId=item_operationSet.dataBaseId,
                            sql=item_operationSet.sql,
                            remarks=item_operationSet.remarks,
                            is_del=0,
                            onlyCode=onlyCode
                        ))
                    db_OperationSet.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region 更新元素动态表为无更变
                    db_ElementDynamic.objects.filter(is_del=0, case_id=basicData.caseId).update(
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
        cls_Logging.record_error_info('API', 'Ui_CaseMaintenance', 'delete_data', errorMsg)
    else:
        obj_db_CaseBaseData = db_CaseBaseData.objects.filter(is_del=0, id=caseId)
        if obj_db_CaseBaseData.exists():
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    # region 历史恢复
                    # db_ApiCaseHistory.objects.create(
                    #     pid_id=obj_db_CaseBaseData[0].pid_id,
                    #     page_id=obj_db_CaseBaseData[0].page_id,
                    #     fun_id=obj_db_CaseBaseData[0].fun_id,
                    #     case_id=caseId,
                    #     caseName=obj_db_CaseBaseData[0].caseName,
                    #     onlyCode=onlyCode,
                    #     operationType='Delete',
                    #     uid_id=userId
                    # )
                    # endregion
                    # region 添加操作信息
                    cls_Logging.record_operation_info(
                        'UI', 'Manual', 3, 'Delete',
                        cls_FindTable.get_pro_name(obj_db_CaseBaseData[0].pid_id),
                        cls_FindTable.get_page_name(obj_db_CaseBaseData[0].page_id),
                        cls_FindTable.get_fun_name(obj_db_CaseBaseData[0].fun_id),
                        userId,
                        f'【删除用例】 ID:{caseId}:{obj_db_CaseBaseData[0].caseName}',
                        CUFront=json.dumps(request.POST)
                    )
                    # endregion
                    # region 删除关联信息
                    db_TestSet.objects.filter(
                        is_del=0, case_id=caseId, onlyCode=obj_db_CaseBaseData[0].onlyCode).update(
                        is_del=1, updateTime=cls_Common.get_date_time()
                    )
                    db_AssociatedPage.objects.filter(
                        is_del=0, case_id=caseId, onlyCode=obj_db_CaseBaseData[0].onlyCode).update(
                        is_del=1, updateTime=cls_Common.get_date_time()
                    )
                    db_OperationSet.objects.filter(
                        is_del=0, case_id=caseId, onlyCode=obj_db_CaseBaseData[0].onlyCode).update(
                        is_del=1, updateTime=cls_Common.get_date_time()
                    )
                    obj_db_CaseBaseData.update(is_del=1, updateTime=cls_Common.get_date_time(), uid_id=userId)
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
        cls_Logging.record_error_info('UI', 'Ui_CaseMaintenance', 'load_case_data', errorMsg)
    else:
        obj_db_CaseBaseData = db_CaseBaseData.objects.filter(is_del=0, id=caseId)
        if obj_db_CaseBaseData.exists():
            # region 基础数据
            # 关联页面
            obj_db_AssociatedPage = db_AssociatedPage.objects.filter(is_del=0, case_id=caseId)
            associatedPage = [i.page_id for i in obj_db_AssociatedPage]
            basicData = {
                'pageId': obj_db_CaseBaseData[0].page_id,
                'funId': obj_db_CaseBaseData[0].fun_id,
                'environmentId': obj_db_CaseBaseData[0].environmentId_id,
                'testType': obj_db_CaseBaseData[0].testType,
                'labelId': obj_db_CaseBaseData[0].label,
                'priorityId': obj_db_CaseBaseData[0].priority,
                'caseName': obj_db_CaseBaseData[0].caseName,
                'caseState': obj_db_CaseBaseData[0].caseState,
                'associatedPage': associatedPage
            }
            # endregion
            # region 测试集
            testSet = []
            obj_db_TestSet = db_TestSet.objects.filter(is_del=0, case_id=caseId).order_by('index')
            for i in obj_db_TestSet:
                elementType = ast.literal_eval(i.elementType) if i.elementType else []
                elementTypeTxt = cls_FindTable.get_element_label_name(elementType)
                obj_db_ElementDynamic = db_ElementDynamic.objects.filter(
                    is_del=0, is_read=0, case_id=caseId, element_id=i.elementId)
                if obj_db_ElementDynamic.exists():
                    elementDynamic = 1
                else:
                    if i.elementId:
                        elementDynamic = 0
                    else:
                        elementDynamic = 3
                testSet.append({'id': i.id,
                                'isAddNew': True,
                                'state': True if i.state == 1 else False,
                                'eventName': i.eventName,
                                'elementId': i.elementId,
                                'elementType': elementType,
                                'inputData': i.inputData,
                                'elementDynamic': elementDynamic,
                                'assertType': i.assertType,
                                'elementTypeTxt': elementTypeTxt,
                                'assertValueType': i.assertValueType,
                                'assertValue': i.assertValue,
                                })

            # endregion
            # region 操作集
            operationSet = []
            obj_db_OperationSet = db_OperationSet.objects.filter(is_del=0, case_id=caseId).order_by('index').order_by('location')
            for i in obj_db_OperationSet:
                if i.operationType == 'TestCase':
                    pageId,caseId = ast.literal_eval(i.caseId)
                    obj_db_CaseBaseData = db_CaseBaseData.objects.filter(is_del=0,id=caseId)
                    if obj_db_CaseBaseData.exists():
                        operationData = obj_db_CaseBaseData[0].caseName
                    else:
                        operationData = None
                elif i.operationType == 'Methods':
                    operationData = i.methodsName
                elif i.operationType == 'DataBase':
                    dbId,dbName = ast.literal_eval(i.dataBaseId)
                    operationData = dbName
                else:
                    operationData = None
                operationSet.append({'id': i.id,
                                     'index': i.index,
                                     'state': True if i.state == 1 else False,
                                     'location': i.location,
                                     'operationType': i.operationType,
                                     'methodsName': i.methodsName,
                                     'dataBaseId': ast.literal_eval(i.dataBaseId) if i.dataBaseId else [],
                                     'sql': i.sql,
                                     'caseId': ast.literal_eval(i.caseId) if i.caseId else [],
                                     'remarks': i.remarks,
                                     'operationData': operationData,
                                     })

            # endregion
            response['statusCode'] = 2000
            response['basicData'] = basicData
            response['testSet'] = testSet
            response['operationSet'] = operationSet
        else:
            response['errorMsg'] = "当前选择的数据不存在,请刷新列表后在重新尝试!"
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def get_case_name_items(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)

        proId = objData.proId
        pageIdList = objData.pageIdList.split(',')
        passCaseId = int(objData.passCaseId) if objData.passCaseId else None
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('UI', 'Ui_CaseMaintenance', 'select_data', errorMsg)
    else:
        obj_db_PageManagement = db_PageManagement.objects.filter(is_del=0, id__in=pageIdList)
        for item_page in obj_db_PageManagement:
            children = []
            obj_db_CaseBaseData = db_CaseBaseData.objects.filter(is_del=0, pid_id=proId, page_id=item_page.id)
            for i in obj_db_CaseBaseData:
                if i.id != passCaseId:
                    children.append({
                        'label': i.caseName,
                        'value': i.id,
                    })
            dataList.append({
                'label': item_page.pageName,
                'value': item_page.id,
                'children': children
            })

        response['statusCode'] = 2000
        response['dataList'] = dataList
    return JsonResponse(response)
