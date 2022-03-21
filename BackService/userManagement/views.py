from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
# from django.conf import settings
from django.db import transaction
from django.contrib.auth import hashers

import json

# Create your db here.
from login.models import UserTable as db_UserTable
from login.models import UserBindRole as db_UserBindRole
from django.contrib.auth.models import User as db_DjUser
from role.models import BasicRole as db_BasicRole

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
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        userName = objData.userName
        isLock = objData.isLock
        isActivation = objData.isActivation

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'userManagement','select_data', errorMsg)
    else:
        obj_db_UserTable = db_UserTable.objects.filter(is_del=0).order_by("-is_activation")
        select_db_UserTable = obj_db_UserTable[minSize: maxSize]

        if userName:
            obj_db_UserTable = obj_db_UserTable.filter(userName__icontains=userName)
            select_db_UserTable = obj_db_UserTable[minSize: maxSize]
        if isLock:
            obj_db_UserTable = obj_db_UserTable.filter(is_lock=isLock)
            select_db_UserTable = obj_db_UserTable[minSize: maxSize]
        if isActivation:
            obj_db_UserTable = obj_db_UserTable.filter(is_activation=isActivation)
            select_db_UserTable = obj_db_UserTable[minSize: maxSize]

        for i in select_db_UserTable:
            roldId = None
            roleName = "游客"
            obj_db_UserBindRole = db_UserBindRole.objects.filter(is_del='0', user_id=i.id)
            if obj_db_UserBindRole:
                roldId = obj_db_UserBindRole[0].role_id
                roleName = obj_db_UserBindRole[0].role.roleName
            dataList.append(
                {"id": i.id,
                 "userImage": str(eval(i.userImg), encoding='utf-8') if i.userImg else None,
                 "userName": i.userName,
                 "nickName": i.nickName,
                 "emails": i.emails,
                 "roldId": roldId,
                 "roleName": roleName,
                 "is_lock": i.is_lock,
                 "is_activation": i.is_activation,
                 }
            )

        response['TableData'] = dataList
        response['Total'] = obj_db_UserTable.count()
        response['statuscode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 用户激活
def user_activation(request):
    response = {}
    try:
        userId = request.POST['userId']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'userManagement','user_activation', errorMsg)
    else:
        obj_db_UserTable = db_UserTable.objects.filter(id=userId, is_del=0)
        if obj_db_UserTable.exists():
            obj_db_UserTable.update(is_activation=1, updateTime=cls_Common.get_date_time())
            response['statusCode'] = 2002
        else:
            response['errorMsg'] = "此用户不存在数据库中!"
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 用户状态修改
def edit_islock_state(request):
    response = {}
    try:
        userId = request.POST['userId']  # 被修改状态的用户ID
        state = request.POST['state']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'userManagement','user_activation', errorMsg)
    else:
        obj_db_UserTable = db_UserTable.objects.filter(id=userId, is_del=0)
        if obj_db_UserTable.exists():
            obj_db_UserTable.update(is_lock=state, updateTime=cls_Common.get_date_time())
            response['statusCode'] = 2002
        else:
            response['errorMsg'] = "此用户不存在数据库中!"
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 用户删除
def delete_data(request):
    response = {}
    try:
        userId = request.POST['userId']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'userManagement','delete_data', errorMsg)
    else:
        obj_db_UserTable = db_UserTable.objects.filter(id=userId, is_del=0)
        if obj_db_UserTable.exists():
            if obj_db_UserTable[0].userName == "admin":
                response['errorMsg'] = "初始超级管理员用户不可删除!"
            else:
                try:
                    with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                        db_DjUser.objects.filter(id=obj_db_UserTable[0].userId).delete()
                        obj_db_UserTable.update(is_del=1, updateTime=cls_Common.get_date_time())
                        db_UserBindRole.objects.filter(is_del=0,user_id=userId).update(
                            is_del=1, updateTime=cls_Common.get_date_time())
                except BaseException as e:  # 自动回滚，不需要任何操作
                    response['errorMsg'] = f"用户删除失败:{e}"
                else:
                    response['statusCode'] = 2003
        else:
            response['errorMsg'] = "该用户不在数据库中!"
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 内部注册
def internal_registered(request):
    response = {}
    try:
        userName = request.POST['userName']
        passWord = request.POST['passWord']
        nickName = request.POST['nickName']
        emails = request.POST['emails']
        roleId = request.POST['roleId']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'userManagement','internal_registered', errorMsg)
    else:
        if userName.lower() == "admin":
            errorMsg = '用户注册失败:不可使用敏感用户名注册!'
            response['errorMsg'] = errorMsg
        else:
            find_db_UserTable = db_UserTable.objects.filter(userName=userName, is_del=0)
            if find_db_UserTable.exists():
                response['errorMsg'] = '已有相同用户名注册,请更换用户名!'
            else:
                try:
                    with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                        create_DjUser = db_DjUser.objects.create_user(username=userName, password=passWord)
                        # is_activation 默认未激活，需要联系管理员进行配置权限工作
                        save_db_UserTable = db_UserTable.objects.create(
                            userId=create_DjUser.id, userName=userName, nickName=nickName, emails=emails,
                            is_lock=0, is_activation=0, is_del=0
                        )
                        db_UserBindRole.objects.create(
                            user_id=save_db_UserTable.id,
                            role_id=roleId,
                            is_del=0,
                        )
                except Exception as e:  # 自动回滚，不需要任何操作
                    errorMsg = f'用户注册失败：{e}!'
                    response['errorMsg'] = errorMsg
                    cls_Logging.record_error_info('HOME', 'userManagement','internal_registered', errorMsg)
                else:
                    response['statusCode'] = 2001
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 用户修改
def edit_data(request):
    response = {}
    try:
        userId = request.POST['userId']
        passWord = request.POST['passWord']
        nickName = request.POST['nickName']
        emails = request.POST['emails']
        roleId = request.POST['roleId']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'userManagement','edit_data', errorMsg)
    else:
        obj_db_UserTable = db_UserTable.objects.filter(id=userId, is_del=0)
        if obj_db_UserTable.exists():
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    # 修改用户信息
                    obj_db_UserTable.update(nickName=nickName, emails=emails, updateTime=cls_Common.get_date_time())
                    # 修改用户权限
                    obj_db_UserBindRole = db_UserBindRole.objects.filter(user_id=userId, is_del=0)
                    if obj_db_UserBindRole.exists():
                        db_UserBindRole.objects.filter(user_id=userId, is_del=0).update(role_id=roleId)
                    else:
                        db_UserBindRole.objects.create(
                            user_id=userId,
                            role_id=roleId,
                            is_del=0
                        )
                    # 修改用户密码
                    obj_db_DjUser = db_DjUser.objects.get(id=obj_db_UserTable[0].userId)
                    obj_db_DjUser.password = hashers.make_password(password=passWord)
                    obj_db_DjUser.save()
            except BaseException as e:  # 自动回滚，不需要任何操作
                response['errorMsg'] = f"用户信息修改失败:{e}"
            else:
                response['statusCode'] = 2002
        else:
            response['errorMsg'] = "该用户不在数据库中!"
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def get_user_name_items(request):
    response = {}
    dataList = []

    obj_db_BasicRole = db_BasicRole.objects.filter(is_del=0)
    for item_role in obj_db_BasicRole:
        children = []
        obj_db_UserBindRole = db_UserBindRole.objects.filter(is_del=0, role_id=item_role.id)
        for i in obj_db_UserBindRole:
            children.append({'label': f'{i.user.userName}({i.user.nickName})', 'value': i.user_id})
        dataList.append({'label': item_role.roleName, 'value': item_role.id, 'children': children})
    response['itemsData'] = dataList
    response['statusCode'] = 2000
    return JsonResponse(response)