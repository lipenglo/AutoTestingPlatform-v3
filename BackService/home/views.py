from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.conf import settings
from django.db import transaction
from django.contrib.auth import hashers
from dwebsocket.decorators import accept_websocket
from time import sleep

import json
import operator

# Create your db here.
from django.db.models import Q
from login.models import UserTable as db_UserTable
from django.contrib.auth.models import User as db_DjUser
from routerPar.models import Router as db_Router
from login.models import UserBindRole as db_UserBindRole
from role.models import RoleBindMenu as db_RoleBindMenu
from info.models import OperateInfo as db_OperateInfo
from info.models import PushInfo as db_PushInfo
from Api_TestReport.models import ApiQueue as db_ApiQueue
from WorkorderManagement.models import WorkBindPushToUsers as db_WorkBindPushToUsers
from WorkorderManagement.models import WorkorderManagement as db_WorkorderManagement
from Api_CaseMaintenance.models import CaseBaseData as db_CaseBaseData
from Api_TimingTask.models import ApiTimingTask as db_ApiTimingTask
from Api_IntMaintenance.models import ApiBaseData as db_ApiBaseData

# Create reference here.
from ClassData.Logger import Logging
from ClassData.GlobalDecorator import GlobalDer
from ClassData.FindCommonTable import FindTable
from ClassData.Common import Common
from ClassData.ImageProcessing import ImageProcessing
from ClassData.ObjectMaker import object_maker
from ClassData.FindServer import FindLocalServer
from ClassData.ObjectMaker import object_maker as cls_object_maker

# Create info here.
cls_Logging = Logging()
cls_GlobalDer = GlobalDer()
cls_FindTable = FindTable()
cls_Common = Common()
cls_ImageProcessing = ImageProcessing()
cls_FindLocalServer = FindLocalServer()


# Create your views here.

@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])
def load_user_info(request):
    response = {}
    try:
        token = request.META['HTTP_TOKEN']
        userId = cls_FindTable.get_userId(token)
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'home', 'load_user_info', errorMsg)
    else:
        obj_db_UserTable = db_UserTable.objects.filter(id=userId)
        if obj_db_UserTable.exists():
            # region 处理userImg
            fileList = []
            if obj_db_UserTable[0].userImg:
                name = f"{cls_Common.generate_random_value()}.png"
                userImg = eval(obj_db_UserTable[0].userImg)
                base64_to_img = cls_ImageProcessing.base64_to_img(userImg, f"{settings.TEMP_PATH}/{name}")
                if base64_to_img['state']:
                    fileList.append({
                        'name': name,
                        'url': f"{settings.NGINX_SERVER}/Temp/{name}"
                    })
            # endregion
            baseInfo = {
                'userName': obj_db_UserTable[0].userName,
                'nickName': obj_db_UserTable[0].nickName,
                'userImg': str(eval(obj_db_UserTable[0].userImg),
                               encoding='utf-8') if obj_db_UserTable[0].userImg else None,
                'fileList': fileList,
                'emails': obj_db_UserTable[0].emails,
            }
            response['baseInfo'] = baseInfo
            response['statusCode'] = 2000
        else:
            response['errorMsg'] = '用户信息获取失败!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def save_user_info(request):
    response = {}
    try:
        responseData = json.loads(request.body)
        objData = object_maker(responseData)
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        nickName = objData.nickName
        emails = objData.emails
        password = objData.password
        fileList = objData.fileList
        # deleteFileList = cls_Common.conversion_post_lists('deleteFileList',request.POST)
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'home', 'save_user_info', errorMsg)
    else:
        obj_db_user = db_UserTable.objects.filter(id=userId)
        if obj_db_user.exists():
            obj_db_DjUser = db_DjUser.objects.get(id=obj_db_user[0].userId)
            if obj_db_DjUser.exists():
                try:
                    with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                        obj_db_DjUser.password = hashers.make_password(password=password)
                        obj_db_DjUser.save()
                        obj_db_user.update(nickName=nickName, emails=emails)

                        # region 处理上传的图片
                        if fileList:
                            name = fileList[0]['name']
                            # url = fileList[0]['url']
                            localhostPath = f"{settings.TEMP_PATH}/{name}"
                            get_file_md5 = cls_Common.get_file_md5(localhostPath)
                            if obj_db_user[0].imgMD5 != get_file_md5:
                                img_to_base64 = cls_ImageProcessing.img_to_base64(localhostPath)
                                obj_db_user.update(userImg=img_to_base64, imgMD5=get_file_md5)
                        else:
                            obj_db_user.update(userImg=None, imgMD5=None)
                        # endregion
                except Exception as e:  # 自动回滚，不需要任何操作
                    response['errorMsg'] = f'保存失败:{e}'
                else:
                    response['statusCode'] = 2002
            else:
                response['errorMsg'] = '内置用户信息缺失!'
        else:
            response['errorMsg'] = '未查询到该用户信息'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 获取HOME页面的菜单权限
