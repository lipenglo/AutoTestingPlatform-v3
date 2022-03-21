from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction

import json

# Create your db here.
from GlobalVariable.models import GlobalVariable as db_GlobalVariable

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
        proId = int(objData.proId)
        sysType = objData.sysType
        globalType = objData.globalType
        globalName = objData.globalName

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'GlobalVariable', 'select_data', errorMsg)
    else:
        obj_db_GlobalVariable = db_GlobalVariable.objects.filter(
            is_del=0, sysType=sysType,pid_id=proId).order_by('-updateTime')
        if globalType:
            obj_db_GlobalVariable = obj_db_GlobalVariable.filter(globalType=globalType)
        if globalName:
            obj_db_GlobalVariable = obj_db_GlobalVariable.filter(globalName__icontains=globalName)
        select_db_GlobalVariable = obj_db_GlobalVariable[minSize: maxSize]
        for i in select_db_GlobalVariable:
            dataList.append(
                {"id": i.id,
                 "globalType": i.globalType,
                 "globalName": i.globalName,
                 "globalValue": i.globalValue,
                 "remarks": i.remarks,
                 "updateTime": str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                 "userName": f"{i.uid.userName}({i.uid.nickName})",
                 }
            )

        response['TableData'] = dataList
        response['Total'] = obj_db_GlobalVariable.count()
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
        globalType = request.POST['globalType']
        globalName = request.POST['globalName']
        globalValue = request.POST['globalValue']
        remarks = request.POST['remarks']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'GlobalVariable', 'save_data', errorMsg)
    else:
        obj_db_GlobalVariable = db_GlobalVariable.objects.filter(
            is_del=0, sysType=sysType, globalName=globalName)
        if obj_db_GlobalVariable.exists():
            response['errorMsg'] = "系统内以有相同的环境名称存在,请更改!"
        else:
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    db_GlobalVariable.objects.create(
                        sysType=sysType,
                        pid_id=proId,
                        globalType=globalType,
                        globalName=globalName,
                        globalValue=globalValue,
                        remarks=remarks,
                        uid_id=userId,
                        cuid=userId,
                        is_del=0,
                    )
                    # region 添加操作信息
                    cls_Logging.record_operation_info(
                        'API', 'Manual', 3, 'Add',
                        cls_FindTable.get_pro_name(proId), None, None,
                        userId,
                        '新增全局变量', CUFront=json.dumps(request.POST)
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
        proId = request.POST['proId']
        globalId = int(request.POST['globalId'])
        globalType = request.POST['globalType']
        globalName = request.POST['globalName']
        globalValue = request.POST['globalValue']
        remarks = request.POST['remarks']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'GlobalVariable', 'edit_data', errorMsg)
    else:
        obj_db_GlobalVariable = db_GlobalVariable.objects.filter(id=globalId, is_del=0)
        if obj_db_GlobalVariable.exists():
            select_db_GlobalVariable = db_GlobalVariable.objects.filter(
                sysType=sysType, pid_id=proId, globalName=globalName, is_del=0)
            if select_db_GlobalVariable.exists():
                if globalId == select_db_GlobalVariable[0].id:  # 自己修改自己
                    is_Edit = True
                else:
                    response['errorMsg'] = '当前系统下已有重复变量名称,请更改!'
            else:
                is_Edit = True
            if is_Edit:
                try:
                    with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                        # region 添加操作信息
                        oldData = list(obj_db_GlobalVariable.values())
                        newData = json.dumps(request.POST)
                        cls_Logging.record_operation_info(
                            'API', 'Manual', 3, 'Edit',
                            cls_FindTable.get_pro_name(proId), None, None,
                            userId,
                            '修改全局变量',
                            oldData, newData
                        )
                        # endregion
                        obj_db_GlobalVariable.update(
                            sysType=sysType,
                            pid_id=proId,
                            globalType=globalType,
                            globalName=globalName,
                            globalValue=globalValue,
                            remarks=remarks,
                            uid_id=userId,
                            updateTime=cls_Common.get_date_time())
                except BaseException as e:  # 自动回滚，不需要任何操作
                    response['errorMsg'] = f'数据修改失败:{e}'
                else:
                    response['statusCode'] = 2002
        else:
            response['errorMsg'] = '未找当前当前的变量数据,请刷新后重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def delete_data(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        globalId = request.POST['globalId']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'GlobalVariable', 'delete_data', errorMsg)
    else:
        obj_db_GlobalVariable = db_GlobalVariable.objects.filter(id=globalId)
        if obj_db_GlobalVariable.exists():
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    obj_db_GlobalVariable.update(
                        is_del=1,
                        updateTime=cls_Common.get_date_time(),
                        uid_id=userId,
                    )
                    # region 添加操作信息
                    cls_Logging.record_operation_info(
                        'API', 'Manual', 3, 'Delete',
                        cls_FindTable.get_pro_name(obj_db_GlobalVariable[0].pid_id), None, None,
                        userId,
                        '删除全局变量', CUFront=json.dumps(request.POST)
                    )
                    # endregion
            except BaseException as e:  # 自动回滚，不需要任何操作
                response['errorMsg'] = f'数据删除失败:{e}'
            else:
                response['statusCode'] = 2003
        else:
            response['errorMsg'] = '未找到当前系统下的全局变量,请刷新后重新尝试!'
    return JsonResponse(response)
