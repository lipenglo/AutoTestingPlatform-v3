from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

# Create reference here.
from ClassData.Logger import Logging
from ClassData.GlobalDecorator import GlobalDer
from ClassData.FindCommonTable import FindTable
from ClassData.FileOperations import FileOperations

# Create info here.
cls_Logging = Logging()
cls_GlobalDer = GlobalDer()
cls_FindTable = FindTable()
cls_FileOperations = FileOperations()


# Create your views here.
@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def upLoad_to_temp_path(request):
    response = {
        'fileList': []
    }
    try:
        fileList = [{'paramsName': item_file, 'file': request.FILES[item_file]} for item_file in request.FILES]
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('ALL', 'upLoad', 'upLoad_to_temp_path', errorMsg)
    else:
        for fileObj in fileList:
            # originalName = fileObj['file'].name# 原始文件名称
            toTemp = cls_FileOperations.file_to_path(fileObj)
            if toTemp['state']:
                fileName = toTemp['fileName']
                filePath = toTemp['filePath']
                response['fileList'].append({'filePath': filePath, 'fileName': fileName})
            else:
                response['errorMsg'] = toTemp['errorMsg']
                break
        if 'errorMsg' not in response:
            response['statusCode'] = 2001
    return JsonResponse(response)
