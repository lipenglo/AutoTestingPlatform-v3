from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction

import json

# Create your db here.
from PageEnvironment.models import PageEnvironment as db_PageEnvironment

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
        sysType = objData.sysType
        proId = objData.proId
        environmentName = objData.environmentName
        environmentUrl = objData.environmentUrl

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'PageEnvironment', 'select_data', errorMsg)
    else:
        obj_db_PageEnvironment = db_PageEnvironment.objects.filter(
            is_del=0, sysType=sysType, pid_id=proId).order_by('-updateTime')
        if environmentName:
            obj_db_PageEnvironment = obj_db_PageEnvironment.filter(environmentName__icontains=environmentName)
        if environmentUrl:
            obj_db_PageEnvironment = obj_db_PageEnvironment.filter(environmentUrl__icontains=environmentUrl)
        select_db_PageEnvironment = obj_db_PageEnvironment[minSize: maxSize]
        for i in select_db_PageEnvironment:
            dataList.append(
                {"id": i.id,
                 "environmentName": i.environmentName,
                 "environmentUrl": i.environmentUrl,
                 "remarks": i.remarks,
                 "updateTime": str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                 "userName": f"{i.uid.userName}({i.uid.nickName})",
                 }
            )

        response['TableData'] = dataList
        response['Total'] = obj_db_PageEnvironment.count()
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def save_data(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        sysType = request.POST['sysType']
        proId = request.POST['proId']
        environmentName = request.POST['environmentName']
        environmentUrl = request.POST['environmentUrl']
        remarks = request.POST['remarks']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'PageEnvironment', 'data_save', errorMsg)
    else:
        obj_db_PageEnvironment = db_PageEnvironment.objects.filter(
            is_del=0, sysType=sysType, pid_id=proId)
        if obj_db_PageEnvironment.filter(environmentName=environmentName).exists():
            response['errorMsg'] = "当前所属项目下已有相同的环境名称存在,请更改!"
        elif obj_db_PageEnvironment.filter(environmentUrl=environmentUrl).exists():
            response['errorMsg'] = "当前所属项目下已有相同的环境地址存在,请更改!"
        else:
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    db_PageEnvironment.objects.create(
                        sysType=sysType,
                        pid_id=proId,
                        environmentName=environmentName,
                        environmentUrl=environmentUrl,
                        remarks=remarks,
                        is_del=0,
                        uid_id=userId,
                        cuid=userId
                    )
                    # region 添加操作信息
                    cls_Logging.record_operation_info(
                        'API', 'Manual', 3, 'Add',
                        cls_FindTable.get_pro_name(proId), None, None,
                        userId,
                        '新增页面环境', CUFront=json.dumps(request.POST)
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
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        sysType = request.POST['sysType']
        environmentId = int(request.POST['environmentId'])
        proId = request.POST['proId']
        environmentName = request.POST['environmentName']
        environmentUrl = request.POST['environmentUrl']
        remarks = request.POST['remarks']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'PageEnvironment', 'edit_data', errorMsg)
    else:
        obj_db_PageEnvironment = db_PageEnvironment.objects.filter(id=environmentId, is_del=0)
        if obj_db_PageEnvironment.exists():
            select_db_PageEnvironment = db_PageEnvironment.objects.filter(
                sysType=sysType, pid_id=proId, environmentName=environmentName, is_del=0)
            if select_db_PageEnvironment.exists():
                if environmentId == select_db_PageEnvironment[0].id:  # 自己修改自己
                    is_Edit = True
                else:
                    response['errorMsg'] = '当前项目下已有重复环境名称,请更改!'
            else:
                is_Edit = True
            if is_Edit:
                try:
                    with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                        # region 添加操作信息
                        oldData = list(obj_db_PageEnvironment.values())
                        newData = json.dumps(request.POST)
                        cls_Logging.record_operation_info(
                            'API', 'Manual', 3, 'Edit',
                            cls_FindTable.get_pro_name(proId), None, None,
                            userId,
                            '修改页面环境',
                            oldData, newData
                        )
                        # endregion
                        obj_db_PageEnvironment.update(
                            sysType=sysType,
                            pid_id=proId,
                            environmentName=environmentName,
                            environmentUrl=environmentUrl,
                            uid_id=userId,
                            remarks=remarks,
                            updateTime=cls_Common.get_date_time())
                except BaseException as e:  # 自动回滚，不需要任何操作
                    response['errorMsg'] = f'数据修改失败:{e}'
                else:
                    response['statusCode'] = 2002
        else:
            response['errorMsg'] = '未找当前页面环境,请刷新后重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def delete_data(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        environmentId = request.POST['environmentId']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'PageEnvironment', 'delete_data', errorMsg)
    else:
        obj_db_PageEnvironment = db_PageEnvironment.objects.filter(id=environmentId)
        if obj_db_PageEnvironment.exists():
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    obj_db_PageEnvironment.update(
                        is_del=1,
                        updateTime=cls_Common.get_date_time(),
                        uid_id=userId,
                    )
                    # region 添加操作信息
                    cls_Logging.record_operation_info(
                        'API', 'Manual', 3, 'Delete',
                        cls_FindTable.get_pro_name(obj_db_PageEnvironment[0].pid_id), None, None,
                        userId,
                        '删除页面环境', CUFront=json.dumps(request.POST)
                    )
                    # endregion
            except BaseException as e:  # 自动回滚，不需要任何操作
                response['errorMsg'] = f'数据删除失败:{e}'
            else:
                response['statusCode'] = 2003
        else:
            response['errorMsg'] = '未找到当前页面环境,请刷新后重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def get_page_environment_name_items(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        proId = objData.proId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'PageEnvironment', 'get_page_environment_name_items', errorMsg)
    else:
        obj_db_PageEnvironment = db_PageEnvironment.objects.filter(is_del=0, pid_id=proId).order_by('-updateTime')
        for i in obj_db_PageEnvironment:
            dataList.append({
                'label': i.environmentName, 'value': i.id
            })
        response['itemsData'] = dataList
        response['statusCode'] = 2000
    return JsonResponse(response)
