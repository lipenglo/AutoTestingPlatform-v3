from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction

import json

# Create your db here.
from role.models import BasicRole as db_BasicRole
from role.models import RoleBindMenu as db_RoleBindMenu
from routerPar.models import Router as db_Router
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
@require_http_methods(["GET"])
def select_data(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        roleName = objData.roleName

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'role', 'select_data', errorMsg)
    else:
        obj_db_BasicRole = db_BasicRole.objects.filter(is_del=0).order_by('updateTime').order_by('dataType')
        select_db_BasicRole = obj_db_BasicRole[minSize: maxSize]
        if roleName:
            obj_db_BasicRole = obj_db_BasicRole.filter(roleName__icontains=roleName)
            select_db_BasicRole = obj_db_BasicRole[minSize: maxSize]
        for i in select_db_BasicRole:
            # region 绑定用户
            bindUsers = ""
            obj_db_UserBindRole = db_UserBindRole.objects.filter(role_id=i.id, is_del=0)
            for index, item_BindRole in enumerate(obj_db_UserBindRole, 1):
                bindUsers += item_BindRole.user.userName
                if obj_db_UserBindRole.count() - index != 0:
                    bindUsers += "、"
            # endregion
            dataList.append(
                {"id": i.id,
                 "roleName": i.roleName,
                 "bindUsers": bindUsers,
                 "updateTime": str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                 "userName": i.uid.userName,
                 }
            )

        response['TableData'] = dataList
        response['Total'] = obj_db_BasicRole.count()
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def save_data(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        roleName = request.POST['roleName']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'role', 'save_data', errorMsg)
    else:
        obj_db_BasicRole = db_BasicRole.objects.filter(is_del='0', roleName=roleName)
        if obj_db_BasicRole.exists():
            response['errorMsg'] = '当前新增角色名称存在,请更改！'
        else:
            db_BasicRole.objects.create(
                roleName=roleName,
                dataType=1,
                uid_id=userId,
                is_admin=0,
                is_del=0,
            )
            response['statusCode'] = 2001
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def edit_data(request):
    response = {}
    update_db_BasicRole = None
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        roleId = request.POST['roleId']
        roleName = request.POST['roleName']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'role', 'save_data', errorMsg)
    else:
        obj_db_BasicRole = db_BasicRole.objects.filter(id=roleId)
        if obj_db_BasicRole[0].is_admin == 1:  # 系统级别数据
            response['errorMsg'] = '系统级别角色不可修改!'
        else:
            obj_db_BasicRole = db_BasicRole.objects.filter(roleName=roleName, is_del='0')
            if obj_db_BasicRole.exists():
                if roleId == obj_db_BasicRole[0].id:  # 自己修改自己
                    update_db_BasicRole = obj_db_BasicRole.filter(is_del='0', id=roleId).update(
                        roleName=roleName,
                        uid_id=userId,
                        updateTime=cls_Common.get_date_time())
                else:
                    response['errorMsg'] = '已有重复角色,请更改!'
            else:
                update_db_BasicRole = db_BasicRole.objects.filter(is_del='0', id=roleId).update(
                    roleName=roleName,
                    uid_id=userId,
                    updateTime=cls_Common.get_date_time())
        if update_db_BasicRole:
            response['statusCode'] = 2002
        return JsonResponse(response)
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def delete_data(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        roleId = request.POST['roleId']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'role', 'delete_data', errorMsg)
    else:
        obj_db_BasicRole = db_BasicRole.objects.filter(is_del=0, id=roleId)
        if obj_db_BasicRole.exists():
            if obj_db_BasicRole[0].dataType == 0:
                response['errorMsg'] = f"当前角色为系统级别,不可删除!"
            else:
                select_db_BasicRole = db_BasicRole.objects.filter(is_del=0, roleName='游客')
                if select_db_BasicRole.exists():
                    touristsId = select_db_BasicRole[0].id
                else:
                    touristsId = db_BasicRole.objects.create(
                        roleName='游客',
                        dataType=0,
                        uid_id=userId,
                        is_admin=0,
                        is_del=0,
                    )
                try:
                    with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                        obj_db_BasicRole.update(
                            is_del=1,
                            uid_id=userId,
                            updateTime=cls_Common.get_date_time()
                        )
                        db_UserBindRole.objects.filter(is_del=0, role_id=roleId).update(
                            role_id=touristsId,
                            updateTime=cls_Common.get_date_time()
                        )
                except BaseException as e:  # 自动回滚，不需要任何操作
                    response['errorMsg'] = f"删除角色失败:{e}"
                else:
                    response['statusCode'] = 2003
        else:
            response['errorMsg'] = "该数据不存在于数据库中!"
    return JsonResponse(response)


