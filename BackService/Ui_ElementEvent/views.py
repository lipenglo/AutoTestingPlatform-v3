from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction

import json
import ast

# Create your db here.
from Ui_ElementEvent.models import ElementEvent as db_ElementEvent
from Ui_ElementEvent.models import ElementEventComponent as db_ElementEventComponent

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

        eventName = objData.eventName
        eventLogo = objData.eventLogo

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('UI', 'Ui_ElementEvent', 'select_data', errorMsg)
    else:
        obj_db_ElementEvent = db_ElementEvent.objects.filter(is_del=0).order_by('index')
        if eventName:
            obj_db_ElementEvent = obj_db_ElementEvent.filter(eventName__icontains=eventName)
        if eventLogo:
            obj_db_ElementEvent = obj_db_ElementEvent.filter(eventLogo__icontains=eventLogo)
        select_db_ElementEvent = obj_db_ElementEvent[minSize: maxSize]
        for i in select_db_ElementEvent:
            obj_db_ElementEventComponent = db_ElementEventComponent.objects.filter(is_del=0, event_id=i.id)
            component = [{'id': item.id,
                          'label': item.label,
                          'state': True if item.state == 1 else False}
                         for item in obj_db_ElementEventComponent]

            dataList.append({
                'id': i.id,
                'eventName': i.eventName,
                'eventLogo': i.eventLogo,
                'remarks': i.remarks,
                'component': component,
                "updateTime": str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                "userName": f"{i.uid.userName}({i.uid.nickName})",
            })
        response['TableData'] = dataList
        response['Total'] = obj_db_ElementEvent.count()
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
        baseData = objData.baseData
        OperationData = objData.OperationData
        onlyCode = cls_Common.generate_only_code()
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('UI', 'Ui_ElementEvent', 'data_save', errorMsg)
    else:
        obj_db_ElementEvent = db_ElementEvent.objects.filter(
            is_del=0, eventName=baseData.eventName, eventLogo=baseData.eventLogo)
        if obj_db_ElementEvent.exists():
            response['errorMsg'] = "已有相同的事件名称或事件标识存在,请更改!"
        else:
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    # region 查询出最大的index 并赋值
                    select_db_ElementEvent = db_ElementEvent.objects.filter(is_del=0)
                    indexList = [i.index for i in select_db_ElementEvent]
                    if indexList:
                        indexList.sort()
                        index = indexList[-1] + 1
                    else:
                        index = 1
                    # endregion
                    # region 基本信息创建
                    save_db_ElementEvent = db_ElementEvent.objects.create(
                        index=index,
                        eventName=baseData.eventName,
                        eventLogo=baseData.eventLogo,
                        remarks=baseData.remarks,
                        is_del=0,
                        uid_id=userId,
                        cuid=userId,
                        onlyCode=onlyCode
                    )
                    # endregion
                    # region 添加元素操作信息
                    product_list_to_insert = list()
                    for index, item_component in enumerate(OperationData, 0):
                        product_list_to_insert.append(db_ElementEventComponent(
                            event_id=save_db_ElementEvent.id,
                            index=index,
                            label=item_component.label,
                            value=item_component.value,
                            remarks=item_component.remarks,
                            state=1 if item_component.state else 0,
                            is_del=0,
                            onlyCode=onlyCode)
                        )
                    db_ElementEventComponent.objects.bulk_create(product_list_to_insert)
                    # endregion
                    # region 添加操作信息
                    cls_Logging.record_operation_info(
                        "UI", 'Manual', 3, 'Add',
                        None, None, None,
                        userId,
                        '【新增元素事件】', CUFront=json.dumps(request.POST)
                    )
                    # endregion
                    # # region 添加历史恢复
                    # restoreData = json.loads(json.dumps(request.POST))
                    # restoreData['updateTime'] = save_db_ProManagement.updateTime.strftime('%Y-%m-%d %H:%M:%S')
                    # restoreData['createTime'] = save_db_ProManagement.createTime.strftime('%Y-%m-%d %H:%M:%S')
                    # restoreData['uid_id'] = save_db_ProManagement.uid_id
                    # restoreData['cuid'] = save_db_ProManagement.cuid
                    # restoreData['onlyCode'] = onlyCode
                    #
                    # db_ProHistory.objects.create(
                    #     pid_id=save_db_ProManagement.id,
                    #     proName=proName,
                    #     onlyCode=onlyCode,
                    #     operationType='Add',
                    #     restoreData=restoreData,
                    #     uid_id=userId,
                    # )
                    # # endregion
            except BaseException as e:  # 自动回滚，不需要任何操作
                response['errorMsg'] = f'保存失败:{e}'
            else:
                response['statusCode'] = 2001
                response['enentId'] = save_db_ElementEvent.id
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
        baseData = objData.baseData
        OperationData = objData.OperationData
        onlyCode = cls_Common.generate_only_code()
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('UI', 'Ui_ElementEvent', 'edit_data', errorMsg)
    else:
        obj_db_ElementEvent = db_ElementEvent.objects.filter(id=baseData.eventId, is_del=0)
        if obj_db_ElementEvent.exists():
            select_db_ElementEvent = db_ElementEvent.objects.filter(eventName=baseData.eventName, is_del=0)
            if select_db_ElementEvent.exists():
                if baseData.eventId == select_db_ElementEvent[0].id:  # 自己修改自己
                    is_Edit = True
                else:
                    response['errorMsg'] = '当前页面已有重复事件名称,请更改!'
            else:
                is_Edit = True
            if is_Edit:
                try:
                    with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                        # region 添加操作信息
                        oldData = list(obj_db_ElementEvent.values())
                        newData = json.dumps(request.POST)
                        cls_Logging.record_operation_info(
                            "UI", 'Manual', 3, 'Edit',
                            None, None, None,
                            userId,
                            '【修改元素事件】',
                            oldData, newData
                        )
                        # endregion
                        # region 删除原信息
                        db_ElementEventComponent.objects.filter(
                            is_del=0, event_id=baseData.eventId, onlyCode=obj_db_ElementEvent[0].onlyCode).update(
                            updateTime=cls_Common.get_date_time(), is_del=1
                        )
                        # endregion
                        # region 基本信息
                        obj_db_ElementEvent.update(
                            eventName=baseData.eventName,
                            eventLogo=baseData.eventLogo,
                            remarks=baseData.remarks,
                            uid_id=userId,
                            updateTime=cls_Common.get_date_time(),
                            onlyCode=onlyCode
                        )
                        # endregion
                        # region 添加元素操作信息
                        product_list_to_insert = list()
                        for index, item_component in enumerate(OperationData, 0):
                            product_list_to_insert.append(db_ElementEventComponent(
                                event_id=baseData.eventId,
                                index=index,
                                label=item_component.label,
                                value=item_component.value,
                                remarks=item_component.remarks,
                                state=1 if item_component.state else 0,
                                is_del=0,
                                onlyCode=onlyCode)
                            )
                        db_ElementEventComponent.objects.bulk_create(product_list_to_insert)
                        # endregion
                        # # region 添加历史恢复
                        # restoreData = json.loads(json.dumps(request.POST))
                        # restoreData['updateTime'] = obj_db_PageManagement[0].updateTime.strftime('%Y-%m-%d %H:%M:%S')
                        # restoreData['createTime'] = obj_db_PageManagement[0].createTime.strftime('%Y-%m-%d %H:%M:%S')
                        # restoreData['uid_id'] = obj_db_PageManagement[0].uid_id
                        # restoreData['cuid'] = obj_db_PageManagement[0].cuid
                        # restoreData['onlyCode'] = onlyCode
                        # db_PageHistory.objects.create(
                        #     pid_id=proId,
                        #     page_id=pageId,
                        #     pageName=pageName,
                        #     onlyCode=onlyCode,
                        #     operationType='Edit',
                        #     restoreData=restoreData,
                        #     uid_id=userId,
                        # )
                        # # endregion
                except BaseException as e:  # 自动回滚，不需要任何操作
                    response['errorMsg'] = f'数据修改失败:{e}'
                else:
                    response['statusCode'] = 2002
        else:
            response['errorMsg'] = '未找当前数据,请刷新后重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def delete_data(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        eventId = request.POST['eventId']
        onlyCode = cls_Common.generate_only_code()
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('UI', 'Ui_ElementEvent', 'delete_data', errorMsg)
    else:
        obj_db_ElementEvent = db_ElementEvent.objects.filter(is_del=0, id=eventId)
        if obj_db_ElementEvent.exists():
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    db_ElementEventComponent.objects.filter(
                        is_del=0, event_id=eventId, onlyCode=obj_db_ElementEvent[0].onlyCode).update(
                        is_del=1, updateTime=cls_Common.get_date_time())
                    obj_db_ElementEvent.update(
                        is_del=1,
                        updateTime=cls_Common.get_date_time(),
                        uid_id=userId,
                    )
                    # region 添加操作信息
                    cls_Logging.record_operation_info(
                        "UI", 'Manual', 3, 'Delete',
                        None, None, None,
                        userId,
                        '【删除元素事件】', CUFront=json.dumps(request.POST)
                    )
                    # endregion
                    # # region 添加历史恢复
                    # db_PageHistory.objects.create(
                    #     pid_id=obj_db_PageManagement[0].pid_id,
                    #     page_id=pageId,
                    #     pageName=obj_db_PageManagement[0].pageName,
                    #     onlyCode=cls_Common.generate_only_code(),
                    #     operationType='Delete',
                    #     uid_id=userId,
                    # )
                    # # endregion
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
def charm_event_data(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(request.body)
        objData = cls_object_maker(responseData)
        charmType = objData.CharmType  # true 新增，false 修改
        baseData = objData.baseData
        OperationData = objData.OperationData
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('UI', 'Ui_ElementEvent', 'charm_event_data', errorMsg)
    else:
        # region 验证 基本信息
        obj_db_ElementEvent = db_ElementEvent.objects.filter(
            is_del=0, eventName=baseData.eventName, eventLogo=baseData.eventLogo)
        if obj_db_ElementEvent.exists():
            if charmType:
                dataList.append({
                    'stepsName': '基本信息',
                    'errorMsg': "当前页面下已有相同事件名称或事件标识,请更改!",
                    'updateTime': cls_Common.get_date_time()})
            else:
                if obj_db_ElementEvent.exists():
                    if baseData.eventId == obj_db_ElementEvent[0].id:
                        pass
                    else:
                        dataList.append({
                            'stepsName': '基本信息',
                            'errorMsg': "当前页面下已有相同事件名称或事件标识,请更改!",
                            'updateTime': cls_Common.get_date_time()})
        # endregion
        # region 验证 元素操作信息
        for index, item_location in enumerate(OperationData, 1):
            if item_location.state:
                if not item_location.label:
                    dataList.append({
                        'stepsName': '定位信息',
                        'errorMsg': f'第{index}行:操作名称不可为空!',
                        'updateTime': cls_Common.get_date_time()})
                if not item_location.value:
                    dataList.append({
                        'stepsName': '定位信息',
                        'errorMsg': f'第{index}行:参数值不可为空!',
                        'updateTime': cls_Common.get_date_time()})
        # endregion
        response['statusCode'] = 2000
        response['TableData'] = dataList
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def load_data(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        eventId = objData.eventId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('UI', 'Ui_ElementEvent', 'load_data', errorMsg)
    else:
        obj_db_ElementEvent = db_ElementEvent.objects.filter(is_del=0, id=eventId)
        if obj_db_ElementEvent.exists():
            baseData = {
                'eventName': obj_db_ElementEvent[0].eventName,
                'eventLogo': obj_db_ElementEvent[0].eventLogo,
                'remarks': obj_db_ElementEvent[0].remarks,
            }
            obj_db_ElementEventComponent = db_ElementEventComponent.objects.filter(
                is_del=0, event_id=eventId).order_by('index')
            componentTable = [{'id': i.id,
                               'state': True if i.state == 1 else False,
                               'label': i.label,
                               'value': i.value,
                               'remarks': i.remarks
                               }
                              for i in obj_db_ElementEventComponent]

            response['statusCode'] = 2000
            response['baseData'] = baseData
            response['componentTable'] = componentTable
        else:
            response['errorMsg'] = "当前选择的数据不存在,请刷新列表后重新尝试!"
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 加载事件排序的一级事件名称
def load_operation_data(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('UI', 'Ui_ElementEvent', 'load_operation_data', errorMsg)
    else:
        obj_db_ElementEvent = db_ElementEvent.objects.filter(is_del=0).order_by('index')
        for i in obj_db_ElementEvent:
            # children = []
            # obj_db_ElementEventComponent = db_ElementEventComponent.objects.filter(is_del=0,event_id=i.id)
            # for item in obj_db_ElementEventComponent:
            #     children.append({'id': item.id,
            #                      'label': item.label,
            #                      'index': item.index,
            #                      'allowDrag': False,  # 能否拖动
            #                      'allowDrop': False})  # 能否拖入
            dataList.append({'id': i.id,
                             'index': i.index,
                             'label': i.eventName,
                             'allowDrag': True,  # 能否拖动
                             'allowDrop': False,  # 能否拖入
                             })

        response['statusCode'] = 2000
        response['treeData'] = dataList
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 更新一级目录的排序
def update_operation_sort(request):
    response = {}
    try:
        responseData = json.loads(request.body)
        objData = cls_object_maker(responseData)
        TreeData = objData.TreeData
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('UI', 'Ui_ElementEvent', 'update_operation_sort', errorMsg)
    else:
        for index, item in enumerate(TreeData, 1):
            db_ElementEvent.objects.filter(is_del=0, id=item.id).update(
                index=index, updateTime=cls_Common.get_date_time())

        response['statusCode'] = 2002
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 加载元素操作类型
def get_element_operation_type_items(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('UI', 'Ui_ElementEvent', 'get_element_operation_type_items', errorMsg)
    else:
        obj_db_ElementEvent = db_ElementEvent.objects.filter(is_del=0).order_by('index')
        for i in obj_db_ElementEvent:
            children = []
            obj_db_ElementEventComponent = db_ElementEventComponent.objects.filter(
                is_del=0,event_id=i.id).order_by('index')
            for item in obj_db_ElementEventComponent:
                children.append({
                    'id':item.id,
                    'label':item.label,
                    'value':item.value,
                    'disabled':False if item.state ==1 else True
                })
            dataList.append({
                'id':i.id,
                'label':i.eventName,
                'value':i.eventLogo,
                'children':children
            })
        response['statusCode'] = 2000
        response['dataList'] = dataList
    return JsonResponse(response)
