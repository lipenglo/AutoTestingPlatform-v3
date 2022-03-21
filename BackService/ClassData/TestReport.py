# Create your db here.
from Api_TestReport.models import ApiTestReport as db_ApiTestReport
from Api_TestReport.models import ApiReportItem as db_ApiReportItem
from Api_TestReport.models import ApiReport as db_ApiReport
from Api_TestReport.models import ApiQueue as db_ApiQueue
from Api_CaseMaintenance.models import CaseBaseData as db_CaseBaseData
from Api_TestReport.models import ApiReportTaskItem as db_ApiReportTaskItem
from Api_TestReport.models import WarningInfo as db_WarningInfo

import ast
import json

# Create reference here.
from ClassData.Logger import Logging as cls_Logging
from ClassData.Common import Common

cls_Common = Common()


class ApiReport(cls_Logging):
    # 创建主1级报告
    def create_test_report(self, proId, reportName, reportType, taskId, apiTotal, userId):
        """
        :param proId:
        :param reportName:
        :param reportType: 报告类型(API:单接口,CASE:测试用例,TASK:定时任务,BATCH:批量任务)
        :param taskId: ApiId/CaseId/TaskId/BatchId,根据任务类型来取
        :param apiTotal:
        :param userId:
        :return:
        """
        results = {}
        try:
            save_db_ApiTestReport = db_ApiTestReport.objects.create(
                pid_id=proId,
                reportName=reportName,
                reportType=reportType,
                taskId=taskId,
                apiTotal=apiTotal,
                uid_id=userId,
                is_del=0,
            )
        except BaseException as e:
            results['state'] = False
            errorMsg = f"保存失败:{e}"
            results['errorMsg'] = errorMsg
            cls_Logging.record_error_info(self, 'API', 'ClassData>TestReport>ApiReport', 'create_test_report', errorMsg)
        else:
            results['state'] = True
            results['testReportId'] = save_db_ApiTestReport.id
        return results

    # 创建2级报告列表
    def create_report_items(self, testReportId, apiId, apiName, caseId=None, reportTaskItemId=None):
        """
        :param testReportId:
        :param apiId:
        :param apiName:
        :param caseId: 单接口没有此ID/Case,Task,Batch类型时这里显示CaseId
        :return:
        """
        results = {}
        try:
            save_db_ApiReportItem = db_ApiReportItem.objects.create(
                testReport_id=testReportId,
                apiId_id=apiId,
                apiName=apiName,
                case_id=caseId,
                batchItem_id=reportTaskItemId,
                successTotal=0,
                failTotal=0,
                errorTotal=0,
                is_del=0,
            )
        except BaseException as e:
            results['state'] = False
            errorMsg = f"保存失败:{e}"
            results['errorMsg'] = errorMsg
            cls_Logging.print_log(self, 'error', 'create_report_items', errorMsg)
            cls_Logging.record_error_info(
                self, 'API', 'ClassData>TestReport>ApiReport', 'create_report_items', errorMsg)
        else:
            results['state'] = True
            results['reportItemId'] = save_db_ApiReportItem.id
        return results

    # 创建2级批量任务的列表
    def create_report_task_items(self, testReportId, taskId, taskName):
        results = {}
        try:
            save_db_ApiReportTaskItem = db_ApiReportTaskItem.objects.create(
                testReport_id=testReportId,
                task_id=taskId,
                taskName=taskName,
                successTotal=0,
                failTotal=0,
                errorTotal=0,
                is_del=0,
            )
        except BaseException as e:
            results['state'] = False
            errorMsg = f"保存失败:{e}"
            results['errorMsg'] = errorMsg
            cls_Logging.print_log(self, 'error', 'create_report_task_items', errorMsg)
            cls_Logging.record_error_info(
                self, 'API', 'ClassData>TestReport>ApiReport', 'create_report_task_items', errorMsg)
        else:
            results['state'] = True
            results['reportTaskItemId'] = save_db_ApiReportTaskItem.id
        return results

    # 更新2级报告 批量任务列表
    def update_report_task_items(self, testReportId):
        runningTime = 0
        passTotal = 0
        failTotal = 0
        errorTotal = 0
        obj_db_ApiReportTaskItem = db_ApiReportTaskItem.objects.filter(is_del=0, testReport_id=testReportId)
        for item_reportTaskItem in obj_db_ApiReportTaskItem:
            obj_db_ApiReportItem = db_ApiReportItem.objects.filter(
                is_del=0, testReport_id=testReportId, batchItem_id=item_reportTaskItem.id)
            for item_reportItem in obj_db_ApiReportItem:
                runningTime += item_reportItem.runningTime
                passTotal += item_reportItem.successTotal
                failTotal += item_reportItem.failTotal
                errorTotal += item_reportItem.errorTotal
            db_ApiReportTaskItem.objects.filter(id=item_reportTaskItem.id).update(
                runningTime=runningTime, successTotal=passTotal, failTotal=failTotal, errorTotal=errorTotal
            )

    # 创建单接口报告
    def create_api_report(self, reportItemId, results):
        try:
            db_ApiReport.objects.create(
                reportItem_id=reportItemId,
                requestUrl=results['request']['requestUrl'],
                requestType=results['request']['requestType'],
                requestHeaders=results['request']['headersDict'],
                requestData=results['request']['requestDataDict'],
                # requestFile=results['requestFile'],
                reportStatus=results['response']['reportState'],

                statusCode=results['response']['responseCode'],
                responseHeaders=results['response']['responseHeaders'],
                responseInfo=results['response']['text'],
                requestExtract=results['response']['extractTable'],

                # responseExtract=results['response']['responseExtract'],
                responseValidate=results['response']['assertionTable'],

                preOperationInfo=results['response']['preOperationTable'],
                rearOperationInfo=results['response']['rearOperationTable'],
                errorInfo=results['response']['errorInfoTable'],
                runningTime=results['response']['time'],
                is_del=0,
            )
        except BaseException as e:
            errorMsg = f"保存失败:{e}"
            cls_Logging.print_log(self, 'error', 'create_api_report', errorMsg)
            cls_Logging.record_error_info(self, 'API', 'ClassData>TestReport>ApiReport', 'create_api_report', errorMsg)

    # 更新 成功失败数量及运行总时间
    def update_report_items(self, testReportId, reportItemId):
        successTotal = 0
        failTotal = 0
        errorTotal = 0
        itemRunningTime = 0  # db_ApiReportItem的统计耗时
        testReportRunningTime = 0  # db_ApiTestReport的统计耗时
        obj_db_ApiReport = db_ApiReport.objects.filter(is_del=0, reportItem_id=reportItemId)
        for i in obj_db_ApiReport:
            if i.reportStatus == 'Pass':
                successTotal += 1
            elif i.reportStatus == 'Fail':
                failTotal += 1
            else:  # Error
                errorTotal += 1

            itemRunningTime += float(i.runningTime)

        # 更新报告成功失败数
        db_ApiReportItem.objects.filter(is_del=0, testReport_id=testReportId, id=reportItemId).update(
            successTotal=successTotal, failTotal=failTotal, errorTotal=errorTotal, runningTime=itemRunningTime,
            updateTime=cls_Common.get_date_time()
        )
        reportStatus = self.get_report_status(failTotal, errorTotal)
        db_db_ApiReportItem = db_ApiReportItem.objects.filter(is_del=0, testReport_id=testReportId)
        for i in db_db_ApiReportItem:
            testReportRunningTime += float(i.runningTime)
        db_ApiTestReport.objects.filter(id=testReportId).update(
            reportStatus=reportStatus, runningTime=round(testReportRunningTime, 2),
            updateTime=cls_Common.get_date_time()
        )

    # 创建队列
    def create_queue(self, proId, pageId, funId, taskType, taskId, testReportId, userId):
        """
        :param taskId: 务ID,apiId,CaseId,TaskId,BatchId
        :param testReportId:
        :param userId:
        :return:
        """
        save_db_ApiQueue = db_ApiQueue.objects.create(
            pid_id=proId, page_id=pageId, fun_id=funId, taskType=taskType, taskId=taskId, testReport_id=testReportId,
            queueStatus=0, uid_id=userId
        )
        return save_db_ApiQueue.id

    # 更新队列状态
    def update_queue(self, queueId, queueStatus, userId):
        """
        :param taskId: 务ID,apiId,CaseId,TaskId,BatchId
        :param testReportId:
        :param queueStatus: 队列执行状态(0:未开始,1:执行中,2:已结束)
        :param userId:
        :return:
        """
        db_ApiQueue.objects.filter(id=queueId).update(queueStatus=queueStatus, uid_id=userId)

    # 警示信息
    def create_warning_info(self, testReportId, triggerType, taskId, taskName, info, userId):
        db_WarningInfo.objects.create(
            testReport_id=testReportId,
            triggerType=triggerType,
            taskId=taskId,
            taskName=taskName,
            info=info,
            uid_id=userId,
        )

    # 测试报告-返回顶部详细数据
    def get_report_top_data(self, testReportId):
        results = {
            'topData': {
                'createUserName': None,
                'reportName': None,
                'reportType': None,
                'createTime': '',
                'runningTime': 0,
                'reportStatus': None,
                'passTotal': 0,
                'failTotal': 0,
                'errorTotal': 0,
                'allTotal': 0,
                'passRate': 0,  # 通过率
                'failedTotal': 0,  # 未执行'
            }
        }

        obj_db_ApiTestReport = db_ApiTestReport.objects.filter(id=testReportId, is_del=0)
        if obj_db_ApiTestReport.exists():
            reportType = obj_db_ApiTestReport[0].reportType
            reportName = obj_db_ApiTestReport[0].reportName
            createTime = str(obj_db_ApiTestReport[0].updateTime.strftime('%Y-%m-%d %H:%M:%S'))
            reportStatus = obj_db_ApiTestReport[0].reportStatus
            apiTotal = obj_db_ApiTestReport[0].apiTotal
            createUserName = obj_db_ApiTestReport[0].uid.userName
            results['topData']['reportName'] = reportName
            results['topData']['createTime'] = createTime
            results['topData']['reportStatus'] = reportStatus
            results['topData']['reportType'] = reportType
            results['topData']['createUserName'] = createUserName

            obj_db_ApiReportItem = db_ApiReportItem.objects.filter(is_del=0, testReport_id=testReportId)
            passTotal = 0
            failTotal = 0
            errorTotal = 0
            runningTime = 0
            failedTotal = apiTotal  # 未执行数

            if reportType == "API":
                allTotal = 1
            elif reportType == "CASE":
                allTotal = obj_db_ApiReportItem.count()
            elif reportType == "TASK":
                caseList = [i.case_id for i in obj_db_ApiReportItem]
                caseList = set(caseList)
                allTotal = len(caseList)
            else:  # BATCH
                allTotal = db_ApiReportTaskItem.objects.filter(is_del=0, testReport_id=testReportId).count()
            prePassTotal = 0  # 前置成功
            rearPassTotal = 0  # 后置成功
            extractPassTotal = 0  # 提取成功
            assertionsPassTotal = 0  # 断言成功
            for item_reportItem in obj_db_ApiReportItem:
                passTotal += int(item_reportItem.successTotal)
                failTotal += int(item_reportItem.failTotal)
                errorTotal += int(item_reportItem.errorTotal)
                failedTotal -= 1

                obj_db_ApiReport = db_ApiReport.objects.filter(is_del=0, reportItem_id=item_reportItem.id)
                for item_apiReport in obj_db_ApiReport:
                    runningTime += float(item_apiReport.runningTime)
                    # region 前置数
                    if item_apiReport.preOperationInfo:
                        preOperationInfo = ast.literal_eval(item_apiReport.preOperationInfo)
                    else:
                        preOperationInfo = []
                    for item_pre in preOperationInfo:
                        if item_pre['resultsState']:
                            prePassTotal += 1
                    # endregion
                    # region 后置数
                    if item_apiReport.rearOperationInfo:
                        rearOperationInfo = ast.literal_eval(item_apiReport.rearOperationInfo)
                    else:
                        rearOperationInfo = []
                    for item_rear in rearOperationInfo:
                        if item_rear['resultsState']:
                            rearPassTotal += 1
                    # endregion
                    # region 提取数
                    if item_apiReport.requestExtract:
                        requestExtract = ast.literal_eval(item_apiReport.requestExtract)
                        extractPassTotal += len(requestExtract)

                    # endregion
                    # region 断言数
                    if item_apiReport.responseValidate:
                        responseValidate = ast.literal_eval(item_apiReport.responseValidate)
                    else:
                        responseValidate = []
                    for item_validate in responseValidate:
                        if item_validate['results']:
                            assertionsPassTotal += 1
                    # endregion
            results['topData']['passTotal'] = passTotal
            results['topData']['failTotal'] = failTotal
            results['topData']['errorTotal'] = errorTotal
            results['topData']['runningTime'] = round(runningTime, 2)
            results['topData']['failedTotal'] = failedTotal
            results['topData']['allTotal'] = allTotal

            allTotal = passTotal + failTotal + errorTotal
            if passTotal == 0 and failTotal == 0 and errorTotal == 0:
                passRate = 0
            else:
                passRate = passTotal / allTotal * 100
            results['topData']['passRate'] = int(passRate)

            results['topData']['prePassTotal'] = prePassTotal
            results['topData']['rearPassTotal'] = rearPassTotal
            results['topData']['assertionsPassTotal'] = assertionsPassTotal
            results['topData']['extractPassTotal'] = extractPassTotal
            results['state'] = True
        else:
            results['state'] = False
            results['errorMsg'] = "当前选择测试报告不存在,请刷新后在重新尝试!"
        return results

    # 测试报告-历史趋势图
    def get_trend_chart(self, testReportId):
        results = {
            'state': True,
            'dataDict': {}
        }
        reportIdList = []
        passList = []
        failList = []
        errorList = []
        obj_db_ApiTestReport = db_ApiTestReport.objects.filter(is_del=0, id=testReportId)
        if obj_db_ApiTestReport.exists():
            taskId = obj_db_ApiTestReport[0].taskId
            reportType = obj_db_ApiTestReport[0].reportType

            select_db_ApiTestReport = db_ApiTestReport.objects.filter(is_del=0, reportType=reportType, taskId=taskId)
            select_db_ApiTestReport = select_db_ApiTestReport[::-1][0:100][::-1]
            for item_testReport in select_db_ApiTestReport:
                passTotal = 0
                failTotal = 0
                errorTotal = 0
                obj_db_ApiReportItem = db_ApiReportItem.objects.filter(is_del=0, testReport_id=item_testReport.id)
                for item_reportItem in obj_db_ApiReportItem:
                    passTotal += item_reportItem.successTotal
                    failTotal += item_reportItem.failTotal
                    errorTotal += item_reportItem.errorTotal
                if passTotal == 0 and failTotal == 0 and errorTotal == 0:
                    pass
                else:
                    reportIdList.append(f'#{item_testReport.id}')
                    passList.append(passTotal)
                    failList.append(failTotal)
                    errorList.append(errorTotal)

            results['dataDict'] = {
                'reportIdList': reportIdList,
                'passList': passList,
                'failList': failList,
                'errorList': errorList,
            }
        else:
            results['state'] = False
            results['errorMsg'] = '当前测试报告不存在!'
        return results

    # 测试报告-简要列表
    def get_report_brief_item(self, testReportId):
        results = {
            'state': True,
        }
        dataList = []
        obj_db_ApiTestReport = db_ApiTestReport.objects.filter(is_del=0, id=testReportId)
        if obj_db_ApiTestReport.exists():
            obj_db_ApiReportItem = db_ApiReportItem.objects.filter(is_del=0, testReport_id=testReportId)
            reportType = obj_db_ApiTestReport[0].reportType
            if reportType in ["API", "CASE"]:
                for item_reportItem in obj_db_ApiReportItem:
                    successTotal = item_reportItem.successTotal
                    failTotal = item_reportItem.failTotal
                    errorTotal = item_reportItem.errorTotal
                    allTotal = successTotal + failTotal + errorTotal
                    if successTotal == 0 and failTotal == 0 and errorTotal == 0:
                        passRate = 0
                    else:
                        passRate = successTotal / allTotal * 100
                    dataList.append({
                        'id': item_reportItem.apiId_id,
                        'name': item_reportItem.apiName,
                        'passTotal': item_reportItem.successTotal,
                        'failTotal': item_reportItem.failTotal,
                        'errorTotal': item_reportItem.errorTotal,
                        'passRate': f"{round(passRate, 1)}%",
                    })
            elif reportType == "TASK":
                caseList = [i.case_id for i in obj_db_ApiReportItem]
                setCaseList = list(set(caseList))
                setCaseList.sort(key=caseList.index)
                for item_caseId in setCaseList:
                    caseStatistical = self.get_report_case_statistical(testReportId, item_caseId)
                    obj_db_CaseBaseData = db_CaseBaseData.objects.filter(id=item_caseId)
                    if obj_db_CaseBaseData.exists():
                        caseName = obj_db_CaseBaseData[0].caseName
                    else:
                        caseName = ""
                    passRate = caseStatistical['passTotal'] / caseStatistical['allTotal'] * 100
                    dataList.append({
                        'id': item_caseId,
                        'name': caseName,
                        'passTotal': caseStatistical['passTotal'],
                        'failTotal': caseStatistical['failTotal'],
                        'errorTotal': caseStatistical['errorTotal'],
                        'passRate': f"{round(passRate, 1)}%",
                    })
            else:  # BATCH
                obj_db_ApiReportTaskItem = db_ApiReportTaskItem.objects.filter(is_del=0, testReport_id=testReportId)
                for item_taskItem in obj_db_ApiReportTaskItem:
                    passTotal = item_taskItem.successTotal
                    allTotal = item_taskItem.successTotal + item_taskItem.failTotal + item_taskItem.errorTotal
                    passRate = passTotal / allTotal * 100
                    dataList.append({
                        'id': item_taskItem.id,
                        'name': item_taskItem.taskName,
                        'passTotal': passTotal,
                        'failTotal': item_taskItem.failTotal,
                        'errorTotal': item_taskItem.errorTotal,
                        'passRate': f"{round(passRate, 1)}%",
                    })
            results['dataList'] = dataList
        else:
            results['state'] = False
            results['errorMsg'] = '当前查询的报告不存在!'
        return results

    # 测试报告-警示信息
    def get_warngig_info(self, testReportId):
        dataList = []
        obj_db_WarningInfo = db_WarningInfo.objects.filter(testReport_id=testReportId)
        for i in obj_db_WarningInfo:
            dataList.append({
                'id': i.id,
                'triggerType': i.triggerType,
                'taskName': i.taskName,
                'info': i.info,
            })

        return dataList

    # 测试报告-获取测试套件
    def get_report_suite_data(self, testReportId):
        results = {
            'state': True
        }
        dataList = []
        obj_db_ApiTestReport = db_ApiTestReport.objects.filter(is_del=0, id=testReportId)
        if obj_db_ApiTestReport.exists():
            reportType = obj_db_ApiTestReport[0].reportType
            obj_db_ApiReportItem = db_ApiReportItem.objects.filter(is_del=0, testReport_id=testReportId)
            if reportType in ["API", "CASE"]:
                for item_reportItem in obj_db_ApiReportItem:
                    obj_db_ApiReport = db_ApiReport.objects.filter(is_del=0, reportItem_id=item_reportItem.id)
                    if obj_db_ApiReport.exists():
                        code = obj_db_ApiReport[0].statusCode
                    else:
                        code = None

                    dataList.append({
                        'id': item_reportItem.id,
                        'layerType': 'API',
                        'label': item_reportItem.apiName,
                        'time': item_reportItem.runningTime,
                        'reportStatus': self.get_report_status(item_reportItem.failTotal, item_reportItem.errorTotal),
                        'code': code
                    })
            elif reportType == "TASK":
                caseList = [i.case_id for i in obj_db_ApiReportItem]
                setCaseList = list(set(caseList))
                setCaseList.sort(key=caseList.index)
                for item_caseId in setCaseList:
                    # region 获取API层
                    children = []
                    select_db_ApiReportItem = obj_db_ApiReportItem.filter(case_id=item_caseId)
                    for item_reportItem in select_db_ApiReportItem:
                        obj_db_ApiReport = db_ApiReport.objects.filter(is_del=0, reportItem_id=item_reportItem.id)
                        if obj_db_ApiReport.exists():
                            code = obj_db_ApiReport[0].statusCode
                        else:
                            code = None
                        children.append({
                            'id': item_reportItem.id,
                            'layerType': 'API',
                            'label': item_reportItem.apiName,
                            'time': item_reportItem.runningTime,
                            'reportStatus': self.get_report_status(item_reportItem.failTotal,
                                                                   item_reportItem.errorTotal),
                            'code': code
                        })
                    # endregion
                    # region 获取CASE 层
                    obj_db_CaseBaseData = db_CaseBaseData.objects.filter(id=item_caseId)
                    if obj_db_CaseBaseData.exists():
                        caseName = obj_db_CaseBaseData[0].caseName
                    else:
                        caseName = ""
                    caseStatistical = self.get_report_case_statistical(testReportId, item_caseId)
                    dataList.append({
                        'id': item_caseId,
                        'label': caseName,
                        'layerType': 'CASE',
                        'passTotal': caseStatistical['passTotal'],
                        'failTotal': caseStatistical['failTotal'],
                        'errorTotal': caseStatistical['errorTotal'],
                        'reportStatus': self.get_report_status(
                            caseStatistical['failTotal'], caseStatistical['errorTotal']),
                        'children': children
                    })
                    # endregion
            else:  # BATCH
                obj_db_ApiReportTaskItem = db_ApiReportTaskItem.objects.filter(is_del=0, testReport_id=testReportId)
                for item_taskItem in obj_db_ApiReportTaskItem:
                    childrenCase = []  # 用例层
                    obj_db_ApiReportItem = db_ApiReportItem.objects.filter(
                        is_del=0, testReport_id=testReportId, batchItem_id=item_taskItem.id)

                    caseList = [i.case_id for i in obj_db_ApiReportItem]
                    setCaseList = list(set(caseList))
                    setCaseList.sort(key=caseList.index)
                    for item_caseId in setCaseList:
                        # region 获取API 层
                        children = []
                        select_db_ApiReportItem = obj_db_ApiReportItem.filter(case_id=item_caseId)
                        for item_reportItem in select_db_ApiReportItem:
                            obj_db_ApiReport = db_ApiReport.objects.filter(is_del=0, reportItem_id=item_reportItem.id)
                            if obj_db_ApiReport.exists():
                                code = obj_db_ApiReport[0].statusCode
                            else:
                                code = None
                            children.append({
                                'id': item_reportItem.id,
                                'layerType': 'API',
                                'label': item_reportItem.apiName,
                                'time': item_reportItem.runningTime,
                                'reportStatus': self.get_report_status(
                                    item_reportItem.failTotal, item_reportItem.errorTotal),
                                'code': code
                            })
                        # endregion
                        # region 获取CASE 层
                        obj_db_CaseBaseData = db_CaseBaseData.objects.filter(id=item_caseId)
                        if obj_db_CaseBaseData.exists():
                            caseName = obj_db_CaseBaseData[0].caseName
                        else:
                            caseName = ""
                        caseStatistical = self.get_report_case_statistical(testReportId, item_caseId)
                        childrenCase.append({
                            'id': item_caseId,
                            'label': caseName,
                            'layerType': 'CASE',
                            'passTotal': caseStatistical['passTotal'],
                            'failTotal': caseStatistical['failTotal'],
                            'errorTotal': caseStatistical['errorTotal'],
                            'children': children
                        })
                        # endregion
                    taskStatistical = self.get_report_task_statistical(testReportId, item_taskItem.task_id)
                    dataList.append({
                        'id': item_taskItem.id,
                        'layerType': 'TASK',
                        'label': item_taskItem.taskName,
                        'passTotal': taskStatistical['passTotal'],
                        'failTotal': taskStatistical['failTotal'],
                        'errorTotal': taskStatistical['errorTotal'],
                        'reportStatus': self.get_report_status(
                            taskStatistical['failTotal'], taskStatistical['errorTotal']),
                        'children': childrenCase
                    })
            results['dataList'] = dataList
        else:
            results['state'] = False
            results['errorMsg'] = '当前查询的报告不存在!'
        return results

    # # 测试报告-返回一级列表数据
    # def get_report_first_list(self, testReportId):
    #     # 根据报告的类型 展示第1层列表是 接口 用例 定时任务 批量任务
    #     results = {}
    #     firstList = []
    #     obj_db_ApiTestReport = db_ApiTestReport.objects.filter(id=testReportId)
    #     if obj_db_ApiTestReport.exists():
    #         reportType = obj_db_ApiTestReport[0].reportType
    #         if reportType == "API" or reportType == "CASE":
    #             obj_db_ApiReportItem = db_ApiReportItem.objects.filter(is_del=0, testReport_id=testReportId)
    #             for i in obj_db_ApiReportItem:
    #                 passTotal = i.successTotal
    #                 failTotal = i.failTotal
    #                 errorTotal = i.errorTotal
    #                 if passTotal + failTotal + errorTotal == 0:
    #                     reportStatus = 'Error'
    #                 elif errorTotal >= 1:
    #                     reportStatus = 'Error'
    #                 elif failTotal >= 1:
    #                     reportStatus = 'Fail'
    #                 else:
    #                     reportStatus = 'Pass'
    #
    #                 firstList.append({
    #                     'id': i.id,
    #                     'name': i.apiName,
    #                     'reportStatus': reportStatus,
    #                 })
    #         elif reportType == "TASK":
    #             obj_db_ApiReportItem = db_ApiReportItem.objects.filter(
    #                 is_del=0, testReport_id=testReportId).order_by('updateTime')
    #             # 先筛选出当前报告的用例ID列表
    #             caseList = [i.case_id for i in obj_db_ApiReportItem]
    #             setCaseList = list(set(caseList))
    #             setCaseList.sort(key=caseList.index)
    #             for item_caseId in setCaseList:
    #                 select_db_ApiReportItem = obj_db_ApiReportItem.filter(case_id=item_caseId)
    #                 passTotal = 0
    #                 failTotal = 0
    #                 errorTotal = 0
    #                 for i in select_db_ApiReportItem:
    #                     passTotal += i.successTotal
    #                     failTotal += i.failTotal
    #                     errorTotal += i.errorTotal
    #                 if passTotal + failTotal + errorTotal == 0:
    #                     reportStatus = 'Error'
    #                 elif errorTotal >= 1:
    #                     reportStatus = 'Error'
    #                 elif failTotal >= 1:
    #                     reportStatus = 'Fail'
    #                 else:
    #                     reportStatus = 'Pass'
    #                 obj_db_CaseBaseData = db_CaseBaseData.objects.filter(id=item_caseId)
    #                 if obj_db_CaseBaseData.exists():
    #                     caseName = obj_db_CaseBaseData[0].caseName
    #                 else:
    #                     caseName = ""
    #                 firstList.append({
    #                     'id': item_caseId,
    #                     'name': caseName,
    #                     'reportStatus': reportStatus,
    #                 })
    #         else:
    #             obj_db_ApiReportTaskItem = db_ApiReportTaskItem.objects.filter(
    #                 is_del=0, testReport_id=testReportId).order_by('updateTime')
    #             for item_reportTaskItem in obj_db_ApiReportTaskItem:
    #                 obj_db_ApiReportItem = db_ApiReportItem.objects.filter(
    #                     is_del=0, testReport_id=testReportId, batchItem_id=item_reportTaskItem.id).order_by(
    #                     'updateTime')
    #                 # 先筛选出当前报告的用例ID列表
    #                 caseList = [i.case_id for i in obj_db_ApiReportItem]
    #                 setCaseList = list(set(caseList))
    #                 setCaseList.sort(key=caseList.index)
    #                 reportItemList = []
    #                 for item_caseId in setCaseList:
    #                     select_db_ApiReportItem = obj_db_ApiReportItem.filter(case_id=item_caseId)
    #                     passTotal = 0
    #                     failTotal = 0
    #                     errorTotal = 0
    #                     for i in select_db_ApiReportItem:
    #                         passTotal += i.successTotal
    #                         failTotal += i.failTotal
    #                         errorTotal += i.errorTotal
    #                     if passTotal + failTotal + errorTotal == 0:
    #                         reportItemList.append('Error')
    #                     elif errorTotal >= 1:
    #                         reportItemList.append('Error')
    #                     elif failTotal >= 1:
    #                         reportItemList.append('Fail')
    #                     else:
    #                         reportItemList.append('Pass')
    #                 if 'Error' in reportItemList:
    #                     reportStatus = 'Error'
    #                 elif 'Fail' in reportItemList:
    #                     reportStatus = 'Fail'
    #                 else:
    #                     reportStatus = 'Pass'
    #                 firstList.append({
    #                     'id': item_reportTaskItem.id,
    #                     'name': item_reportTaskItem.taskName,
    #                     'reportStatus': reportStatus,
    #                 })
    #         results['state'] = True
    #         results['firstList'] = firstList
    #     else:
    #         results['state'] = False
    #         results['errorMsg'] = "当前选择的报告数据缺失!"
    #     return results
    #
    def get_report_api(self, reportItemId):
        results = {}
        obj_db_ApiReportItem = db_ApiReportItem.objects.filter(is_del=0, id=reportItemId)
        if obj_db_ApiReportItem.exists():
            obj_db_ApiReport = db_ApiReport.objects.filter(is_del=0, reportItem_id=obj_db_ApiReportItem[0].id)
            if obj_db_ApiReport.exists():
                general = []  # 基本信息
                requestHeaders = []
                requestData = []
                operationData = []  # 包含前置和后置
                # region 保存基本信息
                general.append({'key': 'Request URL:', 'value': obj_db_ApiReport[0].requestUrl})
                general.append({'key': 'Request Type:', 'value': obj_db_ApiReport[0].requestType})
                general.append({'key': 'Status Code:', 'value': obj_db_ApiReport[0].statusCode})
                # endregion
                # region 保存请求头
                ret_requestHeaders = ast.literal_eval(obj_db_ApiReport[0].requestHeaders)
                for item_header in ret_requestHeaders:
                    requestHeaders.append({'key': item_header, 'value': ret_requestHeaders[item_header]})
                # endregion
                # region 反回求头
                if obj_db_ApiReport[0].responseHeaders:
                    responseHeaders = ast.literal_eval(obj_db_ApiReport[0].responseHeaders)
                else:
                    responseHeaders = []
                # endregion
                # region 保存请求主体
                ret_requestData = ast.literal_eval(obj_db_ApiReport[0].requestData)
                for item_body in ret_requestData:
                    requestData.append({'key': item_body, 'value': ret_requestData[item_body]})
                # endregion
                # region 返回主体信息
                try:
                    ret_responseInfo = eval(obj_db_ApiReport[0].responseInfo)
                    responseInfo = json.dumps(ret_responseInfo, indent=4, separators=(',', ':'), ensure_ascii=False)
                except BaseException as e:
                    responseInfo = obj_db_ApiReport[0].responseInfo
                # endregion
                # region  提取
                if obj_db_ApiReport[0].requestExtract:
                    extract = ast.literal_eval(obj_db_ApiReport[0].requestExtract)
                else:
                    extract = []
                # endregion
                # region 断言
                if obj_db_ApiReport[0].responseValidate:
                    validateResults = ast.literal_eval(obj_db_ApiReport[0].responseValidate)  # 断言结果
                else:
                    validateResults = []
                # endregion
                # region 前后置操作
                if obj_db_ApiReport[0].preOperationInfo:
                    preOperationInfo = ast.literal_eval(obj_db_ApiReport[0].preOperationInfo)
                else:
                    preOperationInfo = []

                if obj_db_ApiReport[0].rearOperationInfo:
                    rearOperationInfo = ast.literal_eval(obj_db_ApiReport[0].rearOperationInfo)
                else:
                    rearOperationInfo = []

                for item_pre in preOperationInfo:
                    operationData.append({
                        'operatingPosition': 'Pre',
                        'operationType': item_pre['operationType'],
                        'callName': item_pre['callName'],
                        'callResults': item_pre['callResults'],
                        'resultsState': item_pre['resultsState']
                    })
                for item_rear in rearOperationInfo:
                    operationData.append({
                        'operatingPosition': 'Rear',
                        'operationType': item_rear['operationType'],
                        'callName': item_rear['callName'],
                        'callResults': item_rear['callResults'],
                        'resultsState': item_rear['resultsState']
                    })
                # endregion
                # region 错误信息
                if obj_db_ApiReport[0].errorInfo:
                    errorTableData = ast.literal_eval(obj_db_ApiReport[0].errorInfo)
                else:
                    errorTableData = []
                # endregion
                dataDict = {
                    'general': general,
                    'requestHeaders': requestHeaders,
                    'requestData': requestData,
                    'responseHeaders': responseHeaders,
                    'responseInfo': responseInfo,
                    'extract': extract,
                    'validateResults': validateResults,
                    'operationData': operationData,
                    'errorTableData': errorTableData,
                }
                results['state'] = True
                results['dataDict'] = dataDict
        else:
            results['state'] = False
            results['errorMsg'] = '未找到当前选择的接口数据!'

        return results

    # 返回报告状态
    def get_report_status(self, failTotal, errorTotal):
        reportStatus = ''
        if failTotal + errorTotal >= 1:
            if failTotal >= 1:
                reportStatus = 'Fail'
            if errorTotal >= 1:
                reportStatus = 'Error'
        else:
            reportStatus = 'Pass'
        return reportStatus

    # 获取报告-用例层的 成功失败统计
    def get_report_case_statistical(self, testReportId, caseId):
        results = {}
        obj_db_ApiReportItem = db_ApiReportItem.objects.filter(is_del=0, testReport_id=testReportId, case_id=caseId)
        passTotal = 0
        failTotal = 0
        errorTotal = 0

        for item_reportItem in obj_db_ApiReportItem:
            passTotal += item_reportItem.successTotal
            failTotal += item_reportItem.failTotal
            errorTotal += item_reportItem.errorTotal
        allTotal = passTotal + failTotal + errorTotal
        results['passTotal'] = passTotal
        results['failTotal'] = failTotal
        results['errorTotal'] = errorTotal
        results['allTotal'] = allTotal
        return results

    def get_report_task_statistical(self, testReportId, taskId):
        results = {}
        passTotal = 0
        failTotal = 0
        errorTotal = 0
        allTotal = 0
        obj_db_ApiReportTaskItem = db_ApiReportTaskItem.objects.filter(is_del=0, testReport_id=testReportId,
                                                                       task_id=taskId)
        for item_taskItem in obj_db_ApiReportTaskItem:
            obj_db_ApiReportItem = db_ApiReportItem.objects.filter(
                is_del=0, testReport_id=testReportId, batchItem_id=item_taskItem.id)

            caseList = [i.case_id for i in obj_db_ApiReportItem]
            setCaseList = list(set(caseList))
            setCaseList.sort(key=caseList.index)
            for item_caseId in setCaseList:
                caseStatistical = self.get_report_case_statistical(testReportId, item_caseId)
                passTotal += caseStatistical['passTotal']
                failTotal += caseStatistical['failTotal']
                errorTotal += caseStatistical['errorTotal']
                allTotal += caseStatistical['allTotal']
        results['passTotal'] = passTotal
        results['failTotal'] = failTotal
        results['errorTotal'] = errorTotal
        results['allTotal'] = allTotal
        return results


class UiReport(cls_Logging):
    pass


class PtsReport(cls_Logging):
    pass