@cls_Logging.log
@require_http_methods(["GET"])  # 无TOKEN的获取,只有主页用来获取角色，不可在系统内使用
def no_token_get_role_name_items(request):
    response = {}
    dataList = []
    obj_db_BasicRole = db_BasicRole.objects.filter(is_del=0).order_by('dataType')
    for i in obj_db_BasicRole:
        dataList.append({
            'label': i.roleName, 'value': i.id
        })
    response['itemsData'] = dataList
    response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def get_role_name_items(request):
    response = {}
    dataList = []
    obj_db_BasicRole = db_BasicRole.objects.filter(is_del=0).order_by('dataType')
    for i in obj_db_BasicRole:
        dataList.append({
            'label': i.roleName, 'value': i.id
        })
    response['itemsData'] = dataList
    response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 传入所属系统，获取对应系统的菜单数据
def get_menu_list(request):
    response = {}
    treeData = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        roleId = objData.roleId
        sysType = objData.sysType
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'role', 'get_menulist', errorMsg)
    else:
        # 根据 归属页面查询出这个页面下所有的菜单
        obj_db_Router = db_Router.objects.filter(is_del=0).order_by('sortNum')
        find_db_Router = obj_db_Router.filter(sysType=sysType, level='1')
        for item_db_router in find_db_Router:
            # 根据1级菜单id,查询二级菜单
            children = []
            select_db_RouterPar = obj_db_Router.filter(belogId=item_db_router.id)
            for i in select_db_RouterPar:
                children.append({'id': i.id,
                                 'label': i.menuName})
            treeData.append({'id': item_db_router.id,
                             'label': item_db_router.menuName,
                             'children': children})

        # 用角色查询，哪些是已经被勾选的数据
        obj_db_RoleBindMenu = db_RoleBindMenu.objects.filter(sysType=sysType,is_del=0, role_id=roleId)
        defaultChecked = [i.router_id for i in obj_db_RoleBindMenu]
        # for i in obj_db_RoleBindMenu:
        #     defaultChecked.append(i.router_id)
        # defaultChecked = [i.router_id for i in obj_db_RoleBindMenu
        #                   if i.router.level == 2 or i.router.menuName == "Home"]

        response['statusCode'] = 2000
        response['TreeData'] = treeData
        response['DefaultChecked'] = defaultChecked
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 保存角色权限
def save_role_permissions(request):
    response = {}
    try:
        responseData = json.loads(request.body)
        objData = cls_object_maker(responseData)
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        roleId = objData.roleId  # 角色ID
        sysType = objData.sysType
        menuChecked = objData.MenuChecked
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'role', 'save_role_permissions', errorMsg)
    else:
        try:
            with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                # 将原权限数据清空
                db_RoleBindMenu.objects.filter(is_del=0, role_id=roleId, sysType=sysType).update(
                    is_del=1, updateTime=cls_Common.get_date_time())

                # 重新新增新的权限
                for item_routerId in menuChecked:
                    obj_db_RouterPar = db_Router.objects.filter(id=item_routerId)
                    if obj_db_RouterPar.exists():
                        routerId = obj_db_RouterPar[0].id
                        db_RoleBindMenu.objects.create(
                            role_id=roleId,
                            router_id=routerId,
                            sysType=sysType,
                            uid_id=userId,
                            is_del=0
                        )
                    else:
                        response['errorMsg'] = f"菜单权限中,{item_routerId} 不存在，请重新刷新后在进行绑定!"
                        break
        except BaseException as e:  # 自动回滚，不需要任何操作
            response['errorMsg'] = f"角色权限修改失败:{e}"
        else:
            response['statusCode'] = 2001
    return JsonResponse(response)
