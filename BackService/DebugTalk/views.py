from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction
from django.conf import settings

import json

# Create your db here.
from DebugTalk.models import DebugTalk as db_DebugTalk

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
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        sysType = objData.sysType
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'DebugTalk>API', 'select_data', errorMsg)
    else:
        if sysType == "API":
            fileName = 'ApiDebug'
        else:
            fileName = 'UiDebug'
        try:
            with open(f"{settings.BASE_DIR}/DebugTalk/Data/{fileName}.py", encoding="utf8") as f:
                readText = f.read()
            obj_db_DebugTalk = db_DebugTalk.objects.filter().order_by('-updateTime')
            if obj_db_DebugTalk.exists():
                titleInfo = f"{obj_db_DebugTalk[0].uid.userName}({obj_db_DebugTalk[0].uid.nickName}) " \
                            f"最后更新时间:{str(obj_db_DebugTalk[0].updateTime.strftime('%Y-%m-%d %H:%M:%S'))}"
            else:
                titleInfo = ""
        except Exception as e:
            errorMsg = f"读取DebugTalk错误:{e}"
            response['errorMsg'] = errorMsg
            cls_Logging.record_error_info('API', 'DebugTalk', 'select_data', errorMsg)
        else:
            response['titleInfo'] = titleInfo
            response['Text'] = readText
            response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def data_save(request):
    response = {}
    try:
        responseData = json.loads(request.body)
        objData = cls_object_maker(responseData)
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        sysType = objData.sysType
        text = objData.text
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'DebugTalk', 'data_save', errorMsg)
    else:
        if sysType == "API":
            fileName = 'ApiDebug'
        else:
            fileName = 'UiDebug'
        try:
            with open(f"{settings.BASE_DIR}/DebugTalk/Data/{fileName}.py", 'w', encoding="utf8") as f:
                f.write(text)
            db_DebugTalk.objects.create(
                codeInfo=text,
                uid_id=userId,
            )
        except BaseException as e:
            response['errorMsg'] = f'数据保存失败:{e}'
        else:
            response['statusCode'] = 2001
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def run_debug(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        sysType = objData.sysType
        methods = objData.methods
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'DebugTalk>API', 'run_debug', errorMsg)
    else:
        try:
            if sysType == "API":
                import DebugTalk.Data.ApiDebug
                strCmd = f"DebugTalk.Data.ApiDebug.{methods}"
                retData = eval(strCmd)
            else:
                pass
                import DebugTalk.Data.UiDebug
                strCmd = f"DebugTalk.Data.UiDebug.{methods}"
                retData = eval(strCmd)
        except Exception as e:
            errorMsg = f"{methods} 执行错误:{e}"
            response['errorMsg'] = errorMsg
            cls_Logging.record_error_info('API', 'DebugTalk', 'run_debug', errorMsg)
        else:
            response['retData'] = retData
            response['statusCode'] = 2000
    return JsonResponse(response)
