from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib import auth
from django.db import transaction

import json

# Create your views here.
from rest_framework.authtoken.models import Token as db_Token
from django.contrib.auth.models import User as db_DjUser
from login.models import UserTable as db_UserTable
from info.models import OperateInfo as db_OperateInfo
from login.models import UserBindRole as db_UserBindRole

# Create reference here.
from ClassData.Logger import Logging

# Create info here.
cls_Logging = Logging()


# Create your views here.
@cls_Logging.log
@require_http_methods(["POST"])  # 外部注册
def registered(request):
    response = {}
    try:
        userName = request.POST['userName']
        passWord = request.POST['passWord']
        nickName = request.POST['nickName']
        emails = request.POST['emails']
        roleId = request.POST['roleId']
    except Exception as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('LOGIN', 'login', 'registered', errorMsg)
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
                    cls_Logging.record_error_info('LOGIN', 'login', 'registered', errorMsg)
                else:
                    response['statusCode'] = 2001
    return JsonResponse(response)


@cls_Logging.log
@require_http_methods(["POST"])
def login_in(request):
    response = {}
    try:
        userName = request.POST['userName']
        passWord = request.POST['passWord']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('LOGIN', 'login', 'login_in', errorMsg)
    else:
        obj_db_Djuser = auth.authenticate(username=userName, password=passWord)
        obj_db_UserTable = db_UserTable.objects.filter(userName=userName)

        if obj_db_Djuser and obj_db_UserTable:
            if obj_db_UserTable.filter(is_lock=1):
                response['errorMsg'] = '用户已被禁用,请联系管理员进行操作！'
            elif obj_db_UserTable.filter(is_activation=0):
                response['errorMsg'] = '用户属于未激活状态,请联系管理员进行操作！'
            else:
                token = db_Token.objects.filter(user=obj_db_Djuser)  # 内置查询方法
                token.delete()

                token = db_Token.objects.create(user=obj_db_Djuser)  # 生成用户的token值
                db_OperateInfo.objects.create(
                    level=4, sysType='LOGIN',
                    toPage='登录页',
                    toFun='登录',
                    uid_id=obj_db_UserTable[0].id,
                    remindType='Other')
                response['code'] = 1001  # 登录时传给vue拦截器验证用的
                response['statusCode'] = 2000
                response['nickName'] = obj_db_UserTable[0].nickName
                # response['userImg'] = ''
                response['token'] = token.key
        else:
            response['errorMsg'] = '用户名或密码错误!'
    return JsonResponse(response)
