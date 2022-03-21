from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction

import json
import ast

# Create your db here.
from login.models import UserTable as db_UserTable
from login.models import UserBindRole as db_UserBindRole
from ProjectManagement.models import ProManagement as db_ProManagement
from ProjectManagement.models import ProBindMembers as db_ProBindMembers
from PageManagement.models import PageManagement as db_PageManagement
from ProjectManagement.models import ProHistory as db_ProHistory
from Api_IntMaintenance.models import ApiBaseData as db_ApiBaseData
from Api_CaseMaintenance.models import CaseBaseData as db_ApiCaseBaseData
from Api_TimingTask.models import ApiTimingTask as db_ApiTimingTask
from Api_BatchTask.models import ApiBatchTask as db_ApiBatchTask

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
    sysType = None
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        sysType = objData.sysType
        proName = objData.proName

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info(sysType, 'ProjectManagement', 'select_data', errorMsg)
    else:
        obj_db_ProManagement = db_ProManagement.objects.filter(is_del=0, sysType=sysType).order_by('-updateTime')
        if proName:
            obj_db_ProManagement = obj_db_ProManagement.filter(proName__icontains=proName)
        select_db_ProManagement = obj_db_ProManagement[minSize: maxSize]
        for i in select_db_ProManagement:
            bindMembers = []
            tableItem = []  # 详情
            # region 查询创建人
            obj_db_UserTable = db_UserTable.objects.filter(is_del=0, id=i.cuid)
            if obj_db_UserTable:
                createUserName = obj_db_UserTable[0].userName
            else:
                createUserName = None
            # endregion
            # region 查询进入，修改，删除，的权限
            if userId == i.cuid:
                isMembers = False
                isEdit = False
                isDelete = False
            else:
                # region 查询当前查询的用户是不是管理员
                obj_db_UserBindRole = db_UserBindRole.objects.filter(user_id=userId)
                if obj_db_UserBindRole:
                    if obj_db_UserBindRole[0].role.is_admin == 1:
                        isMembers = False
                        isEdit = False
                        isDelete = False
                    else:
                        isMembers = True
                        isEdit = True
                        isDelete = True
                else:
                    isMembers = True
                    isEdit = True
                    isDelete = True
                # endregion
            # region 查询当前用户是否有进入权限
            obj_db_ProBindMembers = db_ProBindMembers.objects.filter(is_del=0, pid_id=i.id, uid_id=userId)
            if obj_db_ProBindMembers:
                isEnterInto = False
            else:
                isEnterInto = True
                # endregion
            # endregion
            # region 查询当前项目关联的人员
            obj_db_ProBindMembers = db_ProBindMembers.objects.filter(is_del=0, pid_id=i.id)
            for item in obj_db_ProBindMembers:
                bindMembers.append({'id': item.uid.id, 'name': item.uid.nickName})  # 载入关联的成员
            # endregion
            # endregion
            # region 详情
            performWeekTotal = 0
            perforHistoryTotal = 0
            tableItem.append({
                "createUserName": createUserName,
                "bindMembers": bindMembers,
                "createTime": str(i.createTime.strftime('%Y-%m-%d %H:%M:%S')),
            })
            # endregion
            dataDict = {
                "id": i.id,
                "proName": i.proName,
                "remarks": i.remarks,
                "updateTime": str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                "userName": f"{i.uid.userName}({i.uid.nickName})",
                "isEnterInto": isEnterInto,
                "isMembers": isMembers,
                "isEdit": isEdit,
                "isDelete": isDelete,
                "tableItem": tableItem,
            }
            if sysType == "API":
                projectUnderStatisticalData = cls_FindTable.get_pro_under_statistical_data(sysType, i.id)
                for item in projectUnderStatisticalData['dataTable']:
                    performWeekTotal += item['performWeekTotal']
                    perforHistoryTotal += item['perforHistoryTotal']
                unitCase = db_ApiCaseBaseData.objects.filter(is_del=0, pid_id=i.id, testType='UnitTest').count()
                HybridCase = db_ApiCaseBaseData.objects.filter(is_del=0, pid_id=i.id, testType='HybridTest').count()
                dataDict["apiTotal"] = db_ApiBaseData.objects.filter(is_del=0, pid_id=i.id).count()
                dataDict["caseTotal"] = f"{unitCase}/{HybridCase}"
                dataDict["taskTotal"] = db_ApiTimingTask.objects.filter(is_del=0, pid_id=i.id).count()
                dataDict["batchTotal"] = db_ApiBatchTask.objects.filter(is_del=0, pid_id=i.id).count()
                dataDict["performWeekTotal"] = performWeekTotal
                dataDict["perforHistoryTotal"] = perforHistoryTotal

            dataList.append(dataDict)

        response['TableData'] = dataList
        response['Total'] = obj_db_ProManagement.count()
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def save_data(request):
    response = {}
    sysType = None
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        roleId = cls_FindTable.get_roleId(userId)
        sysType = request.POST['sysType']
        proName = request.POST['proName']
        remarks = request.POST['remarks']
        onlyCode = cls_Common.generate_only_code()
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info(sysType, 'ProjectManagement', 'data_save', errorMsg)
    else:
        if roleId:
            obj_db_ProManagement = db_ProManagement.objects.filter(is_del=0, sysType=sysType, proName=proName)
            if obj_db_ProManagement.exists():
                response['errorMsg'] = "已有相同的所属项目存在,请更改!"
            else:
                try:
                    with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                        # region 基本信息创建
                        save_db_ProManagement = db_ProManagement.objects.create(
                            sysType=sysType,
                            proName=proName,
                            remarks=remarks,
                            is_del=0,
                            uid_id=userId,
                            cuid=userId,
                            onlyCode=onlyCode,
                        )
                        # endregion
                        # region 绑定默认创建人到项目成员中
                        db_ProBindMembers.objects.create(
                            pid_id=save_db_ProManagement.id,
                            role_id=roleId,
                            uid_id=userId,
                            is_del=0
                        )
                        # endregion
                        # region 添加操作信息
                        cls_Logging.record_operation_info(
                            sysType, 'Manual', 3, 'Add',
                            proName, None, None,
                            userId,
                            '新增项目', CUFront=json.dumps(request.POST)
                        )
                        # endregion
                        # region 添加历史恢复
                        restoreData = json.loads(json.dumps(request.POST))
                        restoreData['updateTime'] = save_db_ProManagement.updateTime.strftime('%Y-%m-%d %H:%M:%S')
                        restoreData['createTime'] = save_db_ProManagement.createTime.strftime('%Y-%m-%d %H:%M:%S')
                        restoreData['uid_id'] = save_db_ProManagement.uid_id
                        restoreData['cuid'] = save_db_ProManagement.cuid
                        restoreData['onlyCode'] = onlyCode

                        db_ProHistory.objects.create(
                            pid_id=save_db_ProManagement.id,
                            proName=proName,
                            onlyCode=onlyCode,
                            operationType='Add',
                            restoreData=restoreData,
                            uid_id=userId,
                        )
                        # endregion
                except BaseException as e:  # 自动回滚，不需要任何操作
                    response['errorMsg'] = f'保存失败:{e}'
                else:
                    response['statusCode'] = 2001
                    response['proId'] = save_db_ProManagement.id
                    response['proName'] = proName
        else:
            response['errorMsg'] = "当前用户无角色,请联系管理员"
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def edit_data(request):
    response = {}
    is_edit = False
    sysType = None
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        roleId = cls_FindTable.get_roleId(userId)
        is_admin = cls_FindTable.get_role_is_admin(roleId)
        sysType = request.POST['sysType']
        proId = int(request.POST['proId'])
        proName = request.POST['proName']
        remarks = request.POST['remarks']
        onlyCode = cls_Common.generate_only_code()
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info(sysType, 'ProjectManagement', 'edit_data', errorMsg)
    else:
        obj_db_ProManagement = db_ProManagement.objects.filter(id=proId, is_del=0)
        oldData = list(obj_db_ProManagement.values())
        newData = json.dumps(request.POST)
        if obj_db_ProManagement.exists():
            # 查询当前修改的用户是不是创建者
            if userId == obj_db_ProManagement[0].cuid:
                is_edit = True
            else:
                # 查询当前修改的用户是不是管理员成功
                obj_db_UserBindRole = db_UserBindRole.objects.filter(user_id=userId)
                if obj_db_UserBindRole.exists():
                    if is_admin:
                        is_edit = True
                    else:
                        response['errorMsg'] = '您当前没有权限对此进行操作,只有创建者或超管组才有此操作权限!'
                else:
                    response['errorMsg'] = '当前用户未绑定角色组!'
            if is_edit:
                select_db_ProManagement = db_ProManagement.objects.filter(sysType=sysType, proName=proName, is_del=0)
                if select_db_ProManagement.exists():
                    if proId == select_db_ProManagement[0].id:  # 自己修改自己
                        try:
                            with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                                db_ProManagement.objects.filter(is_del=0, id=proId).update(
                                    sysType=sysType,
                                    proName=proName,
                                    uid_id=userId,
                                    remarks=remarks,
                                    updateTime=cls_Common.get_date_time(),
                                    onlyCode=onlyCode)
                                # region 添加操作信息
                                cls_Logging.record_operation_info(
                                    sysType, 'Manual', 3, 'Edit',
                                    proName, None, None,
                                    userId,
                                    "修改项目",
                                    oldData, newData
                                )
                                # endregion
                                # region 添加历史恢复
                                restoreData = json.loads(json.dumps(request.POST))
                                restoreData['updateTime'] = obj_db_ProManagement[0].updateTime.strftime(
                                    '%Y-%m-%d %H:%M:%S')
                                restoreData['createTime'] = obj_db_ProManagement[0].createTime.strftime(
                                    '%Y-%m-%d %H:%M:%S')
                                restoreData['uid_id'] = obj_db_ProManagement[0].uid_id
                                restoreData['cuid'] = obj_db_ProManagement[0].cuid
                                restoreData['onlyCode'] = onlyCode
                                db_ProHistory.objects.create(
                                    pid_id=proId,
                                    proName=proName,
                                    onlyCode=onlyCode,
                                    operationType='Edit',
                                    restoreData=restoreData
                                )
                                # endregion
                        except BaseException as e:  # 自动回滚，不需要任何操作
                            response['errorMsg'] = f'更新数据失败:{e}'
                        else:
                            response['statusCode'] = 2002
                    else:
                        response['errorMsg'] = '已有重复所属项目名称,请更改!'
                else:
                    try:
                        with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                            # region 添加操作信息
                            cls_Logging.record_operation_info(
                                'API', 'Manual', 3, 'Edit',
                                proName, None, None,
                                userId,
                                None,
                                oldData, newData
                            )
                            # endregion
                            db_ProManagement.objects.filter(is_del=0, id=proId).update(
                                sysType=sysType,
                                proName=proName,
                                uid_id=userId,
                                remarks=remarks,
                                updateTime=cls_Common.get_date_time(),
                                onlyCode=onlyCode)
                            # region 添加历史恢复
                            restoreData = json.loads(json.dumps(request.POST))
                            restoreData['updateTime'] = obj_db_ProManagement[0].updateTime.strftime(
                                '%Y-%m-%d %H:%M:%S')
                            restoreData['createTime'] = obj_db_ProManagement[0].createTime.strftime(
                                '%Y-%m-%d %H:%M:%S')
                            restoreData['uid_id'] = obj_db_ProManagement[0].uid_id
                            restoreData['cuid'] = obj_db_ProManagement[0].cuid
                            restoreData['onlyCode'] = onlyCode
                            db_ProHistory.objects.create(
                                pid_id=proId,
                                proName=proName,
                                onlyCode=onlyCode,
                                operationType='Edit',
                                restoreData=restoreData,
                                uid_id=userId,
                            )
                            # endregion
                    except BaseException as e:  # 自动回滚，不需要任何操作
                        response['errorMsg'] = f'更新数据失败:{e}'
                    else:
                        response['statusCode'] = 2002
        else:
            response['errorMsg'] = '未找到当前项目,请刷新后重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def delete_data(request):
    response = {}
    is_edit = False
    sysType = None
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        sysType = request.POST['sysType']
        proId = request.POST['proId']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info(sysType, 'ProjectManagement', 'delete_data', errorMsg)
    else:
        obj_db_ProManagement = db_ProManagement.objects.filter(id=proId)
        if obj_db_ProManagement.exists():
            obj_db_PageManagement = db_PageManagement.objects.filter(is_del=0, pid_id=proId)
            if obj_db_PageManagement.exists():
                response['errorMsg'] = '当前项目下有所属页面数据,请删除下级所属页面后在重新尝试删除!'
            else:
                # 查询当前修改的用户是不是创建者
                if userId == obj_db_ProManagement[0].cuid:
                    is_edit = True
                else:
                    # 查询当前修改的用户是不是管理员成功
                    obj_db_UserBindRole = db_UserBindRole.objects.filter(user_id=userId)
                    if obj_db_UserBindRole.exists():
                        if obj_db_UserBindRole[0].role.is_admin == 1:
                            is_edit = True
                        else:
                            response['errorMsg'] = '您当前没有权限对此进行操作,只有创建者或超管组才有此操作权限!'
                    else:
                        response['errorMsg'] = '当前用户未绑定角色组!'
                if is_edit:
                    try:
                        with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                            # region 删除基础信息
                            obj_db_ProManagement.update(
                                is_del=1, uid_id=userId, updateTime=cls_Common.get_date_time()
                            )
                            # endregion
                            # region 删除人员绑定表
                            db_ProBindMembers.objects.filter(pid_id=proId, is_del=0).update(
                                is_del=1, updateTime=cls_Common.get_date_time()
                            )
                            # endregion
                            # region 添加操作信息
                            cls_Logging.record_operation_info(
                                sysType, 'Manual', 3, 'Delete',
                                obj_db_ProManagement[0].proName, None, None,
                                userId,
                                '删除项目', CUFront=json.dumps(request.POST)
                            )
                            # endregion
                            # region 添加历史恢复
                            db_ProHistory.objects.create(
                                pid_id=proId,
                                proName=obj_db_ProManagement[0].proName,
                                onlyCode=cls_Common.generate_only_code(),
                                operationType='Delete',
                                uid_id=userId,
                            )
                            # endregion
                    except BaseException as e:  # 自动回滚，不需要任何操作
                        response['errorMsg'] = f'删除失败:{e}'
                    else:
                        response['statusCode'] = 2003
        else:
            response['errorMsg'] = '未找到当前项目,请刷新后重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 查询已加入项目的成员
