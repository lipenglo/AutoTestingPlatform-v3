from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction
from django.conf import settings

import json
import ast

# Create your db here.
from DataBaseEnvironment.models import DataBase as db_DataBase

# Create reference here.
from ClassData.Logger import Logging
from ClassData.GlobalDecorator import GlobalDer
from ClassData.FindCommonTable import FindTable
from ClassData.Common import Common
from ClassData.ImageProcessing import ImageProcessing
from ClassData.ObjectMaker import object_maker as cls_object_maker
from ClassData.Request import RequstOperation
from ClassData.TestReport import ApiReport
from ClassData.OpenApi import Swagger
from ClassData.FileOperations import FileOperations
from ClassData.DataBase import DataBase
from ClassData.DataSecurity import DataSecurity

# Create info here.
cls_Logging = Logging()
cls_GlobalDer = GlobalDer()
cls_FindTable = FindTable()
cls_Common = Common()
cls_ImageProcessing = ImageProcessing()
cls_RequstOperation = RequstOperation()
cls_ApiReport = ApiReport()
cls_Swagger = Swagger()
cls_FileOperations = FileOperations()
cls_DataBase = DataBase()
cls_DataSecurity = DataSecurity()


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
        # sysType = objData.sysType
        dbType = objData.dbType
        dataBaseIp = objData.dataBaseIp

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'DataBaseEnvironment', 'select_data', errorMsg)
    else:
        obj_db_DataBase = db_DataBase.objects.filter(is_del=0).order_by('-updateTime')
        if dbType:
            obj_db_DataBase = obj_db_DataBase.filter(dbType=dbType)
        if dataBaseIp:
            obj_db_DataBase = obj_db_DataBase.filter(dataBaseIp__icontains=dataBaseIp)
        select_db_DataBase = obj_db_DataBase[minSize: maxSize]
        for i in select_db_DataBase:
            connectTest = cls_DataBase.connect_test(
                'MySql', i.dataBaseIp, i.port, i.userName, cls_DataSecurity.aes_decode(ast.literal_eval(i.passWord)))
            if connectTest['state']:
                state = True
            else:
                state = False
            dataList.append(
                {"id": i.id,
                 "dbType": i.dbType,
                 "dataBaseIp": i.dataBaseIp,
                 "port": i.port,
                 "dbUser": i.userName,
                 "dbpwd": i.passWord,
                 "remarks": i.remarks,
                 'state': state,
                 "updateTime": str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                 "userName": f"{i.uid.userName}({i.uid.nickName})",
                 }
            )

        response['TableData'] = dataList
        response['Total'] = obj_db_DataBase.count()
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def test_connect(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        dbType = objData.dbType
        dataBaseIp = objData.dataBaseIp
        port = objData.port
        userName = objData.userName
        passWord = objData.passWord
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'DataBaseEnvironment', 'test_connect', errorMsg)
    else:
        conn = cls_DataBase.connect_test(dbType, dataBaseIp, port, userName, passWord)
        if conn['state']:
            response['statusCode'] = 2000
        else:
            response['errorMsg'] = conn['errorMsg']
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def save_data(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        # sysType = request.POST['sysType']
        dbType = request.POST['dbType']
        dataBaseIp = request.POST['dataBaseIp']
        port = request.POST['port']
        userName = request.POST['userName']
        passWord = request.POST['passWord']
        remarks = request.POST['remarks']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'DataBaseEnvironment', 'data_save', errorMsg)
    else:
        obj_db_DataBase = db_DataBase.objects.filter(is_del=0, sysType=sysType, dataBaseIp=dataBaseIp, port=port)
        if obj_db_DataBase.exists():
            response['errorMsg'] = "当前保存的数据库已有相同数据,请更改!"
        else:
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    aesEncrypt = cls_DataSecurity.aes_encrypt(passWord)
                    # region 保存基本信息
                    db_DataBase.objects.create(
                        # sysType=sysType,
                        dbType=dbType,
                        dataBaseIp=dataBaseIp,
                        port=port,
                        userName=userName,
                        passWord=aesEncrypt,
                        remarks=remarks,
                        is_del=0,
                        uid_id=userId,
                        cuid=userId,
                    )
                    # endregion
                    # region 添加操作信息
                    cls_Logging.record_operation_info(
                        'API', 'Manual', 3, 'Add',
                        None, None, None,
                        userId,
                        '新增数据库环境', CUFront=json.dumps(request.POST)
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
        dbId = int(request.POST['dbId'])
        # sysType = request.POST['sysType']
        dbType = request.POST['dbType']
        dataBaseIp = request.POST['dataBaseIp']
        port = request.POST['port']
        userName = request.POST['userName']
        passWord = request.POST['passWord']
        remarks = request.POST['remarks']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'DataBaseEnvironment', 'edit_data', errorMsg)
    else:
        obj_db_DataBase = db_DataBase.objects.filter(id=dbId, is_del=0)
        if obj_db_DataBase.exists():
            select_db_DataBase = db_DataBase.objects.filter(dbType=dbType, dataBaseIp=dataBaseIp, port=port, is_del=0)
            if select_db_DataBase.exists():
                if dbId == select_db_DataBase[0].id:  # 自己修改自己
                    is_Edit = True
                else:
                    response['errorMsg'] = '当前已有重复类型数据,请更改!'
            else:
                is_Edit = True
            if is_Edit:
                try:
                    with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                        # region 添加操作信息
                        oldData = list(obj_db_DataBase.values())
                        newData = json.dumps(request.POST)
                        cls_Logging.record_operation_info(
                            'API', 'Manual', 3, 'Edit',
                            None, None, None,
                            userId,
                            '修改数据库环境',
                            oldData, newData
                        )
                        # endregion
                        # region 基础信息
                        if passWord == obj_db_DataBase[0].passWord:
                            aesEncrypt = passWord
                        else:
                            aesEncrypt = cls_DataSecurity.aes_encrypt(passWord)  # 加密
                        obj_db_DataBase.update(
                            # sysType=sysType,
                            dbType=dbType,
                            dataBaseIp=dataBaseIp,
                            port=port,
                            userName=userName,
                            passWord=aesEncrypt,
                            remarks=remarks,
                            uid_id=userId,
                            updateTime=cls_Common.get_date_time())
                        # endregion
                except BaseException as e:  # 自动回滚，不需要任何操作
                    response['errorMsg'] = f'数据修改失败:{e}'
                else:
                    response['statusCode'] = 2002
        else:
            response['errorMsg'] = '未找当前当前的数据库数据,请刷新后重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def delete_data(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        dbId = request.POST['dbId']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'DataBaseEnvironment', 'delete_data', errorMsg)
    else:
        obj_db_DataBase = db_DataBase.objects.filter(id=dbId)
        if obj_db_DataBase.exists():
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    obj_db_DataBase.update(
                        is_del=1,
                        updateTime=cls_Common.get_date_time(),
                        uid_id=userId,
                    )
                    # region 添加操作信息
                    cls_Logging.record_operation_info(
                        'API', 'Manual', 3, 'Delete',
                        None, None, None,
                        userId,
                        '删除数据库环境', CUFront=json.dumps(request.POST)
                    )
                    # endregion
            except BaseException as e:  # 自动回滚，不需要任何操作
                response['errorMsg'] = f'数据删除失败:{e}'
            else:
                response['statusCode'] = 2003
        else:
            response['errorMsg'] = '未找到当前系统下的全局变量,请刷新后重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def get_connect_base_items(request):
    response = {}
    dataList = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        # sysType = objData.sysType
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'DataBaseEnvironment', 'select_data', errorMsg)
    else:
        obj_db_DataBase = db_DataBase.objects.filter(is_del=0).order_by('-updateTime')
        for i in obj_db_DataBase:
            children = []
            connectTest = cls_DataBase.connect_test(
                'MySql', i.dataBaseIp, i.port, i.userName, cls_DataSecurity.aes_decode(ast.literal_eval(i.passWord)))
            if connectTest['state']:
                dataBaseList = connectTest['dataBaseList']
            else:
                dataBaseList = []
            for item in dataBaseList:
                children.append({'label':item,'value':item})
            dataList.append({'label':i.dataBaseIp,'value':i.id,'children':children})

        response['statusCode'] = 2000
        response['dataList'] = dataList
    return JsonResponse(response)
