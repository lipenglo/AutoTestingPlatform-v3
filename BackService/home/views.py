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
        errorMsg = f"????????????:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'home', 'load_user_info', errorMsg)
    else:
        obj_db_UserTable = db_UserTable.objects.filter(id=userId)
        if obj_db_UserTable.exists():
            # region ??????userImg
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
            response['errorMsg'] = '????????????????????????!'
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
        errorMsg = f"????????????:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'home', 'save_user_info', errorMsg)
    else:
        obj_db_user = db_UserTable.objects.filter(id=userId)
        if obj_db_user.exists():
            obj_db_DjUser = db_DjUser.objects.get(id=obj_db_user[0].userId)
            if obj_db_DjUser:
                try:
                    with transaction.atomic():  # ???????????????????????????python???????????????????????????
                        obj_db_DjUser.password = hashers.make_password(password=password)
                        obj_db_DjUser.save()
                        obj_db_user.update(nickName=nickName, emails=emails)

                        # region ?????????????????????
                        if fileList:
                            name = fileList[0].name
                            localhostPath = f"{settings.TEMP_PATH}/{name}"
                            get_file_md5 = cls_Common.get_file_md5(localhostPath)
                            if obj_db_user[0].imgMD5 != get_file_md5:
                                img_to_base64 = cls_ImageProcessing.img_to_base64(localhostPath)
                                obj_db_user.update(userImg=img_to_base64, imgMD5=get_file_md5)
                        else:
                            obj_db_user.update(userImg=None, imgMD5=None)
                        # endregion
                except Exception as e:  # ????????????????????????????????????
                    response['errorMsg'] = f'????????????:{e}'
                else:
                    response['statusCode'] = 2002
            else:
                response['errorMsg'] = '????????????????????????!'
        else:
            response['errorMsg'] = '???????????????????????????'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # ??????HOME?????????????????????