def get_home_permissions(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'home', 'get_home_permissions', errorMsg)
    else:
        obj_db_Router = db_Router.objects.filter(is_del=0)
        obj_level_1_Menu = obj_db_Router.filter(level=1, sysType='Home').order_by('sortNum')  # 1级菜单
        obj_db_UserBindRole = db_UserBindRole.objects.filter(is_del=0, user_id=userId)
        menuTable = []
        if obj_db_UserBindRole.exists():
            roleId = obj_db_UserBindRole[0].role_id
            for item_level_1 in obj_level_1_Menu:
                children = []
                # 2级菜单
                obj_level_2_Menu = obj_db_Router.filter(
                    level=2, belogId=item_level_1.id, sysType='Home').order_by('index')
                for item_level_2 in obj_level_2_Menu:
                    obj_db_RoleBindMenu = db_RoleBindMenu.objects.filter(is_del=0, sysType='Home', role_id=roleId)
                    for item_bindMenu in obj_db_RoleBindMenu:
                        if item_bindMenu.router.id == item_level_2.id:
                            children.append({
                                'index': str(item_level_2.index),
                                'menuName': item_level_2.menuName
                            })
                menuTable.append({'index': str(item_level_1.sortNum),
                                  'level': item_level_1.level,
                                  'menuName': item_level_1.menuName,
                                  'disPlay': False if children or item_level_1.menuName == 'Home' else True,
                                  'icon': item_level_1.icon,
                                  'children': children})
        else:
            pass
        response['statusCode'] = 2000
        # response['menuDisPlqy'] = menuDisPlqy
        response['menuTable'] = menuTable
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 获取页面的菜单权限
def get_permissions(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        sysType = objData.sysType
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'home', 'get_api_permissions', errorMsg)
    else:
        obj_db_Router = db_Router.objects.filter(is_del=0)
        obj_level_1_Menu = obj_db_Router.filter(level=1, sysType=sysType).order_by('sortNum')  # 1级菜单
        obj_db_UserBindRole = db_UserBindRole.objects.filter(is_del=0, user_id=userId)
        menuTable = []
        if obj_db_UserBindRole.exists():
            roleId = obj_db_UserBindRole[0].role_id
            for item_level_1 in obj_level_1_Menu:
                children = []
                # 2级菜单
                obj_level_2_Menu = obj_db_Router.filter(
                    level=2, belogId=item_level_1.id, sysType=sysType).order_by('index')
                for item_level_2 in obj_level_2_Menu:
                    obj_db_RoleBindMenu = db_RoleBindMenu.objects.filter(is_del=0, sysType=sysType, role_id=roleId)
                    for item_bindMenu in obj_db_RoleBindMenu:
                        if item_bindMenu.router.id == item_level_2.id:
                            children.append({
                                'index': str(item_level_2.index),
                                'menuName': item_level_2.menuName,
                                'path': item_level_2.routerPath,
                            })
                menuTable.append({'index': str(item_level_1.sortNum),
                                  'level': item_level_1.level,
                                  'menuName': item_level_1.menuName,
                                  'disPlay': False if children or item_level_1.menuName == 'HOME' else True,
                                  'icon': item_level_1.icon,
                                  'children': children})
        else:
            pass
        response['statusCode'] = 2000
        # response['menuDisPlqy'] = menuDisPlqy
        response['menuTable'] = menuTable
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 返回路由地址
def get_router_path(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = object_maker(responseData)

        sysType = objData.sysType
        index = objData.index
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'home', 'get_router_path', errorMsg)
    else:
        obj_db_Router = db_Router.objects.filter(sysType=sysType, index=index, is_del=0)
        if obj_db_Router.exists():
            response['statusCode'] = 2000
            response['routerPath'] = obj_db_Router[0].routerPath
        else:
            response['errorMsg'] = '未查询到此菜单参数!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 用户统计数据,首页右下角弹出框
