from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction

import json
import ast

# Create your db here.
from PageManagement.models import PageManagement as db_PageManagement
from FunManagement.models import FunManagement as db_FunManagement
from PageManagement.models import PageHistory as db_PageHistory
from ProjectManagement.models import ProManagement as db_ProManagement

# Create reference here.
from ClassData.Logger import Logging
from ClassData.GlobalDecorator import GlobalDer
from ClassData.FindCommonTable import FindTable
from ClassData.Common import Common
from ClassData.ImageProcessing import ImageProcessing
from ClassData.ObjectMaker import object_maker as cls_object_maker

# Create info here.
cls_Logging = Logging()
cls_GlobalDer = GlobalDer()
cls_FindTable = FindTable()
cls_Common = Common()
cls_ImageProcessing = ImageProcessing()


# Create your views here.
@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def select_data(request):
    response = {}
    dataList = []
    sysType = None
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        sysType = objData.sysType
        proId = objData.proId
        pageName = objData.pageName

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info(sysType, 'PageMaintenancet', 'select_data', errorMsg)
    else:
        obj_db_PageManagement = db_PageManagement.objects.filter(
            is_del=0, sysType=sysType, pid_id=proId).order_by('-updateTime')
        if pageName:
            obj_db_PageManagement = obj_db_PageManagement.filter(pageName__icontains=pageName)
        select_db_PageManagement = obj_db_PageManagement[minSize: maxSize]
        for i in select_db_PageManagement:
            dataList.append(
                {"id": i.id,
                 "pageName": i.pageName,
                 "remarks": i.remarks,
                 "updateTime": str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                 "userName": f"{i.uid.userName}({i.uid.nickName})",
                 }
            )

        response['TableData'] = dataList
        response['Total'] = obj_db_PageManagement.count()
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def save_data(request):
    response = {}
    sysType = None
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        sysType = request.POST['sysType']
        proId = request.POST['proId']
        pageName = request.POST['pageName']
        remarks = request.POST['remarks']
        onlyCode = cls_Common.generate_only_code()
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info(sysType, 'PageManagement', 'data_save', errorMsg)
    else:
        obj_db_PageManagement = db_PageManagement.objects.filter(
            is_del=0, sysType=sysType, pid_id=proId, pageName=pageName)
        if obj_db_PageManagement.exists():
            response['errorMsg'] = "当前所属项目下已有相同的所属页面存在,请更改!"
        else:
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    # region 保存基本信息
                    save_db_PageManagement = db_PageManagement.objects.create(
                        sysType=sysType,
                        pid_id=proId,
                        pageName=pageName,
                        remarks=remarks,
                        is_del=0,
                        uid_id=userId,
                        cuid=userId,
                        onlyCode=onlyCode,
                    )
                    # endregion
                    # region 添加操作信息
                    cls_Logging.record_operation_info(
                        sysType, 'Manual', 3, 'Add',
                        cls_FindTable.get_pro_name(proId), pageName, None,
                        userId,
                        '新增页面', CUFront=json.dumps(request.POST)
                    )
                    # endregion
                    # region 添加历史恢复
                    restoreData = json.loads(json.dumps(request.POST))
                    restoreData['updateTime'] = save_db_PageManagement.updateTime.strftime('%Y-%m-%d %H:%M:%S')
                    restoreData['createTime'] = save_db_PageManagement.createTime.strftime('%Y-%m-%d %H:%M:%S')
                    restoreData['uid_id'] = save_db_PageManagement.uid_id
                    restoreData['cuid'] = save_db_PageManagement.cuid
                    restoreData['onlyCode'] = onlyCode
                    db_PageHistory.objects.create(
                        pid_id=proId,
                        page_id=save_db_PageManagement.id,
                        pageName=pageName,
                        onlyCode=cls_Common.generate_only_code(),
                        operationType='Add',
                        restoreData=restoreData,
                        uid_id=userId,
                    )
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
    is_Edit = False
    sysType = None
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        sysType = request.POST['sysType']
        proId = request.POST['proId']
        pageId = int(request.POST['pageId'])
        pageName = request.POST['pageName']
        remarks = request.POST['remarks']
        onlyCode = cls_Common.generate_only_code()
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info(sysType, 'PageManagement', 'edit_data', errorMsg)
    else:
        obj_db_PageManagement = db_PageManagement.objects.filter(id=pageId, is_del=0)
        if obj_db_PageManagement.exists():
            select_db_PageManagement = db_PageManagement.objects.filter(
                sysType=sysType, pid_id=proId, pageName=pageName, is_del=0)
            if select_db_PageManagement.exists():
                if pageId == select_db_PageManagement[0].id:  # 自己修改自己
                    is_Edit = True
                else:
                    response['errorMsg'] = '当前项目下已有重复页面名称,请更改!'
            else:
                is_Edit = True
            if is_Edit:
                try:
                    with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                        # region 添加操作信息
                        oldData = list(obj_db_PageManagement.values())
                        newData = json.dumps(request.POST)
                        cls_Logging.record_operation_info(
                            sysType, 'Manual', 3, 'Edit',
                            cls_FindTable.get_pro_name(proId), pageName, None,
                            userId,
                            '修改页面',
                            oldData, newData
                        )
                        # endregion
                        # region 基本信息
                        db_PageManagement.objects.filter(is_del=0, id=pageId).update(
                            pageName=pageName,
                            uid_id=userId,
                            remarks=remarks,
                            updateTime=cls_Common.get_date_time(),
                            onlyCode=onlyCode)
                        # endregion
                        # region 添加历史恢复
                        restoreData = json.loads(json.dumps(request.POST))
                        restoreData['updateTime'] = obj_db_PageManagement[0].updateTime.strftime('%Y-%m-%d %H:%M:%S')
                        restoreData['createTime'] = obj_db_PageManagement[0].createTime.strftime('%Y-%m-%d %H:%M:%S')
                        restoreData['uid_id'] = obj_db_PageManagement[0].uid_id
                        restoreData['cuid'] = obj_db_PageManagement[0].cuid
                        restoreData['onlyCode'] = onlyCode
                        db_PageHistory.objects.create(
                            pid_id=proId,
                            page_id=pageId,
                            pageName=pageName,
                            onlyCode=onlyCode,
                            operationType='Edit',
                            restoreData=restoreData,
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
    sysType = None
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        sysType = request.POST['sysType']
        pageId = request.POST['pageId']
        onlyCode = cls_Common.generate_only_code()
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info(sysType, 'PageManagement', 'delete_data', errorMsg)
    else:
        obj_db_PageManagement = db_PageManagement.objects.filter(id=pageId)
        if obj_db_PageManagement.exists():
            obj_db_FunManagement = db_FunManagement.objects.filter(is_del=0, page_id=pageId)
            if obj_db_FunManagement.exists():
                response['errorMsg'] = '当前所属页面下已有所属功能数据,请删除下级所属功能后在重新尝试删除'
            else:
                try:
                    with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                        obj_db_PageManagement.update(
                            is_del=1,
                            updateTime=cls_Common.get_date_time(),
                            uid_id=userId,
                            onlyCode=onlyCode,
                        )
                        # region 添加操作信息
                        cls_Logging.record_operation_info(
                            sysType, 'Manual', 3, 'Delete',
                            cls_FindTable.get_pro_name(obj_db_PageManagement[0].pid_id),
                            obj_db_PageManagement[0].pageName, None,
                            userId,
                            '删除页面', CUFront=json.dumps(request.POST)
                        )
                        # endregion
                        # region 添加历史恢复
                        db_PageHistory.objects.create(
                            pid_id=obj_db_PageManagement[0].pid_id,
                            page_id=pageId,
                            pageName=obj_db_PageManagement[0].pageName,
                            onlyCode=cls_Common.generate_only_code(),
                            operationType='Delete',
                            uid_id=userId,
                        )
                        # endregion
                except BaseException as e:  # 自动回滚，不需要任何操作
                    response['errorMsg'] = f'数据删除失败:{e}'
                else:
                    response['statusCode'] = 2003
        else:
            response['errorMsg'] = '未找到当前所属页面,请刷新后重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def get_page_name_items(request):
    response = {}
    dataList = []
    sysType = None
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        proId = objData.proId
        sysType = objData.sysType
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info(sysType, 'PageMaintenancet', 'get_page_name_items', errorMsg)
    else:
        obj_db_PageManagement = db_PageManagement.objects.filter(is_del=0, pid_id=proId).order_by('-updateTime')
        for i in obj_db_PageManagement:
            dataList.append({
                'label': i.pageName, 'value': i.id
            })
        response['itemsData'] = dataList
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 查询历史恢复
def select_history(request):
    response = {}
    dataList = []
    sysType = None
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)

        sysType = objData.sysType
        pageId = objData.pageId
        pageName = objData.pageName
        operationType = objData.operationType

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info(sysType, 'PageManagement', 'select_history', errorMsg)
    else:
        if pageId:
            obj_db_PageHistory = db_PageHistory.objects.filter(
                page_id=pageId, page__sysType=sysType).order_by('-createTime')
        else:
            obj_db_PageHistory = db_PageHistory.objects.filter(page__sysType=sysType).order_by('-createTime')
            if pageName:
                obj_db_PageHistory = obj_db_PageHistory.filter(pageName__icontains=pageName).order_by('-createTime')
            if operationType:
                obj_db_PageHistory = obj_db_PageHistory.filter(operationType=operationType).order_by('-createTime')
        select_db_PageHistory = obj_db_PageHistory[minSize: maxSize]
        for i in select_db_PageHistory:
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
                'pageName': i.pageName,
                'operationType': i.operationType,
                'tableItem': tableItem,
                'createTime': str(i.createTime.strftime('%Y-%m-%d %H:%M:%S')),
                "userName": f"{i.uid.userName}({i.uid.nickName})",
            })
        response['TableData'] = dataList
        response['Total'] = obj_db_PageHistory.count()
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 恢复数据 只有管理员组或是项目创建人才可以恢复
def restor_data(request):
    response = {}
    sysType = None
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        roleId = cls_FindTable.get_roleId(userId)
        is_admin = cls_FindTable.get_role_is_admin(roleId)
        historyId = request.POST['historyId']
        sysType = request.POST['sysType']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info(sysType, 'PageManagement', 'restor_data', errorMsg)
    else:
        obj_db_PageHistory = db_PageHistory.objects.filter(id=historyId)
        if obj_db_PageHistory.exists():
            # 恢复时是管理员或是 当前项目的创建人时才可恢复
            if is_admin or obj_db_PageHistory[0].pid.cuid == userId:
                try:
                    with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                        obj_db_ProManagement = db_ProManagement.objects.filter(is_del=0,
                                                                               id=obj_db_PageHistory[0].pid_id)
                        if obj_db_ProManagement.exists():
                            restoreData = obj_db_PageHistory[0].restoreData
                            if obj_db_PageHistory[0].operationType in ["Add", "Edit"]:
                                restoreData = ast.literal_eval(restoreData)
                                obj_db_PageManagement = db_PageManagement.objects.filter(
                                    id=obj_db_PageHistory[0].page_id)
                                if obj_db_PageManagement.exists:
                                    # region 操作记录
                                    cls_Logging.record_operation_info(
                                        'API', 'Manual', 3, 'Update',
                                        cls_FindTable.get_pro_name(obj_db_PageHistory[0].pid_id),
                                        cls_FindTable.get_page_name(obj_db_PageHistory[0].page_id),
                                        None,
                                        userId,
                                        f'【恢复所属页面】 '
                                        f'ID:{obj_db_PageHistory[0].page_id}:'
                                        f"{obj_db_PageHistory[0].pageName}",
                                    )
                                    # endregion
                                    obj_db_PageManagement.update(
                                        pid_id=restoreData['proId'],
                                        pageName=restoreData['pageName'],
                                        remarks=restoreData['remarks'],
                                        updateTime=restoreData['updateTime'],
                                        createTime=restoreData['createTime'],
                                        uid_id=restoreData['uid_id'],
                                        cuid=restoreData['cuid'],
                                        is_del=0,
                                        onlyCode=restoreData['onlyCode'],
                                    )
                                else:
                                    raise ValueError('此数据原始数据在库中无法查询到!')
                            else:
                                raise ValueError('使用了未录入的操作类型!')
                        else:
                            response['errorMsg'] = f"当前恢复的页面上级所属项目不存在,恢复失败!"
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
@require_http_methods(["GET"])  # 获取关联页面
def get_associated_page_name_items(request):
    response = {}
    dataList = []
    sysType = None
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        sysType = objData.sysType
        passPageId = int(objData.passPageId) if objData.passPageId else None
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info(sysType, 'PageMaintenancet', 'get_associated_page_name_items', errorMsg)
    else:
        obj_db_PageManagement = db_PageManagement.objects.filter(is_del=0,sysType=sysType)
        for i in obj_db_PageManagement:
            if i.id != passPageId:
                dataList.append({
                    'label':i.pageName,
                    'value':i.id
                })
        response['statusCode'] = 2000
        response['dataList'] = dataList
    return JsonResponse(response)