def select_join_data(request):
    response = {}
    dataList = []
    sysType = None
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        proId = objData.proId
        roleId = objData.roleId
        userName = objData.userName
        sysType = objData.sysType
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info(sysType, 'ProjectManagement', 'select_join_data', errorMsg)
    else:
        obj_db_ProBindMembers = db_ProBindMembers.objects.filter(is_del=0, pid_id=proId)
        if roleId:
            obj_db_ProBindMembers = obj_db_ProBindMembers.filter(role_id=roleId)
        if userName:
            obj_db_ProBindMembers = obj_db_ProBindMembers.filter(uid__userName__icontains=userName)
        for i in obj_db_ProBindMembers:
            dataList.append({
                'id': i.uid.id,
                'roleName': i.role.roleName,
                'userName': i.uid.userName,
                'nickName': i.uid.nickName,
                'isLock': False if i.uid.is_lock == 0 else True,
            })

        response['TableData'] = dataList
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 查询未加入项目的成员
def select_not_in_join_data(request):
    response = {}
    dataList = []
    sysType = None
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        proId = objData.proId
        roleId = objData.roleId
        userName = objData.userName
        sysType = objData.sysType
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info(sysType, 'ProjectManagement', 'select_not_in_join_data', errorMsg)
    else:
        obj_db_ProBindMembers = db_ProBindMembers.objects.filter(is_del=0, pid_id=proId)
        hasJoinedMembers = [i.uid.id for i in obj_db_ProBindMembers]

        obj_db_UserBindRole = db_UserBindRole.objects.filter(is_del=0)
        if roleId:
            obj_db_UserBindRole = obj_db_UserBindRole.filter(role_id=roleId)
        if userName:
            obj_db_UserBindRole = obj_db_UserBindRole.filter(user__userName__icontains=userName)
        for i in obj_db_UserBindRole:
            if i.user_id not in hasJoinedMembers:
                dataList.append({
                    'id': i.user.id,
                    'roleName': i.role.roleName,
                    'userName': i.user.userName,
                    'nickName': i.user.nickName,
                    'isLock': False if i.user.is_lock == 0 else True,
                })

        response['TableData'] = dataList
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 加入成员
def join_members(request):
    response = {}
    sysType = None
    try:
        sysType = request.POST['sysType']
        proId = request.POST['proId']
        joinUserId = request.POST['userId']  # 需要加入项目的用户
        roleId = cls_FindTable.get_roleId(joinUserId)
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info(sysType, 'ProjectManagement', 'join_members', errorMsg)
    else:
        if roleId:
            db_ProBindMembers.objects.create(
                pid_id=proId,
                role_id=roleId,
                uid_id=joinUserId,
                is_del=0,
            )
            response['statusCode'] = 2002
        else:
            response['errorMsg'] = "当前选择的用户未加入到角色中,请联系管理员!"
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 删除成员
def delete_members(request):
    response = {}
    sysType = None
    try:
        sysType = request.POST['sysType']
        proId = request.POST['proId']
        userId = request.POST['userId']  # 需要加入项目的用户
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info(sysType, 'ProjectManagement', 'delete_members', errorMsg)
    else:
        obj_db_ProBindMembers = db_ProBindMembers.objects.filter(is_del=0, pid_id=proId, uid_id=userId)
        if obj_db_ProBindMembers.exists():
            obj_db_ProBindMembers.update(
                updateTime=cls_Common.get_date_time(),
                is_del=1
            )
            response['statusCode'] = 2003
        else:
            response['errorMsg'] = "当前选择成员不存在于此项目中,请刷新后重新尝试!"
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 验证用户是否有进入此项目的权限
def verify_enter_into(request):
    response = {}
    sysType = None
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        proId = objData.proId
        sysType = objData.sysType
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info(sysType, 'ProjectManagement', 'verify_enter_into', errorMsg)
    else:
        obj_db_ProBindMembers = db_ProBindMembers.objects.filter(is_del=0, uid_id=userId, pid_id=proId)
        if obj_db_ProBindMembers.exists():
            response['statusCode'] = 2000
        else:
            response['errorMsg'] = "当前用户不在此项目的成员列表中,不可进入!"
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 查询历史恢复
def select_history(request):
    response = {}
    dataList = []
    sysType = None
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        sysType = objData.sysType
        proId = objData.proId
        proName = objData.proName
        operationType = objData.operationType

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info(sysType, 'ProjectManagement', 'select_history', errorMsg)
    else:
        if proId:
            obj_db_ProHistory = db_ProHistory.objects.filter(pid_id=proId, pid__sysType=sysType).order_by('-createTime')
        else:
            obj_db_ProHistory = db_ProHistory.objects.filter(pid__sysType=sysType).order_by('-createTime')
            if proName:
                obj_db_ProHistory = obj_db_ProHistory.filter(proName__icontains=proName).order_by('-createTime')
            if operationType:
                obj_db_ProHistory = obj_db_ProHistory.filter(operationType=operationType).order_by('-createTime')
        select_db_ProHistory = obj_db_ProHistory[minSize: maxSize]
        for i in select_db_ProHistory:
            if i.restoreData:
                restoreData = json.dumps(ast.literal_eval(i.restoreData),
                                         sort_keys=True, indent=4, separators=(",", ": "), ensure_ascii=False)
            else:
                restoreData = None
            if restoreData:
                tableItem = [{'restoreData': restoreData}]
            else:
                tableItem = []
            dataList.append({
                'id': i.id,
                'proName': i.proName,
                'operationType': i.operationType,
                'tableItem': tableItem,
                'createTime': str(i.createTime.strftime('%Y-%m-%d %H:%M:%S')),
                "userName": f"{i.uid.userName}({i.uid.nickName})",
            })
        response['TableData'] = dataList
        response['Total'] = obj_db_ProHistory.count()
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 恢复数据 只有管理员组或是项目创建人才可以恢复
def restor_data(request):
    response = {}
    sysType = None
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        roleId = cls_FindTable.get_roleId(userId)
        is_admin = cls_FindTable.get_role_is_admin(roleId)
        historyId = int(request.POST['historyId'])
        sysType = request.POST['sysType']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info(sysType, 'ProjectManagement', 'restor_data', errorMsg)
    else:
        obj_db_ProHistory = db_ProHistory.objects.filter(id=historyId)
        if obj_db_ProHistory.exists():
            # 恢复时是管理员或是 当前项目的创建人时才可恢复
            if is_admin or obj_db_ProHistory[0].pid.cuid == userId:
                try:
                    with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                        restoreData = obj_db_ProHistory[0].restoreData
                        if obj_db_ProHistory[0].operationType in ["Add","Edit"]:
                            obj_db_ProManagement = db_ProManagement.objects.filter(id=obj_db_ProHistory[0].pid_id)
                            if obj_db_ProManagement.exists():
                                # region 操作记录
                                cls_Logging.record_operation_info(
                                    'API', 'Manual', 3, 'Update',
                                    cls_FindTable.get_pro_name(obj_db_ProHistory[0].pid_id),
                                    None, None,
                                    userId,
                                    f'【恢复所属项目】 '
                                    f'ID:{obj_db_ProHistory[0].pid_id}:'
                                    f"{obj_db_ProHistory[0].proName}",
                                )
                                # endregion
                                restoreData = ast.literal_eval(restoreData)
                                obj_db_ProManagement.update(
                                    proName=restoreData['proName'],
                                    remarks=restoreData['remarks'],
                                    updateTime=restoreData['updateTime'],
                                    createTime=restoreData['createTime'],
                                    uid_id=restoreData['uid_id'],
                                    cuid=restoreData['cuid'],
                                    is_del=0,
                                    onlyCode=restoreData['onlyCode'],
                                )
                            else:
                                raise ValueError('此数据原始数据在库中无法查询到!')
                        else:
                            raise ValueError('使用了未录入的操作类型!')
                except BaseException as e:  # 自动回滚，不需要任何操作
                    response['errorMsg'] = f"数据恢复失败:{e}"
                else:
                    response['statusCode'] = 2002
            else:
                response['errorMsg'] = "您没有权限进行此操作,请联系项目的创建者或是管理员!"
        else:
            response['errorMsg'] = "当前选择的恢复数据不存在,请刷新后重新尝试!"
    return JsonResponse(response)
