from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
# from django.conf import settings
from django.db import transaction
# from django.contrib.auth import hashers

import json

# Create your db here.
from routerPar.models import Router as db_Router
from role.models import RoleBindMenu as db_RoleBindMenu

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
        menuName = objData.menuName
        menuLevel = objData.menuLevel
        sysType = objData.sysType

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'routerPar','select_data', errorMsg)
    else:
        obj_db_Router = db_Router.objects.filter(is_del=0)
        select_db_RouterPar = obj_db_Router[minSize: maxSize]
        if menuName:
            obj_db_Router = obj_db_Router.filter(menuName__icontains=menuName)
            select_db_RouterPar = obj_db_Router[minSize: maxSize]
        if menuLevel:
            obj_db_Router = obj_db_Router.filter(level=menuLevel)
            select_db_RouterPar = obj_db_Router[minSize: maxSize]
        if sysType:
            obj_db_Router = obj_db_Router.filter(sysType=sysType)
            select_db_RouterPar = obj_db_Router[minSize: maxSize]

        for i in select_db_RouterPar:
            level = "一级菜单" if i.level == 1 else "二级菜单"
            dataList.append(
                {"id": i.id,
                 "levelText": level,
                 # "index": i.index,
                 "menuName": i.menuName,
                 "routerPath": i.routerPath,
                 "sysType": i.sysType,
                 "icon":i.icon,
                 "updateTime": str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                 }
            )

        response['TableData'] = dataList
        response['Total'] = obj_db_Router.count()
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 显示右侧 层级预览图
def get_preview_data(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        sysType = objData.sysType
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME','routerPar', 'get_preview_data', errorMsg)
    else:
        obj_db_Router = db_Router.objects.filter(is_del=0).order_by('sortNum')
        find_db_Router = obj_db_Router.filter(sysType=sysType, level='1')
        for item_router in find_db_Router:
            # 根据1级菜单id,查询二级菜单
            children = []
            select_db_RouterPar = obj_db_Router.filter(belogId=item_router.id)
            for i in select_db_RouterPar:
                children.append({'id': i.id,
                                 'label': i.menuName,
                                 'sortNum': i.sortNum,
                                 'allowDrag': True,  # 能否拖动
                                 'allowDrop': False})  # 能否拖入
            dataList.append({'id': item_router.id,
                             'label': item_router.menuName,
                             'allowDrag': True,  # 1层菜单不可拖动
                             'allowDrop': False,
                             'children': children})
        response['statusCode'] = 2000
        response['TreeData'] = dataList

    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 加载上级菜单
def get_belogid_table(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)

        sysType = objData.sysType
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'routerPar','get_belogid_table', errorMsg)
    else:
        obj_db_Router = db_Router.objects.filter(is_del=0, level='1', sysType=sysType).order_by('index')
        for i in obj_db_Router:
            dataList.append({'label': i.menuName, 'value': i.id})

        response['dataList'] = dataList
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def save_data(request):
    response = {}
    try:
        sysType = request.POST['sysType']
        menuLevel = request.POST['menuLevel']
        menuName = request.POST['menuName']
        routerPath = request.POST['routerPath']
        belogId = request.POST['belogId']
        icon = request.POST['icon']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'routerPar','data_save', errorMsg)
    else:
        #  效验保存的数据
        obj_db_Router = db_Router.objects.filter(is_del=0, sysType=sysType)
        if obj_db_Router.filter(menuName=menuName).exists():
            response['errorMsg'] = "当前输入的菜单名称已存在,请更改!"
        else:
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    save_db_Router = db_Router.objects.create(
                        sysType=sysType,
                        level=menuLevel,
                        menuName=menuName,
                        routerPath=routerPath,
                        belogId=belogId if belogId else None,
                        icon=icon,
                        is_del=0,
                    )

                    if menuLevel == '1':
                        select_db_Router = obj_db_Router.filter(level=1)
                        sortNum = select_db_Router.count()+1
                        db_Router.objects.filter(id=save_db_Router.id).update(sortNum=sortNum)
                    else:
                        select_db_Router = obj_db_Router.filter(belogId=belogId)
                        index = f"{belogId}-{select_db_Router.count()}"
                        sortNum = select_db_Router.count()
                        db_Router.objects.filter(id=save_db_Router.id).update(index=index, sortNum=sortNum)
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
        routerId = request.POST['routerId']
        sysType = request.POST['sysType']
        menuLevel = request.POST['menuLevel']
        menuName = request.POST['menuName']
        routerPath = request.POST['routerPath']
        belogId = request.POST['belogId']
        icon = request.POST['icon']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'routerPar','edit_data', errorMsg)
    else:
        obj_db_Router = db_Router.objects.filter(id=routerId)
        if obj_db_Router.exists():
            obj_db_Router.update(level=menuLevel,
                                 menuName=menuName,
                                 routerPath=routerPath,
                                 belogId=belogId if belogId else None,
                                 sysType=sysType,
                                 icon=icon,
                                 updateTime=cls_Common.get_date_time()
                                 )

            response['statusCode'] = 2002
        else:
            response['errorMsg'] = "当前修改的路由不存在于数据库中!"
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def delete_data(request):
    response = {}
    try:
        routerId = request.POST['routerId']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'routerPae','delete_data', errorMsg)
    else:
        obj_db_Router = db_Router.objects.filter(is_del=0, id=routerId)
        if obj_db_Router.exists():
            if obj_db_Router[0].level == 1:
                select_db_Router = db_Router.objects.filter(is_del=0, belogId=obj_db_Router[0].id)
                if select_db_Router.exists():
                    response['errorMsg'] = f"当前一级菜单下存在二级菜单数据,请先删除2级菜单数据后在进行删除操作!"
                else:
                    try:
                        with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                            db_RoleBindMenu.objects.filter(is_del=0, router_id=routerId).update(
                                is_del=1, updateTime=cls_Common.get_date_time())
                            obj_db_Router.update(is_del=1, updateTime=cls_Common.get_date_time())
                    except BaseException as e:  # 自动回滚，不需要任何操作
                        response['errorMsg'] = f"删除路由菜单失败:{e}"
                    else:
                        response['statusCode'] = 2003
            else:
                try:
                    with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                        db_RoleBindMenu.objects.filter(is_del=0, router_id=routerId).update(
                            is_del=1, updateTime=cls_Common.get_date_time())
                        obj_db_Router.update(is_del=1, updateTime=cls_Common.get_date_time())
                except BaseException as e:  # 自动回滚，不需要任何操作
                    response['errorMsg'] = f"删除路由菜单失败:{e}"
                else:
                    response['statusCode'] = 2003
        else:
            response['errorMsg'] = "当前路由参数不存在于数据库中!"
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 更新路由排序
def update_router_sort(request):
    response = {}
    try:
        responseData = json.loads(request.body)
        objData = cls_object_maker(responseData)
        treeData = objData.TreeData
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME','routerPar','update_router_sort', errorMsg)
    else:
        for item_level_1_index,item_tree in enumerate(treeData,1):
            db_Router.objects.filter(id=item_tree.id).update(
                sortNum=item_level_1_index, updateTime=cls_Common.get_date_time())
            for index, item_children in enumerate(item_tree.children, 1):
                routerId = item_children.id
                obj_db_Router = db_Router.objects.filter(id=routerId)
                if obj_db_Router.exists():
                    belogId = f"{obj_db_Router[0].belogId}-{index}"
                    obj_db_Router.update(sortNum=index, index=belogId, updateTime=cls_Common.get_date_time())
        response['statusCode'] = 2002
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 编辑时加载路由信息
def load_router_data(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)

        routerId = objData.routerId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'routerPar','get_belogid_table', errorMsg)
    else:
        obj_db_Router = db_Router.objects.filter(id=routerId)
        if obj_db_Router.exists():
            dataTable = {
                'sysType': obj_db_Router[0].sysType,
                'menuLevel': str(obj_db_Router[0].level),
                'belogId': obj_db_Router[0].belogId,
                'menuName': obj_db_Router[0].menuName,
                'routerPath': obj_db_Router[0].routerPath,
                'icon':obj_db_Router[0].icon,
            }
            response['statusCode'] = 2000
            response['dataTable'] = dataTable
        else:
            response['errorMsg'] = "当前选择的路由信息不存在,请刷新后在重新尝试!"

    return JsonResponse(response)
