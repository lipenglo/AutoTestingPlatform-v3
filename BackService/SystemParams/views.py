from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction

import json
import ast

# Create your db here.
from SystemParams.models import SystemParams as db_SystemParams

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
        sysType = objData.sysType
        keyName = objData.keyName

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'SystemParams', 'select_data', errorMsg)
    else:
        obj_db_SystemParams = db_SystemParams.objects.filter(sysType=sysType).order_by('label')
        if keyName:
            obj_db_SystemParams = obj_db_SystemParams.filter(keyName__icontains=keyName)
        select_db_SystemParams = obj_db_SystemParams[minSize: maxSize]
        for i in select_db_SystemParams:
            dataList.append({
                'id':i.id,
                'label':i.label,
                'keyName':i.keyName,
                'value':i.value,
                'valueType':i.valueType,
                'remarks':i.remarks,
                'updateTime':str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                "userName": f"{i.uid.userName}({i.uid.nickName})",
            })
        response['TableData'] = dataList
        response['Total'] = obj_db_SystemParams.count()
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def edit_data(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        paramsId = request.POST['paramsId']
        value = request.POST['value']
        remarks = request.POST['remarks']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'SystemParams', 'edit_data', errorMsg)
    else:
        obj_db_SystemParams = db_SystemParams.objects.filter(id=paramsId)
        if obj_db_SystemParams.exists():
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    # region 添加操作信息
                    oldData = {
                        'keyName':obj_db_SystemParams[0].keyName,
                        'value':obj_db_SystemParams[0].value,
                        'remarks':obj_db_SystemParams[0].remarks,
                        'uid_id':obj_db_SystemParams[0].uid_id,
                    }
                    newData = json.loads(json.dumps(request.POST))
                    newData['keyName'] = obj_db_SystemParams[0].keyName
                    cls_Logging.record_operation_info(
                        'API', 'Manual', 3, 'Edit',
                        None, None, None,
                        userId,
                        "修改系统参数",
                        oldData, newData
                    )
                    # endregion
                    obj_db_SystemParams.update(value=value,remarks=remarks,uid_id=userId)
            except BaseException as e:  # 自动回滚，不需要任何操作
                response['errorMsg'] = f'更新数据失败:{e}'
            else:
                response['statusCode'] = 2002
        else:
            response['errorMsg'] = '当前系统参数缺失,请联系管理员!'
    return JsonResponse(response)
