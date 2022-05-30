# Create your db here.
from django.db.models import Q
from rest_framework.authtoken.models import Token as db_Token
from login.models import UserTable as db_UserTable
from login.models import UserBindRole as db_UserBindRole
from ProjectManagement.models import ProManagement as db_ProManagement
from PageManagement.models import PageManagement as db_PageManagement
from FunManagement.models import FunManagement as db_FunManagement
from role.models import BasicRole as db_BasicRole
from Api_TestReport.models import ApiQueue as db_ApiQueue
from Api_TestReport.models import ApiTestReport as db_ApiTestReport
from Api_IntMaintenance.models import ApiBaseData as db_ApiBaseData
from Api_CaseMaintenance.models import CaseBaseData as db_CaseBaseData
from Api_TestReport.models import ApiReportItem as db_ApiReportItem
from WorkorderManagement.models import WorkorderManagement as db_WorkorderManagement
from WorkorderManagement.models import HistoryInfo as db_HistoryInfo
from WorkorderManagement.models import WorkBindPushToUsers as db_WorkBindPushToUsers
from Api_TimingTask.models import ApiTimingTask as db_ApiTimingTask
from Api_BatchTask.models import ApiBatchTask as db_ApiBatchTask
from DataBaseEnvironment.models import DataBase as db_DataBase
from Ui_ElementEvent.models import ElementEventComponent as db_ElementEventComponent

# Create reference here.
from ClassData.Logger import Logging as cls_Logging
from ClassData.Common import Common
from ClassData.DataSecurity import DataSecurity

import operator
import time
import ast

cls_Common = Common()
cls_DataSecurity = DataSecurity()


