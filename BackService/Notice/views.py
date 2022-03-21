from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction

import json
import ast

# Create your db here.
from Notice.models import NoticeInfo as db_NoticeInfo

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

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Notice', 'select_data', errorMsg)
    else:
        obj_db_NoticeInfo = db_NoticeInfo.objects.filter(is_del=0).order_by('-updateTime').order_by('-state')
        select_db_NoticeInfo = obj_db_NoticeInfo[minSize: maxSize]

        for i in select_db_NoticeInfo:
            dataList.append(
                {"id": i.id,
                 "abstract": i.abstract,
                 "info": i.info,
                 "state": True if i.state == 1 else False,
                 "updateTime": str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                 "userName": f"{i.uid.userName}({i.uid.nickName})",
                 }
            )

        response['TableData'] = dataList
        response['Total'] = obj_db_NoticeInfo.count()
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def save_data(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        abstract = request.POST['abstract']
        info = request.POST['info']
        state = request.POST['state']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Notice', 'save_data', errorMsg)
    else:
        obj_db_NoticeInfo = db_NoticeInfo.objects.filter(is_del=0, abstract=abstract)
        if obj_db_NoticeInfo.exists():
            response['errorMsg'] = "当前已有相同的简介名称,请更改!"
        else:
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    if state:  # 如果当前保存的公告为展示状态的话，其他所有公告必须被更新为不展示
                        db_NoticeInfo.objects.filter(is_del=0, state=1).update(state=0)
                    db_NoticeInfo.objects.create(
                        abstract=abstract,
                        info=info,
                        state=1 if state else 0,
                        uid_id=userId,
                        cuid=userId,
                        is_del=0,
                    )
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
        noticeId = int(request.POST['noticeId'])
        abstract = request.POST['abstract']
        info = request.POST['info']
        state = True if request.POST['state'] == 'true' else False
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Notice', 'edit_data', errorMsg)
    else:
        obj_db_NoticeInfo = db_NoticeInfo.objects.filter(id=noticeId, is_del=0)
        if obj_db_NoticeInfo.exists():
            select_db_NoticeInfo = db_NoticeInfo.objects.filter(abstract=abstract, is_del=0)
            if select_db_NoticeInfo.exists():
                if noticeId == select_db_NoticeInfo[0].id:  # 自己修改自己
                    is_Edit = True
                else:
                    response['errorMsg'] = '当前已有相同的简介名称,请更改!'
            else:
                is_Edit = True
            if is_Edit:
                try:
                    with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                        if state:  # 如果当前保存的公告为展示状态的话，其他所有公告必须被更新为不展示
                            db_NoticeInfo.objects.filter(is_del=0, state=1).update(state=0)
                        obj_db_NoticeInfo.update(
                            abstract=abstract,
                            info=info,
                            state=state,
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
        noticeId = request.POST['noticeId']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Notice', 'delete_data', errorMsg)
    else:
        obj_db_NoticeInfo = db_NoticeInfo.objects.filter(id=noticeId)
        if obj_db_NoticeInfo.exists():
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    obj_db_NoticeInfo.update(
                        is_del=1,
                        state=0,
                        updateTime=cls_Common.get_date_time(),
                        uid_id=userId,
                    )
            except BaseException as e:  # 自动回滚，不需要任何操作
                response['errorMsg'] = f'数据删除失败:{e}'
            else:
                response['statusCode'] = 2003
        else:
            response['errorMsg'] = '未找到当前公告,请刷新后重新尝试!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 展示最新的公告
def select_new_notice(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Notice', 'select_new_notice', errorMsg)
    else:
        obj_db_NoticeInfo = db_NoticeInfo.objects.filter(is_del=0, state=1)
        if obj_db_NoticeInfo.exists():
            noticeTime = str(obj_db_NoticeInfo[0].updateTime.strftime('%Y-%m-%d %H:%M:%S'))
            notice = obj_db_NoticeInfo[0].info
        else:
            noticeTime = None
            notice = None

        response['noticeTime'] = noticeTime
        response['notice'] = notice
        response['statusCode'] = 2000
    return JsonResponse(response)