def get_user_statistics_info(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        roleId = cls_FindTable.get_roleId(userId)
        isAdmin = cls_FindTable.get_role_is_admin(roleId)
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'home', 'get_router_path', errorMsg)
    else:
        obj_db_UserBindRole = db_UserBindRole.objects.filter(user_id=userId, is_del=0)
        if obj_db_UserBindRole.exists():
            pushCount = db_PushInfo.objects.filter(~Q(oinfo__uid_id=userId), uid_id=userId, is_read=0).count()
            errorCount = db_OperateInfo.objects.filter(remindType='Error', is_read=0).count()
            warningCount = db_PushInfo.objects.filter(uid_id=userId, oinfo__remindType='Warning', is_read=0).count()
            obj_db_WorkorderManagement = db_WorkorderManagement.objects.filter(~Q(workState=3), is_del=0)
            unfinishedWorkOrder = 0  # 未完成的工作订单
            for i in obj_db_WorkorderManagement:
                obj_db_WorkBindPushToUsers = db_WorkBindPushToUsers.objects.filter(
                    is_del=0, work_id=i.id, uid_id=userId)
                if obj_db_WorkBindPushToUsers.exists():
                    unfinishedWorkOrder += 1

            if isAdmin:
                message = f"当前您的信息: <br>" \
                          f"错误信息({errorCount})," \
                          f"警告信息({warningCount})," \
                          f"推送信息({pushCount}),<br>" \
                          f"未完成工单信息({unfinishedWorkOrder}),<br>" \
                          f"请注意查收!"
            else:
                message = f"当前您的信息: <br>" \
                          f"警告信息({warningCount})," \
                          f"推送信息({pushCount}),<br>" \
                          f"未完成工单信息({unfinishedWorkOrder}),<br>" \
                          f"请注意查收!"
            response['statusCode'] = 2000
            response['message'] = message

    return JsonResponse(response)


@accept_websocket  # 获取服务器的性能,服务的状态,当前用户推送统计数量
def get_server_indicators(request):
    counter = 0  # 计数器 到10就会断开通信
    if request.is_websocket():
        retMessage = str(request.websocket.wait(), 'utf-8')  # 接受前段发送来的数据
        if retMessage:
            objData = object_maker(json.loads(retMessage))
            token = objData.Params.token
            if objData.Message == "Start":  # 开始执行
                while True:
                    sendText = {}
                    try:
                        retMessage = request.websocket.read()
                    except BaseException as e:
                        cls_Logging.print_log('info', 'get_server_indicators', f'前端已关闭,断开连接:{e}')
                        break
                    else:
                        userId = cls_FindTable.get_userId(token)
                        obj_db_PushInfo = db_PushInfo.objects.filter(uid_id=userId, is_read=0)
                        pushCount = obj_db_PushInfo.count()

                        sendText = {
                            'pushCount': pushCount,
                            'cpu': cls_FindLocalServer.get_cpu_state(),
                            'mem': cls_FindLocalServer.get_mem_state(),
                            'celery': cls_FindLocalServer.get_celery_state(),
                            'celeryBeat': cls_FindLocalServer.get_celery_beat_state(),
                        }

                        request.websocket.send(json.dumps(sendText, ensure_ascii=False).encode('utf-8'))
                        if retMessage:
                            objData = object_maker(json.loads(retMessage))
                            if objData.Message == 'Heartbeat':
                                counter = 0
                        else:
                            counter += 1
                            if counter >= 10:
                                request.websocket.close()
                                cls_Logging.print_log('error', 'get_server_indicators',
                                                      f'心跳包:{counter}秒内无响应,断开连接')
                                break
                        sleep(1)