# Create your views here.
class FindTable(cls_Logging):
    # 根据TOKEN返回用户ID
    def get_userId(self, token):  # 从Hearder中获取用户ID
        token = db_Token.objects.filter(key=token)  # 内置查询方法
        if token.exists():
            obj_db_UserTable = db_UserTable.objects.filter(userId=token[0].user_id)
            if obj_db_UserTable:
                return obj_db_UserTable[0].id
            else:
                return None
        else:
            return None

    # 根据用户ID，返回角色ID
    def get_roleId(self, userId):  # 返回角色ID
        obj_db_UserBindRole = db_UserBindRole.objects.filter(is_del=0, user_id=userId)
        if obj_db_UserBindRole.exists():
            return obj_db_UserBindRole[0].role_id
        else:
            return None

    # 根据用户ID,返回用户名称,用于创建者的名称返回
    def get_userName(self, userId):
        obj_db_UserTable = db_UserTable.objects.filter(is_del=0, id=userId)
        if obj_db_UserTable.exists():
            return obj_db_UserTable[0].userName
        else:
            return None

    # 根据角色ID，返回角色是不是管理员
    def get_role_is_admin(self, roleId):
        obj_db_BasicRole = db_BasicRole.objects.filter(is_del=0, id=roleId)
        if obj_db_BasicRole.exists():
            isAdmin = obj_db_BasicRole[0].is_admin
            if isAdmin == 1:
                return True
            else:
                return False
        else:
            return False

    # 返回 所属项目
    def get_pro_name(self, proId):
        obj_db_ProManagement = db_ProManagement.objects.filter(id=proId)
        if obj_db_ProManagement.exists():
            return obj_db_ProManagement[0].proName
        else:
            return None

    # 返回 所属页面
    def get_page_name(self, pageId):
        obj_db_PageManagement = db_PageManagement.objects.filter(id=pageId)
        if obj_db_PageManagement.exists():
            return obj_db_PageManagement[0].pageName
        else:
            return None

    # 返回 所属功能
    def get_fun_name(self, funId):
        obj_db_FunManagement = db_FunManagement.objects.filter(id=funId)
        if obj_db_FunManagement.exists():
            return obj_db_FunManagement[0].funName
        else:
            return None

    # 判断队列是不是已结束
    def get_queue_state(self, taskType, taskId):
        obj_db_ApiQueue = db_ApiQueue.objects.filter(~Q(queueStatus=2), taskType=taskType, taskId=taskId)
        if obj_db_ApiQueue.exists():
            return True
        else:
            return False

    # 测试结果概述
    def get_overview_of_test_results(self, proId):
        results = {}
        passData = []
        failData = []
        errorData = []
        reportTime = []

        # 这里因该把删除的也显示出来
        obj_db_ApiTestReport = db_ApiTestReport.objects.filter(pid_id=proId).order_by('updateTime')
        for i in obj_db_ApiTestReport:
            reportTime.append(str(i.updateTime.strftime('%Y-%m-%d')))
        reportTime = list(set(reportTime))  # 去重复时间
        reportTime.sort()  # 排序
        for i in reportTime:
            passTotal = 0
            failTotal = 0
            errorTotal = 0
            staTime = i + " 00:00:00"
            endTime = i + " 23:59:59"
            select_db_ApiTestReport = obj_db_ApiTestReport.filter(updateTime__gte=staTime, updateTime__lte=endTime)
            for item in select_db_ApiTestReport:
                if item.reportStatus == 'Pass':
                    passTotal += 1
                elif item.reportStatus == 'Fail':
                    failTotal += 1
                elif item.reportStatus == 'Error':
                    errorTotal += 1
                else:
                    errorTotal += 1
            if passTotal != 0:
                passData.append({'name': i, 'value': [i, passTotal]})
            if failTotal != 0:
                failData.append({'name': i, 'value': [i, failTotal]})
            if errorTotal != 0:
                errorData.append({'name': i, 'value': [i, errorTotal]})

            results['timeData'] = reportTime
            results['passData'] = passData
            results['failData'] = failData
            results['errorData'] = errorData
        return results

    # 页面下所有数据的统计
    def get_page_under_statistical_data(self, proId):
        results = {
            'dataTable': []
        }

        obj_db_PageManagement = db_PageManagement.objects.filter(is_del=0, pid_id=proId)
        for item_page in obj_db_PageManagement:
            # region 获取本周时间
            # weekData = cls_Common.get_this_weeks_interval_data()
            # staTime = weekData[0].strftime('%Y-%m-%d') + " 00:00:00"
            # endTime = weekData[1].strftime('%Y-%m-%d') + " 23:59:59"
            # endregion
            obj_db_ApiBaseData = db_ApiBaseData.objects.filter(is_del=0, pid_id=proId, page_id=item_page.id)
            apiTotal = obj_db_ApiBaseData.count()  # 接口数量
            # region 本周新增
            # weekTotal = 0  # 本周新增
            # weekTotal += obj_db_ApiBaseData.filter(createTime__gte=staTime, createTime__lte=endTime).count()
            # weekTotal += db_CaseBaseData.objects.filter(
            #     pid_id=proId,page_id=item_page.id,createTime__gte=staTime, createTime__lte=endTime).count()
            # endregion
            # region 本周执行
            # performWeekTotal = db_ApiQueue.objects.filter(
            #     pid_id=proId, page_id__in=[item_page.id,None], updateTime__gte=staTime, updateTime__lte=endTime).count()
            # endregion
            # perforHistoryTotal = db_ApiQueue.objects.filter(pid_id=proId, page_id=item_page.id).count()  # 历史执行
            obj_db_CaseBaseData = db_CaseBaseData.objects.filter(is_del=0, page_id=item_page.id)
            results['dataTable'].append({
                'id': item_page.id,
                'pageName': item_page.pageName,
                'apiTotal': apiTotal,
                'unitTotal': obj_db_CaseBaseData.filter(testType="UnitTest").count(),
                'hybridTestTotal': obj_db_CaseBaseData.filter(testType="HybridTest").count(),
                'caseTotal': obj_db_CaseBaseData.count(),
                # 'weekTotal': weekTotal,
                # 'performWeekTotal': performWeekTotal,
                # 'perforHistoryTotal': perforHistoryTotal

            })
        return results

    # 项目下所有数据的统计
    def get_pro_under_statistical_data(self, sysType, proId):
        results = {
            'dataTable': []
        }
        # region 获取本周时间
        weekData = cls_Common.get_this_weeks_interval_data()
        staTime = weekData[0].strftime('%Y-%m-%d') + " 00:00:00"
        endTime = weekData[1].strftime('%Y-%m-%d') + " 23:59:59"
        # endregion
        if sysType == "API":
            obj_db_ApiBaseData = db_ApiBaseData.objects.filter(is_del=0, pid_id=proId)
            # region 本周新增
            weekTotal = 0  # 本周新增
            weekTotal += obj_db_ApiBaseData.filter(  # 接口
                pid_id=proId, createTime__gte=staTime, createTime__lte=endTime).count()
            weekTotal += db_CaseBaseData.objects.filter(  # 测试用例
                pid_id=proId, createTime__gte=staTime, createTime__lte=endTime).count()
            weekTotal += db_ApiTimingTask.objects.filter(  # 定时任务
                is_del=0, pid_id=proId, createTime__gte=staTime, createTime__lte=endTime).count()
            weekTotal += db_ApiBatchTask.objects.filter(  # 批量任务
                is_del=0, pid_id=proId, createTime__gte=staTime, createTime__lte=endTime).count()
            # endregion
            # region 本周执行
            performWeekTotal = db_ApiQueue.objects.filter(
                pid_id=proId, updateTime__gte=staTime, updateTime__lte=endTime).count()
            # endregion
            perforHistoryTotal = db_ApiQueue.objects.filter(pid_id=proId).count()  # 历史执行

            results['dataTable'].append({
                'taskTotal': db_ApiTimingTask.objects.filter(is_del=0, pid_id=proId).count(),  # 定时任务
                'batchTotal': db_ApiBatchTask.objects.filter(is_del=0, pid_id=proId).count(),  # 批量任务,
                'weekTotal': weekTotal,  # 本周新增
                'performWeekTotal': performWeekTotal,
                'perforHistoryTotal': perforHistoryTotal
            })
        return results

    # 过去7天内Top10
    def get_past_seven_days_top_ten_data(self, proId):
        results = {}
        dataTable = []

        # region 获取本周时间
        weekData = cls_Common.get_seven_days_ago_time()
        staTime = weekData[0].strftime('%Y-%m-%d') + " 00:00:00"
        endTime = weekData[1].strftime('%Y-%m-%d') + " 23:59:59"
        # endregion
        # 这里把删除的也显示出来,觉得被删除的一般都是引起系统错误的也算统计内
        obj_db_ApiTestReport = db_ApiTestReport.objects.filter(
            ~Q(reportStatus='Pass'), pid_id=proId, updateTime__gte=staTime, updateTime__lte=endTime)
        reportNameList = [i.reportName for i in obj_db_ApiTestReport]
        reportNameList = list(set(reportNameList))
        for item_reportName in reportNameList:
            failTotal = 0
            errorTotal = 0
            select_db_ApiTestReport = obj_db_ApiTestReport.filter(reportName=item_reportName)
            for i in select_db_ApiTestReport:
                if i.reportStatus == 'Fail':
                    failTotal += 1
                elif i.reportStatus == 'Error':
                    errorTotal += 1
                elif i.reportStatus == '':
                    errorTotal += 1

            if select_db_ApiTestReport[0].reportType == 'API':
                obj_db_ApiBaseData = db_ApiBaseData.objects.filter(id=select_db_ApiTestReport[0].taskId)
                if obj_db_ApiBaseData.exists():
                    itsName = f"{obj_db_ApiBaseData[0].page.pageName}/{obj_db_ApiBaseData[0].fun.funName}"
                else:
                    itsName = ""
            elif select_db_ApiTestReport[0].reportType == 'CASE':
                obj_db_CaseBaseData = db_CaseBaseData.objects.filter(id=select_db_ApiTestReport[0].taskId)
                if obj_db_CaseBaseData.exists():
                    itsName = f"{obj_db_CaseBaseData[0].page.pageName}/{obj_db_CaseBaseData[0].fun.funName}"
                else:
                    itsName = ""
            else:
                itsName = ""
            dataTable.append({
                'index': '',
                'itsName': itsName,
                'taskType': select_db_ApiTestReport[0].reportType,
                'taskName': item_reportName,
                'number': failTotal + errorTotal
            })
        dataTable = sorted(dataTable, key=operator.itemgetter('number'), reverse=True)  # 利用number来倒序排列
        # 给index 来赋值
        for index, i in enumerate(dataTable[:10], 1):
            dataTable[index - 1]['index'] = str(index)

        results['dataTable'] = dataTable
        return results

    # 我的工单
    def get_my_work(self, sysType, proId, userId):
        results = {}
        dataTable = []
        obj_db_WorkorderManagement = db_WorkorderManagement.objects.filter(
            ~Q(workState=3), is_del=0, sysType=sysType, pid_id=proId).order_by('-updateTime')
        for i in obj_db_WorkorderManagement:
            obj_db_HistoryInfo = db_HistoryInfo.objects.filter(work_id=i.id).order_by('-createTime')
            if obj_db_HistoryInfo.exists():
                message = obj_db_HistoryInfo[0].message
            else:
                message = ""
            # region 查询创建人
            obj_db_UserTable = db_UserTable.objects.filter(is_del=0, id=i.cuid)
            if obj_db_UserTable:
                createUserName = obj_db_UserTable[0].userName
            else:
                createUserName = None
            # endregion
            obj_db_WorkBindPushToUsers = db_WorkBindPushToUsers.objects.filter(is_del=0, uid_id=userId,
                                                                               work_id=i.id)
            # 创建人是自己 或 被关联人有自己
            bindUser = [item_bindUser.uid_id for item_bindUser in obj_db_WorkBindPushToUsers]
            if userId in bindUser or i.cuid == userId:
                timeArray = time.strptime(i.updateTime.strftime('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S")
                dataTable.append(
                    {"id": i.id,
                     "codeId": f'A-{i.id}',
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
                     "createUserName": createUserName,
                     })
        results['dataTable'] = dataTable
        return results

    # 获取项目队列
    def get_pro_queue(self, proId):
        results = {}
        dataTable = []

        obj_db_ApiQueue = db_ApiQueue.objects.filter(~Q(queueStatus='2'), pid_id=proId).order_by('-updateTime')
        for i in obj_db_ApiQueue:
            if i.taskType == 'API':
                obj_db_ApiBaseData = db_ApiBaseData.objects.filter(id=i.taskId)
                if obj_db_ApiBaseData.exists():
                    itsName = f"{obj_db_ApiBaseData[0].page.pageName}/{obj_db_ApiBaseData[0].fun.funName}"
                else:
                    itsName = ""
            elif i.taskType == 'CASE':
                obj_db_CaseBaseData = db_CaseBaseData.objects.filter(id=i.taskId)
                if obj_db_CaseBaseData.exists():
                    itsName = f"{obj_db_CaseBaseData[0].page.pageName}/{obj_db_CaseBaseData[0].fun.funName}"
                else:
                    itsName = ""
            else:
                itsName = ""
            obj_db_ApiReportItem = db_ApiReportItem.objects.filter(is_del=0, testReport_id=i.testReport_id)
            dataTable.append({
                'id': i.id,
                'itsName': itsName,
                'taskType': i.taskType,
                'taskName': i.testReport.reportName,
                'taskState': i.queueStatus,
                'performProgress': f"{obj_db_ApiReportItem.count()}/{i.testReport.apiTotal}",
                # 'updateTime': str(i.updateTime.strftime('%H:%M:%S')),
                'updateTime': str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                "userName": f"{i.uid.userName}({i.uid.nickName})",
            })
        results['dataTable'] = dataTable
        return results

    # 获取用户的email
    def user_email_list(self, userList):
        dataList = []
        for userId in userList:
            obj_db_UserTable = db_UserTable.objects.filter(id=userId)
            if obj_db_UserTable.exists():
                dataList.append(str(obj_db_UserTable[0].emails))

        return dataList

    # 查询数据库环境
    def get_data_base_data(self, dbId):
        results = {}
        obj_db_DataBase = db_DataBase.objects.filter(is_del=0, id=dbId)
        if obj_db_DataBase.exists():
            results['state'] = True
            results['dbData'] = {
                'dbType': obj_db_DataBase[0].dbType,
                'dataBaseIp': obj_db_DataBase[0].dataBaseIp,
                'port': obj_db_DataBase[0].port,
                'userName': obj_db_DataBase[0].userName,
                'passWord': cls_DataSecurity.aes_decode(ast.literal_eval(obj_db_DataBase[0].passWord)),
            }
        else:
            results['state'] = False
            results['errorMsg'] = '未找到当前数据库环境'
        return results

    # 返回元素中文名称
    def get_element_label_name(self, elementType):
        """
        :param elementType: 元素类型，List
        :return: 元素label名称
        """
        if elementType:
            obj_db_ElementEventComponent = db_ElementEventComponent.objects.filter(is_del=0, value=elementType[1])
            if obj_db_ElementEventComponent.exists():
                label = obj_db_ElementEventComponent[0].label
            else:
                label = ""
        else:
            label = ""
        return label
