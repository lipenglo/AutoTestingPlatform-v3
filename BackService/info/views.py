from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction

import json
import ast

# Create your db here.
from info.models import OperateInfo as db_OperateInfo
from info.models import PushInfo as db_PushInfo
from login.models import UserTable as db_UserTable
from login.models import UserBindRole as db_UserBindRole

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
@require_http_methods(["GET"])  # 操作信息
def select_operational_info(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        roleId = cls_FindTable.get_roleId(userId)
        isAdminGroup = cls_FindTable.get_role_is_admin(roleId)
        sysType = objData.sysType
        remindType = objData.remindType
        isRead = objData.isRead

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'info', 'select_operational_info', errorMsg)
    else:
        if isAdminGroup:
            obj_db_OperateInfo = db_OperateInfo.objects.filter().order_by('-createTime')
            if sysType:
                obj_db_OperateInfo = obj_db_OperateInfo.filter(sysType=sysType)
            if remindType:
                obj_db_OperateInfo = obj_db_OperateInfo.filter(remindType=remindType)
            if isRead:
                obj_db_OperateInfo = obj_db_OperateInfo.filter(is_read=isRead)
            select_db_OperateInfo = obj_db_OperateInfo[minSize: maxSize]
            total = obj_db_OperateInfo.count()
            for i in select_db_OperateInfo:
                dataList.append({
                    'id': i.id,
                    'triggerType': i.triggerType,
                    'level': i.level,
                    'remindType': i.remindType,
                    'sysType': i.sysType,
                    'toPro': i.toPro,
                    'toPage': i.toPage,
                    'toFun': i.toFun,
                    'info': i.info,
                    # 'editInfo':editInfo,
                    'tableItem': [{
                        'CUFront': i.CUFront,
                        'CURear': i.CURear,
                    }],
                    'is_read': i.is_read,
                    "userName": f"{i.uid.userName}({i.uid.nickName})",
                    'createTime': str(i.createTime.strftime('%Y-%m-%d %H:%M:%S')),
                })
        else:
            obj_db_PushInfo = db_PushInfo.objects.filter(uid_id=userId).order_by('-createTime')
            select_db_PushInfo = obj_db_PushInfo[minSize: maxSize]
            if remindType:
                obj_db_PushInfo = obj_db_PushInfo.filter(oinfo__remindType=remindType)
                select_db_PushInfo = obj_db_PushInfo[minSize: maxSize]
            if isRead:
                obj_db_PushInfo = obj_db_PushInfo.filter(is_read=isRead)
                select_db_PushInfo = obj_db_PushInfo[minSize: maxSize]
            total = obj_db_PushInfo.count()
            for i in select_db_PushInfo:
                # 排除创建者看到自己推给别人的信息
                # if i.oinfo.uid_id != userId:
                dataList.append({
                    'id': i.id,
                    'triggerType': i.oinfo.triggerType,
                    'level': i.oinfo.level,
                    'remindType': i.oinfo.remindType,
                    'sysType': i.oinfo.sysType,
                    'toPro': i.oinfo.toPro,
                    'toPage': i.oinfo.toPage,
                    'toFun': i.oinfo.toFun,
                    'info': i.oinfo.info,
                    'tableItem': [{
                        'CUFront': i.oinfo.CUFront,
                        'CURear': i.oinfo.CURear,
                    }],
                    'is_read': i.is_read,
                    "userName": f"{i.oinfo.uid.userName}({i.oinfo.uid.nickName})",
                    'createTime': str(i.oinfo.createTime.strftime('%Y-%m-%d %H:%M:%S')),
                })
        response['TableData'] = dataList
        response['Total'] = total
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 独立用户的操作信息
def user_operational_info(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        sysType = objData.sysType
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'info', 'select_operational_info', errorMsg)
    else:
        # 加载推送信息
        obj_db_PushInfo = db_PushInfo.objects.filter(uid_id=userId, is_read=0).order_by('-updateTime')
        if sysType:
            obj_db_PushInfo = obj_db_PushInfo.filter(oinfo__sysType=sysType)
        select_db_PushInfo = obj_db_PushInfo[minSize: maxSize]
        obj_db_UserTable = db_UserTable.objects.filter(id=userId)
        if obj_db_UserTable.exists():
            for i in select_db_PushInfo:
                sourcePath = ""
                # 排除创建者看到自己推给别人的信息
                # if i.oinfo.uid_id != userId:
                if i.oinfo.toPro:
                    sourcePath += f'{i.oinfo.toPro} | '
                if i.oinfo.toPage:
                    sourcePath += f'{i.oinfo.toPage} | '
                if i.oinfo.toFun:
                    sourcePath += f'{i.oinfo.toFun}'
                dataList.append({
                    'id': i.id,
                    'triggerType': i.oinfo.triggerType,
                    'level': i.oinfo.level,
                    'remindType': i.oinfo.remindType,
                    'sysType': i.oinfo.sysType,
                    'sourcePath':sourcePath,
                    # 'toPro':i.oinfo.toPro,
                    # 'toPage': i.oinfo.toPage,
                    # 'toFun': i.oinfo.toFun,
                    'info': i.oinfo.info,
                    # 'CUFront': i.CUFront,
                    # 'CURear': i.CURear,
                    'is_read': i.is_read,
                    "userName": f"{i.oinfo.uid.userName}({i.oinfo.uid.nickName})",
                    'createTime': str(i.oinfo.createTime.strftime('%Y-%m-%d %H:%M:%S')),
                })

        response['TableData'] = dataList
        response['Total'] = obj_db_PushInfo.count()
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 更改未读为已读取
def edit_isread_state(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        infoId = request.POST['infoId']
        types = request.POST['types']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'info', 'edit_isread_state', errorMsg)
    else:
        try:
            with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                if types == 'ALL':  # 全读
                    # 使用推送信息去更新操作信息
                    db_PushInfo.objects.filter(uid_id=userId).update(updateTime=cls_Common.get_date_time(), is_read=1)
                else:
                    db_PushInfo.objects.filter(id=infoId).update(updateTime=cls_Common.get_date_time(), is_read=1)
        except BaseException as e:  # 自动回滚，不需要任何操作
            response['errorMsg'] = f"已读操作失败:{e}"
        else:
            response['statusCode'] = 2002
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 更改操作信息中的Error未读为已读取
def edit_operational_info_state(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        roleId = cls_FindTable.get_roleId(userId)
        isAdminGroup = cls_FindTable.get_role_is_admin(roleId)
        oId = request.POST['oId']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'info', 'edit_operational_info_state', errorMsg)
    else:
        try:
            with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                if isAdminGroup:
                    db_OperateInfo.objects.filter(id=oId).update(is_read=1, updateTime=cls_Common.get_date_time())
                else:
                    obj_db_PushInfo = db_PushInfo.objects.filter(id=oId)
                    if obj_db_PushInfo.exists():
                        db_OperateInfo.objects.filter(id=obj_db_PushInfo[0].oinfo_id).update(
                            is_read=1, updateTime=cls_Common.get_date_time())
                        obj_db_PushInfo.update(is_read=1, updateTime=cls_Common.get_date_time())
        except BaseException as e:  # 自动回滚，不需要任何操作
            response['errorMsg'] = f"已读操作失败:{e}"
        else:
            response['statusCode'] = 2002
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 根据条件来全读取
def setting_operational_read_all(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        roleId = cls_FindTable.get_roleId(userId)
        isAdminGroup = cls_FindTable.get_role_is_admin(roleId)
        sysType = request.POST['sysType']
        remindType = request.POST['remindType']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'info', 'setting_operational_read_all', errorMsg)
    else:
        try:
            with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                if isAdminGroup:
                    db_OperateInfo.objects.filter(sysType=sysType,remindType=remindType).update(
                        is_read=1, updateTime=cls_Common.get_date_time())
                else:
                    obj_db_PushInfo = db_PushInfo.objects.filter(sysType=sysType,remindType=remindType)
                    if obj_db_PushInfo.exists():
                        db_OperateInfo.objects.filter(id=obj_db_PushInfo[0].oinfo_id).update(
                            is_read=1, updateTime=cls_Common.get_date_time())
                        obj_db_PushInfo.update(is_read=1, updateTime=cls_Common.get_date_time())
        except BaseException as e:  # 自动回滚，不需要任何操作
            response['errorMsg'] = f"已读操作失败:{e}"
        else:
            response['statusCode'] = 2002
    return JsonResponse(response)