@accept_websocket  # 当前页面的 测试结果总览,项目统计,过去7天内Top10,项目队列,数据返回
def api_page_get_main_data(request):
    counter = 0  # 计数器 到10就会断开通信
    if request.is_websocket():
        retMessage = str(request.websocket.wait(), 'utf-8')  # 接受前段发送来的数据
        if retMessage:
            objData = object_maker(json.loads(retMessage))

            proId = objData.Params.proId
            token = objData.Params.token
            userId = cls_FindTable.get_userId(token)
            if objData.Message == "Start":  # 开始执行
                while True:
                    try:
                        retMessage = request.websocket.read()
                    except BaseException as e:
                        cls_Logging.print_log('info', 'get_server_indicators', f'前端已关闭,断开连接:{e}')
                        break
                    else:
                        sendText = {
                            'testResults': cls_FindTable.get_overview_of_test_results(proId),  # 测试结果概述
                            # 项目下所有数据的统计
                            'pageStatistical': cls_FindTable.get_page_under_statistical_data(proId),
                            'proStatistical': cls_FindTable.get_pro_under_statistical_data('API', proId),
                            'pastSevenDaysTop': cls_FindTable.get_past_seven_days_top_ten_data(proId),  # 过去7天内Top10
                            'proQueue': cls_FindTable.get_pro_queue(proId),  # 获取项目队列
                            'myWork': cls_FindTable.get_my_work('API', proId, userId),
                        }

                        request.websocket.send(json.dumps(sendText, ensure_ascii=False).encode('utf-8'))
                        if retMessage:
                            objData = object_maker(json.loads(retMessage))
                            if objData.Message == 'Heartbeat':
                                counter = 0
                        else:
                            counter += 1
                            if counter >= 10:
                                request.websocket.close()
                                cls_Logging.print_log('error', 'api_page_main_data_refresh',
                                                      f'心跳包:{counter}秒内无响应,断开连接')
                                break
                        sleep(1)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 测试结果总览
