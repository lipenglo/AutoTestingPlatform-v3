from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction

import json
import ast
import time

# Create your db here.
from login.models import UserTable as db_UserTable
from WorkorderManagement.models import WorkorderManagement as db_WorkorderManagement
from WorkorderManagement.models import WorkBindPushToUsers as db_WorkBindPushToUsers
from WorkorderManagement.models import WorkLifeCycle as db_WorkLifeCycle
from WorkorderManagement.models import HistoryInfo as db_HistoryInfo

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
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        myWork = objData.myWork
        sysType = objData.sysType
        proId = objData.proId
        pageId = objData.pageId
        funId = objData.funId

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'WorkorderManagement', 'select_data', errorMsg)
    else:
        obj_db_WorkorderManagement = db_WorkorderManagement.objects.filter(
            is_del=0, sysType=sysType, pid_id=proId).order_by('-updateTime')
        if pageId:
            obj_db_WorkorderManagement = obj_db_WorkorderManagement.filter(page_id=pageId)
        if funId:
            obj_db_WorkorderManagement = obj_db_WorkorderManagement.filter(fun_id=funId)
        select_db_WorkorderManagement = obj_db_WorkorderManagement[minSize: maxSize]
        for i in select_db_WorkorderManagement:
            timeArray = time.strptime(i.updateTime.strftime('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S")
            obj_db_HistoryInfo = db_HistoryInfo.objects.filter(work_id=i.id).order_by('-createTime')
            if obj_db_HistoryInfo.exists():
                message = obj_db_HistoryInfo[0].message
            else:
                message = ""
            # region 查询创建人
            obj_db_UserTable = db_UserTable.objects.filter(is_del=0, id=i.cuid)
            if obj_db_UserTable:
                createUserName = obj_db_UserTable[0].userName
                nickName = obj_db_UserTable[0].nickName
            else:
                createUserName = None
                nickName = None
            # endregion
            if myWork == "My":
                obj_db_WorkBindPushToUsers = db_WorkBindPushToUsers.objects.filter(is_del=0, uid_id=userId,work_id=i.id)
                # 创建人是自己 或 被关联人有自己
                bindUser = [item_bindUser.uid_id for item_bindUser in obj_db_WorkBindPushToUsers]
                if userId in bindUser or i.cuid == userId:
                    dataList.append(
                        {"id": i.id,
                         "workSource": i.workSource,
                         "workType": i.workType,
                         "pageNameAndfunName": f"{i.page.pageName}/{i.fun.funName}",
                         # "pageName": ,
                         # "funName": i.fun.funName,
                         "workName": i.workName,
                         "message": message,
                         "workState": i.workState,
                         "updateTime": str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                         "timeStamp": int(time.mktime(timeArray)),  # 用于排序使用,前端str类型的时间不可排序
                         "createUserName": f"{createUserName}({nickName})",
                         })
            else:
                dataList.append(
                    {"id": i.id,
                     "workSource": i.workSource,
                     "workType": i.workType,
                     "pageNameAndfunName": f"{i.page.pageName}/{i.fun.funName}",
                     # "pageName": i.page.pageName,
                     # "funName": i.fun.funName,
                     "workName": i.workName,
                     "message": message,
                     "workState": i.workState,
                     "updateTime": str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                     "timeStamp": int(time.mktime(timeArray)),  # 用于排序使用,前端str类型的时间不可排序
                     "createUserName": f"{createUserName}({nickName})",
                     })

        response['TableData'] = dataList
        response['Total'] = obj_db_WorkorderManagement.count()
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
        pageId = request.POST['pageId']
        funId = request.POST['funId']
        workType = request.POST['workType']
        workState = request.POST['workState']
        workName = request.POST['workName']
        message = request.POST['message']
        pushTo = ast.literal_eval(request.POST['pushTo']) if request.POST['pushTo'] else []
        pushToList = [i for index, i in enumerate(pushTo, 1) if index % 2 == 0]
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'WorkorderManagement', 'data_save', errorMsg)
    else:
        # obj_db_WorkorderManagement = db_WorkorderManagement.objects.filter(
        #     is_del=0, sysType=sysType, pid_id=proId, page_id=pageId, fun_id=funId,workSource=0, workName=workName)
        # if obj_db_WorkorderManagement.exists():
        #     response['errorMsg'] = "当前所属功能下已有相同工单名称,请更改!"
        # else:
        try:
            with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                # region 基本信息
                save_db_WorkorderManagement = db_WorkorderManagement.objects.create(
                    sysType=sysType,
                    pid_id=proId,
                    page_id=pageId,
                    fun_id=funId,
                    workSource=0,
                    workType=workType,
                    workState=workState,
                    workName=workName,
                    # message=message,
                    is_del=0,
                    uid_id=userId,
                    cuid=userId
                )
                # endregion
                # region 添加操作信息
                operationInfoId = cls_Logging.record_operation_info(
                    'API', 'Manual', 3, "Add",
                    cls_FindTable.get_pro_name(proId),
                    cls_FindTable.get_page_name(pageId),
                    cls_FindTable.get_fun_name(funId),
                    userId,
                    f'工单编号:【A-{save_db_WorkorderManagement.id}】 {workName}:{message}',
                    CUFront=json.dumps(request.POST)
                )
                # endregion
                # region 添加信息到历史信息
                db_HistoryInfo.objects.create(
                    work_id=save_db_WorkorderManagement.id,
                    message=message,
                    uid_id=userId,
                )
                # endregion
                # region 添加工单的生命周期
                db_WorkLifeCycle.objects.create(
                    work_id=save_db_WorkorderManagement.id,
                    operationType='Add',
                    workState=workState,
                    uid_id=userId,
                    is_del=0,
                )
                # endregion
                # region 如果有接收人,就保存
                if pushTo:
                    product_list_to_insert = list()
                    for i in pushToList:
                        if i != userId:#创建人不被推送信息
                            # 添加推送to数据
                            cls_Logging.push_to_user(operationInfoId, i)
                        product_list_to_insert.append(db_WorkBindPushToUsers(
                            work_id=save_db_WorkorderManagement.id,
                            uid_id=i,
                            is_del=0
                        ))
                    db_WorkBindPushToUsers.objects.bulk_create(product_list_to_insert)
                # endregion
        except BaseException as e:  # 自动回滚，不需要任何操作
            response['errorMsg'] = f'保存失败:{e}'
        else:
            response['statusCode'] = 2001
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def load_data(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        workId = objData.workId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'WorkorderManagement', 'load_edit_data', errorMsg)
    else:
        obj_db_WorkorderManagement = db_WorkorderManagement.objects.filter(is_del=0, id=workId)
        if obj_db_WorkorderManagement.exists():
            # cuid = obj_db_WorkorderManagement[0].cuid
            data = obj_db_WorkorderManagement[0]
            pushTo = []
            obj_db_WorkBindPushToUsers = db_WorkBindPushToUsers.objects.filter(is_del=0, work_id=data.id)
            for i in obj_db_WorkBindPushToUsers:
                roleId = cls_FindTable.get_roleId(i.uid_id)
                pushTo.append([roleId, i.uid.id])

            # # 在编辑时把创建人给加到推送TO中,省的反推时还要在添加
            # roleId = cls_FindTable.get_roleId(cuid)
            # if [roleId, cuid] not in pushTo:
            #     pushTo.append([roleId, cuid])
            # region 历史回复信息
            historyInfo = []
            obj_db_HistoryInfo = db_HistoryInfo.objects.filter(work_id=workId).order_by('-createTime')
            for item_hisInfo in obj_db_HistoryInfo:
                historyInfo.append({
                    'timestamp': str(item_hisInfo.createTime.strftime('%Y-%m-%d %H:%M:%S')),
                    'title': f'{item_hisInfo.uid.userName}({item_hisInfo.uid.nickName}):',
                    'content': item_hisInfo.message
                })
            # endregion
            dataTabel = {
                'workType': data.workType,
                'workState': data.workState,
                'pageId': data.page_id,
                'funId': data.fun_id,
                'workName': data.workName,
                'historyInfo': historyInfo,
                'pushTo': pushTo,
            }

            response['statusCode'] = 2000
            response['dataTabel'] = dataTabel
        else:
            response['errorMsg'] = "当前选择的工单不存在,请刷新后重新尝试!"
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def edit_data(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        workId = int(request.POST['workId'])
        sysType = request.POST['sysType']
        proId = request.POST['proId']
        pageId = request.POST['pageId']
        funId = request.POST['funId']
        workType = request.POST['workType']
        workState = int(request.POST['workState'])
        workName = request.POST['workName']
        workMessage = request.POST['message']
        pushTo = ast.literal_eval(request.POST['pushTo']) if request.POST['pushTo'] else []
        pushToList = [i for index, i in enumerate(pushTo, 1) if index % 2 == 0]
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'ProjectManagement', 'edit_data', errorMsg)
    else:
        obj_db_WorkorderManagement = db_WorkorderManagement.objects.filter(id=workId, is_del=0)
        if obj_db_WorkorderManagement.exists():
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    # region添加操作信息
                    oldData = list(obj_db_WorkorderManagement.values())
                    obj_db_HistoryInfo = db_HistoryInfo.objects.filter(work_id=workId).order_by('-createTime')
                    if obj_db_HistoryInfo.exists():
                        oldData[0]['message'] = obj_db_HistoryInfo[0].message
                    else:
                        oldData[0]['message'] = ""
                    newData = ast.literal_eval(json.dumps(request.POST))
                    # if workState != obj_db_WorkorderManagement[0].workState:
                        # 0: 待受理, 1: 受理中, 2: 已解决, 3: 已关闭
                    if workState == 0:
                        workStateName = '待受理'
                    elif workState == 1:
                        workStateName = '受理中'
                    elif workState == 2:
                        workStateName = '已解决'
                    else:
                        workStateName = '已关闭'
                    message = f'工单编号:【A-{workId}】【{workStateName}】:{workMessage}'
                        # message = f'工单编号:【A-{workId}】 修改状态:{workStateName}'
                    # else:
                    #     message = f'工单编号:【A-{workId}】 {workName}:{workMessage}'
                    operationInfoId = cls_Logging.record_operation_info(
                        'API', 'Manual', 3, 'Edit',
                        cls_FindTable.get_pro_name(proId),
                        cls_FindTable.get_page_name(pageId),
                        cls_FindTable.get_fun_name(funId),
                        userId,
                        # f'A-{workId}:{workName}',
                        message,
                        oldData, newData
                    )
                    # endregion
                    # region 基本信息
                    obj_db_WorkorderManagement.update(
                        sysType=sysType,
                        pid_id=proId,
                        page_id=pageId,
                        fun_id=funId,
                        workType=workType,
                        workState=workState,
                        workName=workName,
                        uid_id=userId,
                        updateTime=cls_Common.get_date_time()
                    )
                    # endregion
                    # region 添加信息到历史信息
                    obj_db_HistoryInfo = db_HistoryInfo.objects.filter(work_id=workId, message=workMessage)
                    if obj_db_HistoryInfo.exists():
                        pass
                    else:
                        db_HistoryInfo.objects.create(
                            work_id=workId,
                            message=workMessage,
                            uid_id=userId,
                        )
                    # endregion
                    # region 添加工单的生命周期
                    # region 把工单的修改差异显示出来
                    passKeyName = ['workId', 'pushTo', 'proId', 'pageId', 'funId']
                    conversionNew = [i for i in newData.keys() if i not in passKeyName]
                    newData['workState'] = int(newData['workState'])
                    diffList = [{'new': {i: newData[i]}, 'old': {i: oldData[0][i]}}
                                for i in conversionNew if oldData[0][i] != newData[i]]
                    keyNameDict = {
                        'workType': '工单类型',
                        'workState': '工单状态',
                        'workName': '工单名称',
                        'message': '工单信息',
                    }
                    strData = ""
                    for item in diffList:
                        newData = item['new']
                        oldData = item['old']
                        key = list(newData.keys())[0]
                        newValue = newData[key]
                        oldValue = oldData[key]

                        if key == "workState":
                            if oldValue == 0:
                                oldValue = '待受理'
                            elif oldValue == 1:
                                oldValue = '受理中'
                            elif oldValue == 2:
                                oldValue = '已解决'
                            else:
                                oldValue = '已关闭'
                        strData += f'<b>【{keyNameDict[key]}修改前】</b>:{oldValue}\n'

                        if key == "workState":
                            if newValue == 0:
                                newValue = '待受理'
                            elif newValue == 1:
                                newValue = '受理中'
                            elif newValue == 2:
                                newValue = '已解决'
                            else:
                                newValue = '已关闭'
                        strData += f'<b>【{keyNameDict[key]}修改为】</b>:{newValue}\n'
                        strData += '\n---------------------------------------------------------------------------------------\n'
                    # endregion
                    db_WorkLifeCycle.objects.create(
                        work_id=workId,
                        operationType='Edit',
                        workState=workState,
                        # operationInfo=newData,
                        operationInfo=strData,
                        uid_id=userId,
                        is_del=0,
                    )
                    # endregion
                    # region 如果有推送To信息,就保存
                    if pushTo:
                        db_WorkBindPushToUsers.objects.filter(is_del=0, work_id=workId).update(
                            is_del=1, updateTime=cls_Common.get_date_time())
                        product_list_to_insert = list()
                        for i in pushToList:
                            product_list_to_insert.append(db_WorkBindPushToUsers(
                                work_id=workId,
                                uid_id=i,
                                is_del=0
                            ))
                        db_WorkBindPushToUsers.objects.bulk_create(product_list_to_insert)

                        # 推送列表中加入 工单的创建人,但要先判断当前修改的人是不是创建人,如果是就不添加,如果不是才添加
                        # 修改者==创建者时,不发推送给修改者
                        if userId == obj_db_WorkorderManagement[0].cuid:
                            if userId in pushToList:
                                pushToList.remove(userId)
                        else:
                            if obj_db_WorkorderManagement[0].cuid not in pushToList:
                                pushToList.append(obj_db_WorkorderManagement[0].cuid)
                        # 如果修改者在推送列表中的时候 不推送修改者
                        if userId in pushToList:
                            pushToList.remove(userId)
                        for i in pushToList:
                            # 添加推送to数据
                            cls_Logging.push_to_user(operationInfoId, i)
                    # endregion
            except BaseException as e:  # 自动回滚，不需要任何操作
                response['errorMsg'] = f'工单修改失败:{e}'
            else:
                response['statusCode'] = 2002
        else:
            response['errorMsg'] = '未找到当前工单,请刷新后重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def delete_data(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        workId = request.POST['workId']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'WorkorderManagement', 'delete_data', errorMsg)
    else:
        obj_db_WorkorderManagement = db_WorkorderManagement.objects.filter(id=workId)
        if obj_db_WorkorderManagement.exists():
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    obj_db_WorkorderManagement.update(is_del=1, uid_id=userId, updateTime=cls_Common.get_date_time())
                    db_WorkBindPushToUsers.objects.filter(is_del=0, work_id=workId).update(
                        is_del=1, updateTime=cls_Common.get_date_time()
                    )
                    db_WorkLifeCycle.objects.filter(is_del=0, work_id=workId).update(
                        is_del=1, updateTime=cls_Common.get_date_time()
                    )
                    # region 添加操作信息
                    cls_Logging.record_operation_info(
                        'API', 'Manual', 3, 'Delete',
                        cls_FindTable.get_pro_name(obj_db_WorkorderManagement[0].pid_id),
                        cls_FindTable.get_page_name(obj_db_WorkorderManagement[0].page_id),
                        cls_FindTable.get_fun_name(obj_db_WorkorderManagement[0].fun_id),
                        userId,
                        obj_db_WorkorderManagement[0].workName, CUFront=json.dumps(request.POST)
                    )
                    # endregion
            except BaseException as e:  # 自动回滚，不需要任何操作
                response['errorMsg'] = f"当前工单删除失败:{e}"
            else:
                response['statusCode'] = 2003
        else:
            response['errorMsg'] = '未找到当前工单信息,请刷新后重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def select_life_cycle(request):  # 获取当前工单的生命周期
    response = {}
    dataList = []
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        workId = objData.workId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'WorkorderManagement', 'select_life_cycle', errorMsg)
    else:
        obj_db_WorkLifeCycle = db_WorkLifeCycle.objects.filter(work_id=workId).order_by('-updateTime')
        for i in obj_db_WorkLifeCycle:
            title = None
            content = ''
            operationType = i.operationType
            if i.workState == 0:
                workState = '待受理'
            elif i.workState == 1:
                workState = '受理中'
            elif i.workState == 2:
                workState = '已解决'
            else:
                workState = '已关闭'
            if operationType == "Add":
                title = f'创建工单【{workState}】 {i.uid.userName}({i.uid.nickName})'
            elif operationType == "Edit":
                title = f'修改工单【{workState}】 {i.uid.userName}({i.uid.nickName})'
                content = i.operationInfo
            dataList.append({
                'title': title,
                'content': content,
                'timestamp': str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
            })
        response['statusCode'] = 2000
        response['dataTabel'] = dataList
    return JsonResponse(response)
