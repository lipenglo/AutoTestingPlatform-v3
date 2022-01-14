from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction

import json
import ast

# Create your db here.
from Api_TestReport.models import ApiTestReport as db_ApiTestReport
from Api_TestReport.models import ApiReportItem as db_ApiReportItem
from Api_TestReport.models import ApiReport as db_ApiReport
from Api_TestReport.models import ApiQueue as db_ApiQueue
from Api_CaseMaintenance.models import CaseBaseData as db_CaseBaseData

# Create reference here.
from ClassData.Logger import Logging
from ClassData.GlobalDecorator import GlobalDer
from ClassData.FindCommonTable import FindTable
from ClassData.Common import Common
from ClassData.ImageProcessing import ImageProcessing
from ClassData.ObjectMaker import object_maker as cls_object_maker
from ClassData.TestReport import ApiReport

# Create info here.
cls_Logging = Logging()
cls_GlobalDer = GlobalDer()
cls_FindTable = FindTable()
cls_Common = Common()
cls_ImageProcessing = ImageProcessing()
cls_ApiReport = ApiReport()


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

        proId = objData.proId
        reportName = objData.reportName
        reportType = objData.reportType
        reportStatus = objData.reportStatus

        current = int(objData.current)  # 当前页数
        pageSize = int(objData.pageSize)  # 一页多少条
        minSize = (current - 1) * pageSize
        maxSize = current * pageSize
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_TestReport', 'select_data', errorMsg)
    else:
        obj_db_ApiTestReport = db_ApiTestReport.objects.filter(is_del=0, pid_id=proId).order_by('-updateTime')
        select_db_ApiTestReport = obj_db_ApiTestReport[minSize: maxSize]
        if reportName:
            obj_db_ApiTestReport = obj_db_ApiTestReport.filter(reportName__icontains=reportName)
            select_db_ApiTestReport = obj_db_ApiTestReport[minSize: maxSize]
        if reportStatus:
            obj_db_ApiTestReport = obj_db_ApiTestReport.filter(reportStatus=reportStatus)
            select_db_ApiTestReport = obj_db_ApiTestReport[minSize: maxSize]
        if reportType:
            obj_db_ApiTestReport = obj_db_ApiTestReport.filter(reportType=reportType)
            select_db_ApiTestReport = obj_db_ApiTestReport[minSize: maxSize]
        for i in select_db_ApiTestReport:
            obj_db_ApiReportItem = db_ApiReportItem.objects.filter(is_del=0, testReport_id=i.id)
            obj_db_ApiQueue = db_ApiQueue.objects.filter(testReport_id=i.id)
            if i.runningTime is not None:
                runningTime = round(i.runningTime, 2)
            else:
                runningTime = None
            dataList.append(
                {"id": i.id,
                 "reportName": i.reportName,
                 "reportType": i.reportType,
                 "queueStatus": obj_db_ApiQueue[0].queueStatus if obj_db_ApiQueue.exists() else None,
                 "runningProgress": f"{obj_db_ApiReportItem.count()}/{i.apiTotal}",
                 "reportStatus": i.reportStatus if i.reportStatus else 'Error',
                 "runningTime": runningTime,
                 "updateTime": str(i.updateTime.strftime('%Y-%m-%d %H:%M:%S')),
                 "userName": f"{i.uid.userName}({i.uid.nickName})",
                 }
            )

        response['TableData'] = dataList
        response['Total'] = obj_db_ApiTestReport.count()
        response['statusCode'] = 2000
    return JsonResponse(response)


@cls_Logging.log
@cls_GlobalDer.foo_isToken
@require_http_methods(["POST"])
def delete_data(request):
    response = {}
    try:
        userId = cls_FindTable.get_userId(request.META['HTTP_TOKEN'])
        testReportId = request.POST['testReportId']
    except BaseException as e:
        errorMsg = f"入参错误:{e}"
        response['errorMsg'] = errorMsg
        cls_Logging.record_error_info('API', 'Api_TestReport', 'delete_data', errorMsg)
    else:
        obj_db_ApiTestReport = db_ApiTestReport.objects.filter(is_del=0, id=testReportId)
        if obj_db_ApiTestReport.exists():
            try:
                with transaction.atomic():  # 上下文格式，可以在python代码的任何位置使用
                    obj_db_ApiReportItem = db_ApiReportItem.objects.filter(is_del=0, testReport_id=testReportId)
                    for i in obj_db_ApiReportItem:
                        db_ApiReport.objects.filter(is_del=0, reportItem_id=i.id).update(is_del=1)  # API报告
                    obj_db_ApiReportItem.update(is_del=1)  # 测试集报告
                    obj_db_ApiTestReport.update(is_del=1, uid_id=userId)  # 主报告
            except BaseException as e:  # 自动回滚，不需要任何操作
                response['errorMsg'] = f'删除失败:{e}'
            else:
                response['statusCode'] = 2003
        else:
            response['errorMsg'] = '未找到当前功能数据,请刷新后重新尝试!'
    return JsonResponse(response)