def api_pagehome_select_test_results(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = object_maker(responseData)
        proId = objData.proId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'home', 'api_pagehome_select_test_results', errorMsg)
    else:
        overviewOfTestResults = cls_FindTable.get_overview_of_test_results(proId)
        if overviewOfTestResults:
            timeData = overviewOfTestResults['timeData']
            passData = overviewOfTestResults['passData']
            failData = overviewOfTestResults['failData']
            errorData = overviewOfTestResults['errorData']
        else:
            timeData = []
            passData = []
            failData = []
            errorData = []

        response['statusCode'] = 2000
        response['timeData'] = timeData
        response['passData'] = passData
        response['failData'] = failData
        response['errorData'] = errorData
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 页面下的所有数据总统计
def api_pagehome_select_page_statistical(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = object_maker(responseData)
        proId = objData.proId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'home', 'api_pagehome_select_pro_statistical', errorMsg)
    else:
        projectUnderStatisticalData = cls_FindTable.get_page_under_statistical_data(proId)
        dataTable = projectUnderStatisticalData['dataTable']
        response['dataTable'] = dataTable
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 项目下的所有数据总统计
def api_pagehome_select_pro_statistical(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = object_maker(responseData)
        proId = objData.proId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'home', 'api_pagehome_select_pro_statistical', errorMsg)
    else:
        projectUnderStatisticalData = cls_FindTable.get_pro_under_statistical_data('API', proId)
        dataTable = projectUnderStatisticalData['dataTable']
        response['dataTable'] = dataTable
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 过去7天内Top10
def api_pagehome_select_Formerly_data(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = object_maker(responseData)
        proId = objData.proId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'home', 'api_pagehome_select__Formerly_data', errorMsg)
    else:
        pastSevenDaysTopTenData = cls_FindTable.get_past_seven_days_top_ten_data(proId)
        response['dataTable'] = pastSevenDaysTopTenData['dataTable']
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 项目队列
def api_pagehome_select_pro_queue(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = object_maker(responseData)
        proId = objData.proId
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'home', 'api_pagehome_select_pro_queue', errorMsg)
    else:
        proQueue = cls_FindTable.get_pro_queue(proId)
        response['dataTable'] = proQueue['dataTable']
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # 修改队列状态
def api_pagehome_handle_state(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        queueId = request.POST['queueId']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'home', 'api_pagehome_handle_state', errorMsg)
    else:
        db_ApiQueue.objects.filter(id=queueId).update(
            queueStatus=2, updateTime=cls_Common.get_date_time(), uid_id=userId
        )
        response['statusCode'] = 2002
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 主页系统统计
def select_sys_total(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = object_maker(responseData)
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'home', 'select_sys_total', errorMsg)
    else:
        # 用户总数
        userTotal = db_UserTable.objects.filter(is_del=0, is_activation=1).count()
        # 会统计3个系统的数量
        # 用例总数
        caseTotal = db_CaseBaseData.objects.filter(is_del=0).count()

        # 任务总数
        taskTotal = db_ApiTimingTask.objects.filter(is_del=0).count()

        # 执行总数
        executeTotal = db_ApiQueue.objects.filter().count()

        response['statusCode'] = 2000
        response['userTotal'] = userTotal
        response['caseTotal'] = caseTotal
        response['taskTotal'] = taskTotal
        response['executeTotal'] = executeTotal
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # 主页用户Top5统计
def select_user_total(request):
    response = {}
    dataList = []
    tempStatistical = []  # 临时统计数据
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = object_maker(responseData)
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'home', 'select_user_total', errorMsg)
    else:
        obj_db_UserTable = db_UserTable.objects.filter(is_del=0, is_activation=1)
        for item_user in obj_db_UserTable:
            apiTotal = db_ApiBaseData.objects.filter(is_del=0, uid_id=item_user.id).count()
            elementTotal = 0
            caseTotal = db_CaseBaseData.objects.filter(is_del=0, uid_id=item_user.id).count()
            taskTotal = db_ApiTimingTask.objects.filter(is_del=0, uid_id=item_user.id).count()
            workOrderTotal = db_WorkorderManagement.objects.filter(is_del=0, uid_id=item_user.id).count()
            executeTotal = db_ApiQueue.objects.filter(uid_id=item_user.id).count()

            allTotal = apiTotal + elementTotal + caseTotal + taskTotal + executeTotal
            tempStatistical.append({
                'id': item_user.id,
                'userName': f"{item_user.userName}({item_user.nickName})",
                'apiAndElementTotal': f"{apiTotal}/{elementTotal}",
                'caseTotal': caseTotal,
                'taskTotal': taskTotal,
                'workOrderTotal': workOrderTotal,
                'executeTotal': executeTotal,
                'allTotal': allTotal,
            })
        sortList = sorted(tempStatistical, key=operator.itemgetter('allTotal'), reverse=True)  # 倒序排列
        for index, item in enumerate(sortList[:5], 1):
            if item['allTotal'] != 0:
                dataList.append({
                    'index': index,
                    'id': item['id'],
                    'userName': item['userName'],
                    'apiAndElementTotal': item['apiAndElementTotal'],
                    'caseTotal': item['caseTotal'],
                    'taskTotal': item['taskTotal'],
                    'workOrderTotal': item['workOrderTotal'],
                    'executeTotal': item['executeTotal'],
                })
        response['statusCode'] = 2000
        response['tableData'] = dataList
    return JsonResponse(response)