def get_home_permissions(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
    except BaseException as e:
        errorMsg = f"????????????:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'home', 'get_home_permissions', errorMsg)
    else:
        obj_db_Router = db_Router.objects.filter(is_del=0)
        obj_level_1_Menu = obj_db_Router.filter(level=1, sysType='Home').order_by('sortNum')  # 1?????????
        obj_db_UserBindRole = db_UserBindRole.objects.filter(is_del=0, user_id=userId)
        menuTable = []
        if obj_db_UserBindRole.exists():
            roleId = obj_db_UserBindRole[0].role_id
            for item_level_1 in obj_level_1_Menu:
                children = []
                # 2?????????
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
@require_http_methods(["GET"])  # ???????????????????????????
def get_permissions(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = cls_object_maker(responseData)
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        sysType = objData.sysType
    except BaseException as e:
        errorMsg = f"????????????:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'home', 'get_api_permissions', errorMsg)
    else:
        obj_db_Router = db_Router.objects.filter(is_del=0)
        obj_level_1_Menu = obj_db_Router.filter(level=1, sysType=sysType).order_by('sortNum')  # 1?????????
        obj_db_UserBindRole = db_UserBindRole.objects.filter(is_del=0, user_id=userId)
        menuTable = []
        if obj_db_UserBindRole.exists():
            roleId = obj_db_UserBindRole[0].role_id
            for item_level_1 in obj_level_1_Menu:
                children = []
                # 2?????????
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
@require_http_methods(["GET"])  # ??????????????????
def get_router_path(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = object_maker(responseData)

        sysType = objData.sysType
        index = objData.index
    except BaseException as e:
        errorMsg = f"????????????:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'home', 'get_router_path', errorMsg)
    else:
        obj_db_Router = db_Router.objects.filter(sysType=sysType, index=index, is_del=0)
        if obj_db_Router.exists():
            response['statusCode'] = 2000
            response['routerPath'] = obj_db_Router[0].routerPath
        else:
            response['errorMsg'] = '???????????????????????????!'
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # ??????????????????,????????????????????????
def get_user_statistics_info(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        roleId = cls_FindTable.get_roleId(userId)
        isAdmin = cls_FindTable.get_role_is_admin(roleId)
    except BaseException as e:
        errorMsg = f"????????????:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'home', 'get_router_path', errorMsg)
    else:
        obj_db_UserBindRole = db_UserBindRole.objects.filter(user_id=userId, is_del=0)
        if obj_db_UserBindRole.exists():
            pushCount = db_PushInfo.objects.filter(~Q(oinfo__uid_id=userId), uid_id=userId, is_read=0).count()
            errorCount = db_OperateInfo.objects.filter(remindType='Error', is_read=0).count()
            warningCount = db_PushInfo.objects.filter(uid_id=userId, oinfo__remindType='Warning', is_read=0).count()
            obj_db_WorkorderManagement = db_WorkorderManagement.objects.filter(~Q(workState=3), is_del=0)
            unfinishedWorkOrder = 0  # ????????????????????????
            for i in obj_db_WorkorderManagement:
                obj_db_WorkBindPushToUsers = db_WorkBindPushToUsers.objects.filter(
                    is_del=0, work_id=i.id, uid_id=userId)
                if obj_db_WorkBindPushToUsers.exists():
                    unfinishedWorkOrder += 1

            if isAdmin:
                message = f"??????????????????: <br>" \
                          f"????????????({errorCount})," \
                          f"????????????({warningCount})," \
                          f"????????????({pushCount}),<br>" \
                          f"?????????????????????({unfinishedWorkOrder}),<br>" \
                          f"???????????????!"
            else:
                message = f"??????????????????: <br>" \
                          f"????????????({warningCount})," \
                          f"????????????({pushCount}),<br>" \
                          f"?????????????????????({unfinishedWorkOrder}),<br>" \
                          f"???????????????!"
            response['statusCode'] = 2000
            response['message'] = message

    return JsonResponse(response)


@accept_websocket  # ????????????????????????,???????????????,??????????????????????????????
def get_server_indicators(request):
    counter = 0  # ????????? ???10??????????????????
    if request.is_websocket():
        retMessage = str(request.websocket.wait(), 'utf-8')  # ??????????????????????????????
        if retMessage:
            objData = object_maker(json.loads(retMessage))
            token = objData.Params.token
            if objData.Message == "Start":  # ????????????
                while True:
                    sendText = {}
                    try:
                        retMessage = request.websocket.read()
                    except BaseException as e:
                        cls_Logging.print_log('info', 'get_server_indicators', f'???????????????,????????????:{e}')
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
                                                      f'?????????:{counter}???????????????,????????????')
                                break
                        sleep(1)


@accept_websocket  # ??????????????? ??????????????????,????????????,??????7??????Top10,????????????,????????????
def api_page_get_main_data(request):
    counter = 0  # ????????? ???10??????????????????
    if request.is_websocket():
        retMessage = str(request.websocket.wait(), 'utf-8')  # ??????????????????????????????
        if retMessage:
            objData = object_maker(json.loads(retMessage))

            proId = objData.Params.proId
            token = objData.Params.token
            userId = cls_FindTable.get_userId(token)
            if objData.Message == "Start":  # ????????????
                while True:
                    try:
                        retMessage = request.websocket.read()
                    except BaseException as e:
                        cls_Logging.print_log('info', 'get_server_indicators', f'???????????????,????????????:{e}')
                        break
                    else:
                        sendText = {
                            'testResults': cls_FindTable.get_overview_of_test_results(proId),  # ??????????????????
                            # ??????????????????????????????
                            'pageStatistical': cls_FindTable.get_page_under_statistical_data(proId),
                            'proStatistical': cls_FindTable.get_pro_under_statistical_data('API', proId),
                            'pastSevenDaysTop': cls_FindTable.get_past_seven_days_top_ten_data(proId),  # ??????7??????Top10
                            'proQueue': cls_FindTable.get_pro_queue(proId),  # ??????????????????
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
                                                      f'?????????:{counter}???????????????,????????????')
                                break
                        sleep(1)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # ??????????????????
def api_pagehome_select_test_results(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = object_maker(responseData)
        proId = objData.proId
    except BaseException as e:
        errorMsg = f"????????????:{e}"
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
@require_http_methods(["GET"])  # ?????????????????????????????????
def api_pagehome_select_page_statistical(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = object_maker(responseData)
        proId = objData.proId
    except BaseException as e:
        errorMsg = f"????????????:{e}"
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
@require_http_methods(["GET"])  # ?????????????????????????????????
def api_pagehome_select_pro_statistical(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = object_maker(responseData)
        proId = objData.proId
    except BaseException as e:
        errorMsg = f"????????????:{e}"
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
@require_http_methods(["GET"])  # ??????7??????Top10
def api_pagehome_select_Formerly_data(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = object_maker(responseData)
        proId = objData.proId
    except BaseException as e:
        errorMsg = f"????????????:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'home', 'api_pagehome_select__Formerly_data', errorMsg)
    else:
        pastSevenDaysTopTenData = cls_FindTable.get_past_seven_days_top_ten_data(proId)
        response['dataTable'] = pastSevenDaysTopTenData['dataTable']
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # ????????????
def api_pagehome_select_pro_queue(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = object_maker(responseData)
        proId = objData.proId
    except BaseException as e:
        errorMsg = f"????????????:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'home', 'api_pagehome_select_pro_queue', errorMsg)
    else:
        proQueue = cls_FindTable.get_pro_queue(proId)
        response['dataTable'] = proQueue['dataTable']
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])  # ??????????????????
def api_pagehome_handle_state(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        queueId = request.POST['queueId']
    except BaseException as e:
        errorMsg = f"????????????:{e}"
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
@require_http_methods(["GET"])  # ??????????????????
def select_sys_total(request):
    response = {}
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = object_maker(responseData)
    except BaseException as e:
        errorMsg = f"????????????:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('HOME', 'home', 'select_sys_total', errorMsg)
    else:
        # ????????????
        userTotal = db_UserTable.objects.filter(is_del=0, is_activation=1).count()
        # ?????????3??????????????????
        # ????????????
        caseTotal = db_CaseBaseData.objects.filter(is_del=0).count()

        # ????????????
        taskTotal = db_ApiTimingTask.objects.filter(is_del=0).count()

        # ????????????
        executeTotal = db_ApiQueue.objects.filter().count()

        response['statusCode'] = 2000
        response['userTotal'] = userTotal
        response['caseTotal'] = caseTotal
        response['taskTotal'] = taskTotal
        response['executeTotal'] = executeTotal
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["GET"])  # ????????????Top5??????
def select_user_total(request):
    response = {}
    dataList = []
    tempStatistical = []  # ??????????????????
    try:
        responseData = json.loads(json.dumps(request.GET))
        objData = object_maker(responseData)
    except BaseException as e:
        errorMsg = f"????????????:{e}"
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
        sortList = sorted(tempStatistical, key=operator.itemgetter('allTotal'), reverse=True)  # ????????????
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