# @cls_Logging.log
# @cls_GlobalDer.foo_isToken
# @require_http_methods(["GET"])  # 加载报告数据并返回第1层列表
# def load_report_data(request):
#     response = {}
#     try:
#         responseData = json.loads(json.dumps(request.GET))
#         objData = cls_object_maker(responseData)
#         testReportId = objData.testReportId
#     except BaseException as e:
#         errorMsg = f"入参错误:{e}"
#         response['errorMsg'] = errorMsg
#         cls_Logging.record_error_info('API', 'Api_TestReport', 'load_report_data', errorMsg)
#     else:
#         reportTopData = cls_ApiReport.get_report_top_data(testReportId)
#         if reportTopData['state']:
#             reportFirstList = cls_ApiReport.get_report_first_list(testReportId)
#             if reportFirstList['state']:
#                 response['topData'] = reportTopData['topData']
#                 response['firstList'] = reportFirstList['firstList']
#             else:
#                 response['errorMsg'] = reportFirstList['errorMsg']
#         else:
#             response['errorMsg'] = reportTopData['errorMsg']
#         if 'errorMsg' not in response:
#             response['statusCode'] = 2000
#     return JsonResponse(response)
#
#
# @cls_Logging.log
# @cls_GlobalDer.foo_isToken
# @require_http_methods(["GET"])  # 点击1层列表加载2层列表
# def load_report_case(request):
#     response = {}
#     secondList = []
#     try:
#         responseData = json.loads(json.dumps(request.GET))
#         objData = cls_object_maker(responseData)
#         reportType = objData.reportType
#         testReportId = objData.testReportId
#         id = objData.id  # 定时任务时:caseId,批量任务时:batchItemId
#     except BaseException as e:
#         errorMsg = f"入参错误:{e}"
#         response['errorMsg'] = errorMsg
#         cls_Logging.record_error_info('API', 'Api_TestReport', 'load_report_case', errorMsg)
#     else:
#         if reportType == 'TASK':
#             obj_db_ApiReportItem = db_ApiReportItem.objects.filter(
#                 is_del=0, testReport_id=testReportId, case_id=id).order_by('updateTime')
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
#                 secondList.append({
#                     'id': i.id,
#                     'name': i.apiName,
#                     'reportStatus': reportStatus
#                 })
#         else:
#             obj_db_ApiReportItem = db_ApiReportItem.objects.filter(
#                 is_del=0, testReport_id=testReportId, batchItem_id=id).order_by('updateTime')
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
#                 secondList.append({
#                     'id': item_caseId,
#                     'name': caseName,
#                     'reportStatus': reportStatus,
#                 })
#         response['secondList'] = secondList
#         response['statusCode'] = 2000
#     return JsonResponse(response)
#
#
# @cls_Logging.log
# @cls_GlobalDer.foo_isToken
# @require_http_methods(["GET"])
# def load_report_api(request):
#     response = {}
#     try:
#         responseData = json.loads(json.dumps(request.GET))
#         objData = cls_object_maker(responseData)
#         reportItemId = objData.reportItemId
#     except BaseException as e:
#         errorMsg = f"入参错误:{e}"
#         response['errorMsg'] = errorMsg
#         cls_Logging.record_error_info('API', 'Api_TestReport', 'load_report_api', errorMsg)
#     else:
#         getReportApi = cls_ApiReport.get_report_api(reportItemId)
#         if getReportApi['state']:
#             response['statusCode'] = 2000
#             response['TableData'] = getReportApi['dataDict']
#         else:
#             response['errorMsg'] = getReportApi['errorMsg']
#     return JsonResponse(response)
