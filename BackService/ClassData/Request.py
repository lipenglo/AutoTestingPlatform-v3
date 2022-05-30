# -*- coding:utf-8 -*-
from django.conf import settings

# Create your db here.
from Api_TestReport.models import TempExtractData as db_TempExtractData
from GlobalVariable.models import GlobalVariable as db_GlobalVariable
from Api_IntMaintenance.models import ApiBaseData as db_ApiBaseData
from Api_IntMaintenance.models import ApiHeaders as db_ApiHeaders
from Api_IntMaintenance.models import ApiParams as db_ApiParams
from Api_IntMaintenance.models import ApiBody as db_ApiBody
from Api_IntMaintenance.models import ApiExtract as db_ApiExtract
from Api_IntMaintenance.models import ApiValidate as db_ApiValidate
from Api_IntMaintenance.models import ApiOperation as db_ApiOperation
from PageEnvironment.models import PageEnvironment as db_PageEnvironment

from Api_CaseMaintenance.models import CaseBaseData as db_CaseBaseData
from Api_CaseMaintenance.models import CaseTestSet as db_CaseTestSet
from Api_CaseMaintenance.models import CaseApiBase as db_CaseApiBase
from Api_CaseMaintenance.models import CaseApiHeaders as db_CaseApiHeaders
from Api_CaseMaintenance.models import CaseApiParams as db_CaseApiParams
from Api_CaseMaintenance.models import CaseApiBody as db_CaseApiBody
from Api_CaseMaintenance.models import CaseApiExtract as db_CaseApiExtract
from Api_CaseMaintenance.models import CaseApiValidate as db_CaseApiValidate
from Api_CaseMaintenance.models import CaseApiOperation as db_CaseApiOperation

from Api_TimingTask.models import ApiTimingTaskTestSet as db_ApiTimingTaskTestSet
from Api_BatchTask.models import ApiBatchTaskTestSet as db_ApiBatchTaskTestSet
from SystemParams.models import SystemParams as db_SystemParams

# Create reference here.
from ClassData.Common import Common as cls_Common
from ClassData.Logger import Logging as cls_Logging
from ClassData.TestReport import ApiReport
from ClassData.Redis import RedisHandle
from ClassData.FindCommonTable import FindTable
from ClassData.DataBase import DataBase

import requests
import os
import ast
import json

cls_ApiReport = ApiReport()
cls_RedisHandle = RedisHandle()
cls_FindTable = FindTable()
cls_DataBase = DataBase()


class RequstOperation(cls_Logging, cls_Common):
    # 循环请求的数据查询出当前请求的最终是从params，body，中哪种发出
    def for_data_get_requset_params_type(self, paramsTable, bodyTable, raw, jsons):
        requestParamsType = None
        for item_params in paramsTable:
            if item_params.state:
                requestParamsType = 'Params'
                return requestParamsType
        for item_body in bodyTable:
            if item_body.state:
                requestParamsType = 'Body'
                return requestParamsType
        if raw or jsons:
            requestParamsType = 'Body'
            return requestParamsType
        return requestParamsType

    # 转换参数中带有引用的数据
    def conversion_params_import_data(self, onlyCode, proId, requestUrl, requestHeaders, requestData):
        results = {}
        conversionRequestUrl = requestUrl
        conversionHeaders = {}
        conversionRequestData = {}
        if '{{' in requestUrl:
            splitUrl = requestUrl.split('{{')
            globalName = splitUrl[1].replace('}}', '')
            obj_db_GlobalVariable = db_GlobalVariable.objects.filter(
                sysType='API', is_del=0, pid_id=proId, globalName=globalName)
            if obj_db_GlobalVariable.exists():
                conversionRequestUrl = conversionRequestUrl.replace("{{%s}}" % globalName,
                                                                    obj_db_GlobalVariable[0].globalValue)

        for item_headersKey in requestHeaders.keys():
            item_headersValue = requestHeaders[item_headersKey]
            if '{{' in item_headersValue:
                splitHeaders = item_headersValue.split('{{')
                globalName = splitHeaders[1].replace('}}', '')
                # 1.先查找临时存储库
                obj_db_TempExtractData = db_TempExtractData.objects.filter(onlyCode=onlyCode, keys=globalName)
                if obj_db_TempExtractData.exists():
                    conversionHeaders[item_headersKey] = obj_db_TempExtractData[0].values
                else:
                    # 如果临时存储库存在了就不会去找全局库
                    obj_db_GlobalVariable = db_GlobalVariable.objects.filter(
                        sysType='API', is_del=0, pid_id=proId, globalName=globalName)
                    if obj_db_GlobalVariable.exists():
                        conversionHeaders[item_headersKey] = obj_db_GlobalVariable[0].globalValue
                    else:
                        conversionHeaders[item_headersKey] = item_headersValue
            else:
                conversionHeaders[item_headersKey] = item_headersValue

        for item_dataKey in requestData.keys():
            item_dataValue = requestData[item_dataKey]
            if '{{' in item_dataValue:
                splitData = item_dataValue.split('{{')
                globalName = splitData[1].replace('}}', '')
                # 1.先查找临时存储库
                obj_db_TempExtractData = db_TempExtractData.objects.filter(onlyCode=onlyCode, keys=globalName)
                if obj_db_TempExtractData.exists():
                    conversionRequestData[item_dataKey] = obj_db_TempExtractData[0].values
                else:
                    obj_db_GlobalVariable = db_GlobalVariable.objects.filter(
                        sysType='API', is_del=0, pid_id=proId, globalName=globalName)
                    if obj_db_GlobalVariable.exists():
                        conversionRequestData[item_dataKey] = obj_db_GlobalVariable[0].globalValue
                    else:
                        conversionRequestData[item_dataKey] = item_dataValue
            else:
                conversionRequestData[item_dataKey] = item_dataValue

        results['state'] = True
        results['requestUrl'] = conversionRequestUrl
        results['headersData'] = conversionHeaders
        results['requestData'] = conversionRequestData
        return results

    # 转换请求数据为JSON格式
    def conversion_params_to_json(self, headers, params, bodyType, body):
        results = {}
        headersDict = {}
        paramsDict = {}
        bodyDict = {}
        bodyFile = {}
        for item_headers in headers:
            headersDict[item_headers['key']] = item_headers['value']

        for item_params in params:
            paramsDict[item_params['key']] = item_params['value']

        if bodyType == 'form-data':
            for item_body in body:
                if item_body['fileList']:
                    fileList = item_body['fileList'][0]
                    filePath = fileList['url'].replace(settings.NGINX_SERVER, f"{settings.BASE_DIR._str}/_DataFiles/")
                    bodyFile = {'name': item_body['key'], 'url': filePath}
                else:
                    bodyDict[item_body['key']] = item_body['value']
        elif bodyType == 'json':
            bodyDict = json.loads(body)
        elif bodyType == 'raw':
            pass
        else:
            bodyDict = {}

        # results['state'] = True
        results['headersDict'] = headersDict
        results['paramsDict'] = paramsDict
        results['bodyDict'] = bodyDict
        results['bodyFile'] = bodyFile
        return results

    # 转换参数为最后请求的数据
    def conversion_data_to_request_data(self, onlyCode, getRequestData):
        results = {'state': False}
        proId = getRequestData['proId']
        requestUrl = getRequestData['requestUrl']

        requestParamsType = getRequestData['requestParamsType']
        headersData = getRequestData['headersData']
        paramsData = getRequestData['paramsData']
        bodyRequestType = getRequestData['bodyRequestType']
        bodyData = getRequestData['bodyData']

        # 转换请求数据为JSON格式
        conversionToJson = self.conversion_params_to_json(
            headersData, paramsData, bodyRequestType, bodyData)
        # if conversionToJson['state']:
        requestHeaders = conversionToJson['headersDict']
        requestParams = conversionToJson['paramsDict']
        requestBody = conversionToJson['bodyDict']
        requestFile = conversionToJson['bodyFile']
        if requestParamsType == "Body":
            requestData = requestBody
            results['requestData'] = bodyData
        else:
            requestData = requestParams
            results['requestData'] = paramsData
        results['requestFile'] = requestFile

        # 转换参数中带有引用的数据
        conversionImportData = self.conversion_params_import_data(
            onlyCode, proId, requestUrl, requestHeaders, requestData)
        if conversionImportData['state']:
            conversionRequestUrl = conversionImportData['requestUrl']
            conversionHeadersData = conversionImportData['headersData']
            conversionRequestData = conversionImportData['requestData']
            results['state'] = True
            results['conversionRequestUrl'] = conversionRequestUrl
            results['conversionHeadersData'] = conversionHeadersData
            results['conversionRequestData'] = conversionRequestData
        else:
            results['errorMsg'] = conversionImportData['errorMsg']
        # else:
        #     # 这里目前没有可获取到的错误，以后在需求中添加
        #     results['errorMsg'] = ""
        return results

    # 提取并推送给当前执行的用户提取失败的信息
    def request_extract(self,userId, labelName, onlyCode, content, statuscode, extract):
        results = {
            'state': True,
            'errorInfoTable': []
        }
        extractList = []

        if type(content) == dict:
            for item in extract:
                extractKey = item['key']
                extractValue = item['value']
                retValue = ''  # 返回结果值
                if extractKey == 'statuscode':
                    retValue = statuscode
                else:
                    if extractValue[:2] == '$.':
                        params = extractValue[2:]
                        splitParams = params.split('.')
                        if len(splitParams) == 1:
                            combination_content = f'content["{params}"]'
                        else:
                            combination_content = f'content'
                            for item in splitParams:
                                splitItem = item.split('[')
                                combination_content += f'["{splitItem[0]}"]'
                                if len(splitItem) > 1:
                                    combination_content += f'[{splitItem[1][:-1]}]'
                        try:
                            retValue = eval(combination_content)
                        except:
                            # 能进这里的肯定是设置了无法被提取到的参数
                            message = f"提取失败:无法提取到:{combination_content}," \
                                      f"下的返回值,请确认Response返回值中有此数据!"
                            results['errorInfoTable'].append({
                                'createTime': cls_Common.get_date_time(self),
                                'errorName': '提取失败',
                                'errorInfo': message
                            })
                            cls_Logging.print_log(self, 'warning', 'requests_api', message)

                            # region 添加操作信息
                            operationInfo = cls_Logging.record_local_operation_info(
                                self, 'API', 'System', 2, 'Warning',
                                'ClassData', 'Request', 'request_extract', f'{labelName}{message}',
                            )
                            cls_Logging.push_to_user(self, operationInfo, userId)
                            # endregion
                    else:
                        message = f"提取失败:变量名称:{extractKey}," \
                                  f"的提取表达式:{extractValue},首参数不为$,请更改后在重试!"
                        # results['state'] = False
                        # results['errorMsg'] = message
                        results['errorInfoTable'].append({
                            'createTime': cls_Common.get_date_time(self),
                            'errorName': '提取失败',
                            'errorInfo': message
                        })
                        cls_Logging.print_log(self, 'warning', 'requests_api', message)
                        # region 添加操作信息
                        operationInfo = cls_Logging.record_local_operation_info(
                            self, 'API', 'System', 2, 'Warning',
                            'ClassData', 'Request', 'request_extract', f'{labelName}{message}',
                        )
                        cls_Logging.push_to_user(self, operationInfo, userId)
                        # endregion
                        # cls_Logging.record_error_info(self, 'API', 'ClassData', 'request_extract', message)
                if type(retValue) == str:
                    retValueType = 'str'
                elif type(retValue) == list:
                    retValueType = 'list'
                elif type(retValue) == int:
                    retValueType = 'int'
                elif type(retValue) == float:
                    retValueType = 'float'
                elif type(retValue) == bool:
                    retValueType = 'bool'
                else:
                    retValueType = ''
                extractList.append({'key': extractKey, 'value': retValue, 'valueType': retValueType})

                # 保存进临时数据库中
                db_TempExtractData.objects.create(
                    onlyCode=onlyCode, keys=extractKey, values=retValue, valueType=retValueType
                )
        else:
            results['state'] = False
            results['errorMsg'] = f"使用了未录入的提取类型:{type(content)}"
        cls_Logging.print_log(self, 'info', 'request_extract', f'返回提取数据:{extractList}')
        results['extractList'] = extractList
        return results

    # 断言
    def request_validate(self, extractList, validate):
        results = {}
        validateReport = []
        reportState = True
        for item_validate in validate:
            if item_validate['checkName'] and item_validate['validateType'] and item_validate['valueType']:
                checkName = item_validate['checkName']  # 检查值
                validateType = item_validate['validateType']
                valueType = eval(item_validate['valueType'])
                expectedResults = item_validate['expectedResults']  # 预期结果

                if valueType == str:
                    retValueType = "Str"
                elif valueType == int:
                    retValueType = "Int"
                elif valueType == list:
                    retValueType = "List"
                else:
                    retValueType = ""

                for item_extract in extractList:
                    extractKey = item_extract['key']
                    extractValue = item_extract['value']
                    extractValueType = eval(item_extract['valueType'])
                    if extractKey == checkName:
                        if validateType == 'equals':  # ==
                            if valueType == list:
                                try:
                                    list_expected = eval(expectedResults)
                                except BaseException as e:
                                    reportState = False
                                else:
                                    if list_expected == extractValue:
                                        reportState = True
                                    else:
                                        reportState = False
                            else:
                                try:  # 可能会出现 int(str)这种的断言,所以这里要捕获这种错误
                                    if valueType(expectedResults) == extractValueType(extractValue):
                                        reportState = True
                                    else:
                                        reportState = False
                                except:
                                    reportState = False
                        elif validateType == 'contains':  # in
                            if str(expectedResults) in str(extractValue):
                                reportState = True
                            else:
                                reportState = False
                        elif validateType == 'not_equals':  # !=
                            if valueType(expectedResults) != extractValueType(extractValue):
                                reportState = True
                            else:
                                reportState = False

                        if extractValueType == str:
                            extractValueType = "Str"
                        elif extractValueType == int:
                            extractValueType = "Int"
                        elif extractValueType == list:
                            extractValueType = "List"
                        validateReport.append(
                            {'checkName': checkName,
                             'retCheckOut': f'{retValueType}({expectedResults})',  # 预期结果
                             'validateType': validateType,
                             'retExtractorOut': f'{extractValueType}({extractValue})',  # 实际返回
                             'results': reportState}
                        )
                        break
                else:
                    validateReport.append(
                        {'checkName': checkName,
                         'retCheckOut': f'{retValueType}({expectedResults})',  # 预期结果
                         'validateType': validateType,
                         'retExtractorOut': '没有找到当前检查值的可提取数据,请检查提取设置中是否有此检查值!',
                         'results': False}
                    )
        passNum = 0
        failNum = 0
        for i in validateReport:
            if i['results']:
                passNum += 1
            else:
                failNum += 1
        results['state'] = True
        results['validateReport'] = validateReport
        results['reportState'] = False if failNum >= 1 else True
        cls_Logging.print_log(self, 'info', 'request_validate', f'返回断言数据:{validateReport}')
        return results

    # 执行提取和断言操作
    def perform_extract_and_validate(self,labelName, onlyCode, extractData, validateData, requestsApi, userId):
        results = {
            'extractTable': [],
            'assertionTable': [],
            'errorInfoTable': []
        }
        if extractData:  # 如果有提取的数据才会执行断言
            requestExtract = self.request_extract(userId, labelName, onlyCode,
                                                  requestsApi['content'],
                                                  requestsApi['responseCode'],
                                                  extractData)
            if requestExtract['state']:
                results['extractTable'] = requestExtract['extractList']
                results['errorInfoTable'] = requestExtract['errorInfoTable']

                # 断言数据
                requestValidate = self.request_validate(requestExtract['extractList'], validateData)
                if requestValidate['state']:
                    results['assertionTable'] = requestValidate['validateReport']
                    results['reportState'] = 'Pass' if requestValidate['reportState'] else 'Fail'
                    results['state'] = True
                else:
                    results['errorMsg'] = requestValidate['errorMsg']
                    results['state'] = False
                    results['reportState'] = 'Error'
            else:
                results['errorMsg'] = requestExtract['errorMsg']
                results['state'] = False
                results['reportState'] = 'Error'
        else:
            results['reportState'] = 'Pass'
            results['state'] = True
        return results

    # 核心-单-获取请求的数据
    def get_api_data(self, apiId, environmentId):
        results = {}
        obj_db_ApiBaseData = db_ApiBaseData.objects.filter(is_del=0, id=apiId)
        if obj_db_ApiBaseData.exists():
            # region 获取环境URl
            if environmentId:
                obj_db_PageEnvironment = db_PageEnvironment.objects.filter(id=environmentId)
                if obj_db_PageEnvironment.exists():
                    environmentUrl = obj_db_PageEnvironment[0].environmentUrl
                else:
                    environmentUrl = obj_db_ApiBaseData[0].environment.environmentUrl
            else:
                environmentUrl = obj_db_ApiBaseData[0].environment.environmentUrl
            # endregion
            requestUrlRadio = obj_db_ApiBaseData[0].requestUrlRadio
            requestUrl = ast.literal_eval(obj_db_ApiBaseData[0].requestUrl)[f'url{requestUrlRadio}']
            results['proId'] = obj_db_ApiBaseData[0].pid_id
            results['apiName'] = obj_db_ApiBaseData[0].apiName
            results['requestType'] = obj_db_ApiBaseData[0].requestType
            results['requestUrl'] = f"{environmentUrl}{requestUrl}"
            results['environmentUrl'] = environmentUrl
            results['apiUrl'] = requestUrl
            results['requestParamsType'] = obj_db_ApiBaseData[0].requestParamsType  # 最终是以body请求还是以params请求
            # 如果是body请求，还要看他请求的类型来决定以哪种形式发送
            results['bodyRequestType'] = obj_db_ApiBaseData[0].bodyRequestSaveType

            # region 请求数据获取
            # 获取头部数据
            obj_db_ApiHeaders = db_ApiHeaders.objects.filter(is_del=0, apiId_id=apiId).order_by('index')
            results['headersData'] = [{'key': i.key, 'value': i.value} for i in obj_db_ApiHeaders if i.state]

            # 获取params数据
            obj_db_ApiParams = db_ApiParams.objects.filter(is_del=0, apiId_id=apiId).order_by('index')
            results['paramsData'] = [{'key': i.key, 'value': i.value} for i in obj_db_ApiParams if i.state]

            # 获取body数据
            obj_db_ApiBody = db_ApiBody.objects.filter(is_del=0, apiId_id=apiId).order_by('index')
            if results['bodyRequestType'] == 'form-data':
                fileList = [{'key': i.key, 'name': i.filePath.split('/')[-1], 'url': i.filePath}
                            for i in obj_db_ApiBody if i.state and i.filePath]
                results['bodyData'] = [{'key': i.key, 'value': i.value, 'fileList': fileList}
                                       for i in obj_db_ApiBody if i.state]
            elif results['bodyRequestType'] in ('json', 'raw'):
                results['bodyData'] = obj_db_ApiBody[0].value
            else:
                results['bodyData'] = []

            # 获取提取数据
            obj_db_ApiExtract = db_ApiExtract.objects.filter(is_del=0, apiId_id=apiId).order_by('index')
            results['extractData'] = [{'key': i.key, 'value': i.value} for i in obj_db_ApiExtract if i.state]

            # 获取断言数据
            obj_db_ApiValidate = db_ApiValidate.objects.filter(is_del=0, apiId_id=apiId).order_by('index')
            results['validateData'] = [{'checkName': i.checkName, 'validateType': i.validateType,
                                        'valueType': i.valueType, 'expectedResults': i.expectedResults}
                                       for i in obj_db_ApiValidate if i.state]

            # 获取前置数据
            obj_db_ApiOperation = db_ApiOperation.objects.filter(is_del=0, apiId_id=apiId).order_by('index')
            obj_db_PreOperation = obj_db_ApiOperation.filter(location='Pre')
            results['PreOperation'] = [{'operationType': i.operationType,
                                        'methodsName': i.methodsName,
                                        'dataBase': i.dataBaseId,
                                        'sql': i.sql} for i in obj_db_PreOperation if i.state]

            # 获取后置数据
            obj_db_RearOperation = obj_db_ApiOperation.filter(location='Rear')
            results['RearOperation'] = [{'operationType': i.operationType,
                                         'methodsName': i.methodsName,
                                         'dataBase': i.dataBaseId,
                                         'sql': i.sql} for i in obj_db_RearOperation if i.state]

            # endregion
            results['state'] = True
        else:
            results['state'] = False
            results['errorMsg'] = '没有找到当前所发送请求的接口信息'
        return results

    # 核心-单-请求
    def requests_api(self, requestType, requestParamsType, bodyRequestType, url, headers, requestData, requestFile):
        """
        :param requestType: GET/POST
        :param requestParamsType: Params,Body 2种请求参数方式
        param bodyRequestType: none,form-data,json,raw 3种请求参数方式
        :param url: 拼接好的整URL
        :param headers:
        :param requestData:
        :param files:
        :return:执行返回的数据结果
        """
        obj_db_SystemParams = db_SystemParams.objects.filter(keyName='RequestTimeOut')
        if obj_db_SystemParams.exists():
            timeout = int(obj_db_SystemParams[0].value)
        else:
            timeout = 10
            errorMsg = "系统参数:RequestTimeOut,丢失!目前使用默认超时时间:10"
            cls_Logging.print_log(self, 'error', 'requests_api', errorMsg)
            cls_Logging.record_error_info(self, 'API', 'ClassData', 'requests_api', errorMsg)
        r = {}
        results = {
            'state': True
        }
        os.system('echo 3 > /proc/sys/vm/drop_caches')  # 执行前清理缓存
        cls_Logging.print_log(self, 'info', 'requests_api', f'RequestURl:{url}')
        cls_Logging.print_log(self, 'info', 'requests_api', f'requestType:{requestType}')
        cls_Logging.print_log(self, 'info', 'requests_api', f'requestParamsType:{requestParamsType}')
        cls_Logging.print_log(self, 'info', 'requests_api', f'requestParamsType:{bodyRequestType}')
        cls_Logging.print_log(self, 'info', 'requests_api', f'headers:{headers}')
        cls_Logging.print_log(self, 'info', 'requests_api', f'requestData:{requestData}')
        # cls_Logging.print_log(self, 'info', 'requests_api', f'files:{files}')

        try:
            if requestType == "GET":
                r = requests.get(url, headers=headers, params=requestData, timeout=timeout,verify=False)
            elif requestType == "POST":
                files = {requestFile['name']: open(requestFile['url'], 'rb')} if requestFile else {}
                if bodyRequestType in ("form-data", "raw", 'none'):
                    r = requests.post(url, headers=headers, data=requestData, files=files, timeout=timeout,verify=False)
                else:  # json
                    requestData = json.dumps(requestData)
                    r = requests.post(url, headers=headers, data=requestData, timeout=timeout,verify=False)
            else:
                message = f"当前使用了未录入的请求参数:{requestType}"
                results['state'] = False
                results['errorMsg'] = message
                cls_Logging.print_log(self, 'error', 'requests_api', message)
                cls_Logging.record_error_info(self, 'API', 'ClassData', 'requests_api', message)
        except BaseException as e:
            results['state'] = False
            message = f"请求失败:{e}"
            results['content'] = message
            results['errorMsg'] = message
            cls_Logging.print_log(self, 'error', 'requests_api', message)
            # cls_Logging.record_error_info(self, 'API', 'ClassData', 'requests_api', message)
        else:
            text = r.text
            if '<!DOCTYPE html>' in text:
                content = text
            elif '<html>' in text:
                content = text
            elif not text:
                content = text
            else:
                if 'null' in text:
                    text = text.replace('null', "''")
                else:
                    text = r.text
                try:
                    # text = json.dumps(json.loads(text), ensure_ascii=False)
                    text = ast.literal_eval(text)
                    if 'true' in text:
                        text = text.replace('true', 'True')
                    if 'false' in text:
                        text = text.replace('false', 'False')
                    content = ast.literal_eval(text)
                except BaseException as e:
                    content = text
                    cls_Logging.print_log(self, 'error', 'requests_api', f'content:{e}')
            cls_Logging.print_log(self, 'info', 'requests_api', f'content:{content}')
            results['responseCode'] = r.status_code
            results['time'] = round(r.elapsed.total_seconds(), 2)
            responseHeaders = [{'key': item_resHeaders,
                                'value': r.headers[item_resHeaders]}
                               for item_resHeaders in r.headers]
            results['responseHeaders'] = responseHeaders
            results['content'] = content
        return results

    # 核心-执行api
    def execute_api(self, is_test, onlyCode, userId, apiId=None, environmentId=None, requestData=None,
                    testReportId=None, reportItemId=None, labelName=''):
        """
        :param testReportId:
        :param is_test:
        :param onlyCode:
        :param userId:
        :param apiId:
        :param environmentId:
        :param requestData:
        :param reportItemId:
        :param labelName: 是一种标识，用于推送提醒的时候标识是什么
        :return:
        """
        results = {
            'request': {
                'requestType': '',
                'requestUrl': '',
                'environmentUrl': '',
                'apiUrl': '',

                'headersList': [],
                'headersDict': [],
                'requestDataDict': {},
                'requestDataList': [],
            },
            'response': {
                'content': "",  # 返回主体 格式化的数据
                'text': "",  # 返回主体,未格式化
                'responseCode': 0,
                'time': 0,
                'reportState': '',

                'headersList': [],  # 返回头部
                'extractTable': [],  # 提取信息
                'assertionTable': [],  # 断言信息
                'preOperationTable': [],
                'rearOperationTable': [],
                'errorInfoTable:': [],
            },
            'errorMsg': '',
            'state': True,
        }
        if is_test:
            getRequestData = requestData
        else:
            getRequestData = self.get_api_data(apiId, environmentId)

        if getRequestData['state']:
            results['request']['environmentUrl'] = getRequestData['environmentUrl']
            results['request']['apiUrl'] = getRequestData['apiUrl']
            results['request']['requestType'] = getRequestData['requestType']

            # 转换参数为最后请求的数据
            conversionDataToRequestData = self.conversion_data_to_request_data(onlyCode, getRequestData)
            if conversionDataToRequestData['state']:
                conversionRequestUrl = conversionDataToRequestData['conversionRequestUrl']
                conversionHeadersData = conversionDataToRequestData['conversionHeadersData']
                conversionRequestData = conversionDataToRequestData['conversionRequestData']
                requestFile = conversionDataToRequestData['requestFile']

                results['request']['requestUrl'] = conversionRequestUrl
                results['request']['headersList'] = cls_Common.conversion_dict_to_kv(self, conversionHeadersData)
                results['request']['headersDict'] = conversionHeadersData
                results['request']['requestDataDict'] = conversionRequestData
                if requestFile:
                    key = requestFile['name']
                    value = requestFile['url'].split('/')[-1]
                    conversionRequestData[key] = value
                results['request']['requestDataList'] = cls_Common.conversion_dict_to_kv(self, conversionRequestData)

                resultOfExecution = self.request_operation_extract_validate(
                    labelName, onlyCode, getRequestData,
                    conversionRequestUrl,
                    conversionHeadersData,
                    conversionRequestData,
                    requestFile,
                    userId)
                if resultOfExecution['state']:
                    results['response']['responseCode'] = resultOfExecution['responseCode']
                    results['response']['time'] = resultOfExecution['time']
                    results['response']['content'] = resultOfExecution['content']
                    results['response']['text'] = resultOfExecution['text']
                    results['response']['reportState'] = resultOfExecution['reportState']

                    results['response']['responseHeaders'] = resultOfExecution['responseHeaders']
                    results['response']['extractTable'] = resultOfExecution['extractTable']
                    results['response']['assertionTable'] = resultOfExecution['assertionTable']
                    results['response']['preOperationTable'] = resultOfExecution['preOperationTable']
                    results['response']['rearOperationTable'] = resultOfExecution['rearOperationTable']
                    results['response']['errorInfoTable'] = resultOfExecution['errorInfoTable']

                    # 创建3级测试报告
                    if not is_test:
                        cls_ApiReport.create_api_report(reportItemId, results)
                        # region 添加报告版本的警示信息
                        if results['errorMsg']:
                            cls_ApiReport.create_warning_info(
                                testReportId, 'Error', apiId, getRequestData['apiName'], results['errorMsg'], userId)
                        for item_error in results['response']['errorInfoTable']:
                            cls_ApiReport.create_warning_info(
                                testReportId, 'Warning',
                                apiId, getRequestData['apiName'], item_error['errorInfo'], userId)
                        # endregion
                else:
                    results['errorMsg'] = resultOfExecution['errorMsg']
                    results['state'] = False
            else:
                results['errorMsg'] = conversionDataToRequestData['errorMsg']
                results['state'] = False
        else:
            results['errorMsg'] = getRequestData['errorMsg']
            results['state'] = False

        return results

    # 请求-前后操作-提取-断言
    def request_operation_extract_validate(self,labelName, onlyCode, getRequestData,
                                           conversionRequestUrl, conversionHeadersData, conversionRequestData,
                                           requestFile, userId):
        results = {
            'responseCode': 0,
            'time': 0,
            'content': '',
            'text': '',
            'reportState': '',
            'responseHeaders': [],
            'extractTable': [],
            'assertionTable': [],
            'preOperationTable': [],
            'rearOperationTable': [],
            'errorInfoTable': [],
        }
        reportState = []  # 1(前置状态),2(接口运行完成),3(提取和断言),4(后置状态)
        preOperationTable = []
        rearOperationTable = []
        errorInfoTable = []

        requestParamsType = getRequestData['requestParamsType']
        bodyRequestType = getRequestData['bodyRequestType']
        extractData = getRequestData['extractData']
        validateData = getRequestData['validateData']
        preOperationData = getRequestData['PreOperation']
        rearOperationData = getRequestData['RearOperation']
        requestType = results['requestType'] = getRequestData['requestType']

        # region 前置操作
        for item_pre in preOperationData:
            if item_pre['operationType'] == 'Methods':
                callName = item_pre['methodsName']
                import DebugTalk.Data.ApiDebug
                strCmd = f"DebugTalk.Data.ApiDebug.{callName}"
                try:
                    callResults = eval(strCmd)
                    resultsState = True
                    reportState.append('Pass')
                except BaseException as e:
                    callResults = f"{callName} 执行错误:{e}"
                    resultsState = False
                    reportState.append('Error')
                    errorInfoTable.append({
                        'createTime': cls_Common.get_date_time(self),
                        'errorName': '前置操作',
                        'errorInfo': callResults,
                    })
                preOperationTable.append(
                    {'operationType': item_pre['operationType'],  # 操作类型
                     'callName': callName,  # 调用名称
                     'callResults': str(callResults),  # 调用结果
                     'resultsState': resultsState
                     }
                )
            elif item_pre['operationType'] == 'DataBase':
                if type(item_pre['dataBase']) == list:
                    dbId, dbName = item_pre['dataBase']
                else:
                    dbId, dbName = ast.literal_eval(item_pre['dataBase'])
                dataBaseData = cls_FindTable.get_data_base_data(dbId)
                if dataBaseData['state']:
                    dbType = dataBaseData['dbData']['dbType']
                    ip = dataBaseData['dbData']['dataBaseIp']
                    port = dataBaseData['dbData']['port']
                    userName = dataBaseData['dbData']['userName']
                    passWord = dataBaseData['dbData']['passWord']
                    sql = item_pre['sql']
                    executeType = sql.split(' ')[0]
                    executeMysql = cls_DataBase.execute_sql(dbType, executeType, ip, port, userName, passWord, dbName,
                                                            sql)
                    if executeMysql['state']:
                        callResults = f"SQL:{sql}\n" \
                                      f"结果:{executeMysql['resultsData']}"
                        resultsState = True
                    else:
                        callResults = f"数据库:{dbName},SQL:{sql},执行错误:{executeMysql['errorMsg']}"
                        resultsState = False
                        reportState.append('Error')
                        errorInfoTable.append({
                            'createTime': cls_Common.get_date_time(self),
                            'errorName': '前置操作',
                            'errorInfo': callResults,
                        })
                else:
                    callResults = f"数据库:{dbName} 错误:{dataBaseData['errorMsg']}"
                    resultsState = False
                    reportState.append('Error')
                    errorInfoTable.append({
                        'createTime': cls_Common.get_date_time(self),
                        'errorName': '前置操作',
                        'errorInfo': callResults,
                    })
                preOperationTable.append(
                    {'operationType': item_pre['operationType'],  # 操作类型
                     'callName': f"数据库:{dbName}",  # 调用名称
                     'callResults': str(callResults),  # 调用结果
                     'resultsState': resultsState
                     }
                )
            else:
                pass
        # endregion

        # region 发送请求
        requestsApi = self.requests_api(
            requestType, requestParamsType, bodyRequestType,
            conversionRequestUrl, conversionHeadersData, conversionRequestData, requestFile=requestFile)
        if requestsApi['state']:
            results['responseCode'] = requestsApi['responseCode']
            results['time'] = requestsApi['time']
            # 解决中文乱码的问题
            results['content'] = json.dumps(
                requestsApi['content'], sort_keys=True, indent=4, separators=(",", ": "), ensure_ascii=False)
            results['text'] = requestsApi['content']
            results['responseHeaders'] = requestsApi['responseHeaders']
            reportState.append('Pass')

            # 断言及提取
            performExtractAndValidate = self.perform_extract_and_validate(
                labelName, onlyCode, extractData, validateData, requestsApi, userId)
            if performExtractAndValidate['state']:
                for i in performExtractAndValidate['errorInfoTable']:
                    errorInfoTable.append(i)
                results['extractTable'] = performExtractAndValidate['extractTable']
                results['assertionTable'] = performExtractAndValidate['assertionTable']
            else:  # 失败后的结果
                errorInfoTable.append({
                    'createTime': cls_Common.get_date_time(self),
                    'errorName': '提取/断言',
                    'errorInfo': performExtractAndValidate['errorMsg'],
                })
            reportState.append(performExtractAndValidate['reportState'])
            # results['state'] = True
        else:
            # 解决中文乱码的问题
            results['content'] = json.dumps(
                requestsApi['content'], sort_keys=True, indent=4, separators=(",", ": "), ensure_ascii=False)
            results['text'] = requestsApi['content']

            errorInfoTable.append({
                'createTime': cls_Common.get_date_time(self),
                'errorName': '访问接口',
                'errorInfo': requestsApi['errorMsg'],
            })
            reportState.append('Error')
        # endregion

        # region 后置操作
        for item_rear in rearOperationData:
            if item_rear['operationType'] == 'Methods':
                callName = item_rear['methodsName']
                import DebugTalk.Data.ApiDebug
                strCmd = f"DebugTalk.Data.ApiDebug.{callName}"
                try:
                    callResults = eval(strCmd)
                    resultsState = True
                    reportState.append('Pass')
                except BaseException as e:
                    callResults = f"{callName} 执行错误:{e}"
                    resultsState = False
                    reportState.append('Error')
                    errorInfoTable.append({
                        'createTime': cls_Common.get_date_time(self),
                        'errorName': '后置操作',
                        'errorInfo': callResults,
                    })
                rearOperationTable.append(
                    {'operationType': item_rear['operationType'],  # 操作类型
                     'callName': callName,  # 调用名称
                     'callResults': callResults,  # 调用结果
                     'resultsState': resultsState
                     }
                )
            elif item_rear['operationType'] == 'DataBase':
                if type(item_rear['dataBase']) == list:
                    dbId, dbName = item_rear['dataBase']
                else:
                    dbId, dbName = ast.literal_eval(item_rear['dataBase'])
                dataBaseData = cls_FindTable.get_data_base_data(dbId)
                if dataBaseData['state']:
                    dbType = dataBaseData['dbData']['dbType']
                    ip = dataBaseData['dbData']['dataBaseIp']
                    port = dataBaseData['dbData']['port']
                    userName = dataBaseData['dbData']['userName']
                    passWord = dataBaseData['dbData']['passWord']
                    sql = item_rear['sql']
                    executeType = sql.split(' ')[0]
                    executeMysql = cls_DataBase.execute_sql(dbType, executeType, ip, port, userName, passWord, dbName,
                                                            sql)
                    if executeMysql['state']:
                        callResults = f"SQL:{sql}\n" \
                                      f"结果:{executeMysql['resultsData']}"
                        resultsState = True
                    else:
                        callResults = f"数据库:{dbName},SQL:{sql},执行错误:{executeMysql['errorMsg']}"
                        resultsState = False
                        reportState.append('Error')
                        errorInfoTable.append({
                            'createTime': cls_Common.get_date_time(self),
                            'errorName': '后置操作',
                            'errorInfo': callResults,
                        })
                else:
                    callResults = f"数据库:{dbName} 错误:{dataBaseData['errorMsg']}"
                    resultsState = False
                    reportState.append('Error')
                    errorInfoTable.append({
                        'createTime': cls_Common.get_date_time(self),
                        'errorName': '后置操作',
                        'errorInfo': callResults,
                    })
                rearOperationTable.append(
                    {'operationType': item_rear['operationType'],  # 操作类型
                     'callName': f"数据库:{dbName} ",  # 调用名称
                     'callResults': str(callResults),  # 调用结果
                     'resultsState': resultsState
                     }
                )
            else:
                pass
        # endregion

        results['preOperationTable'] = preOperationTable
        results['rearOperationTable'] = rearOperationTable
        results['errorInfoTable'] = errorInfoTable

        if 'Error' in reportState:
            results['reportState'] = 'Error'
        elif 'Fail' in reportState:
            results['reportState'] = 'Fail'
        else:
            results['reportState'] = 'Pass'

        results['state'] = True

        return results

    # 核心-用例-获取请求的数据
    def get_case_data(self, caseId, environmentId):
        results = {
            'caseId': caseId,
            'request': []
        }
        obj_db_CaseBaseData = db_CaseBaseData.objects.filter(is_del=0, id=caseId)
        if obj_db_CaseBaseData.exists():
            # region 获取环境URl
            if environmentId:
                obj_db_PageEnvironment = db_PageEnvironment.objects.filter(id=environmentId)
                if obj_db_PageEnvironment.exists():
                    environmentUrl = obj_db_PageEnvironment[0].environmentUrl
                else:
                    environmentUrl = obj_db_CaseBaseData[0].environmentId.environmentUrl
            else:
                environmentUrl = obj_db_CaseBaseData[0].environmentId.environmentUrl
            results['environmentUrl'] = environmentUrl
            # endregion
            obj_db_CaseTestSet = db_CaseTestSet.objects.filter(is_del=0, caseId_id=caseId).order_by('index')
            for item_testSet in obj_db_CaseTestSet:
                state = True if item_testSet.state == 1 else False
                if state:
                    if item_testSet.testName:
                        testName = f'{item_testSet.apiId.apiName}({item_testSet.testName})'
                    else:
                        testName = item_testSet.apiId.apiName
                    itemApi = {
                        'proId': obj_db_CaseBaseData[0].pid_id,
                        'apiId': item_testSet.apiId_id,
                        'testName': testName,
                        'headersData': [],
                        'paramsData': [],
                        'bodyData': [],
                        'extractData': [],
                        'validateData': [],
                    }
                    synchronous = True if item_testSet.is_synchronous == 1 else False  # 是否开启了同步
                    if synchronous:
                        obj_db_ApiBaseData = db_ApiBaseData.objects.filter(is_del=0, id=item_testSet.apiId_id)
                        if obj_db_ApiBaseData.exists():
                            requestUrlRadio = obj_db_ApiBaseData[0].requestUrlRadio
                            requestUrl = ast.literal_eval(obj_db_ApiBaseData[0].requestUrl)[f'url{requestUrlRadio}']
                            itemApi['requestType'] = obj_db_ApiBaseData[0].requestType
                            itemApi['apiUrl'] = requestUrl
                            itemApi['requestUrl'] = f'{environmentUrl}{requestUrl}'
                            itemApi['requestParamsType'] = obj_db_ApiBaseData[0].requestParamsType
                            itemApi['bodyRequestType'] = obj_db_ApiBaseData[0].bodyRequestSaveType

                            # region 获取头部数据
                            obj_db_ApiHeaders = db_ApiHeaders.objects.filter(
                                is_del=0, apiId_id=item_testSet.apiId_id).order_by('index')
                            for item_headers in obj_db_ApiHeaders:
                                if item_headers.state:
                                    obj_db_CaseApiHeaders = db_CaseApiHeaders.objects.filter(
                                        is_del=0, testSet_id=item_testSet.id, key=item_headers.key)
                                    if obj_db_CaseApiHeaders.exists():
                                        value = obj_db_CaseApiHeaders[0].value
                                    else:
                                        value = None
                                    itemApi['headersData'].append({'key': item_headers.key, 'value': value})
                            # endregion
                            # region 获取params数据
                            obj_db_ApiParams = db_ApiParams.objects.filter(
                                is_del=0, apiId_id=item_testSet.apiId_id).order_by('index')
                            for item_params in obj_db_ApiParams:
                                if item_params.state:
                                    obj_db_CaseApiParams = db_CaseApiParams.objects.filter(
                                        is_del=0, testSet_id=item_testSet.id, key=item_params.key)
                                    if obj_db_CaseApiParams.exists():
                                        value = obj_db_CaseApiParams[0].value
                                    else:
                                        value = None
                                    itemApi['paramsData'].append({'key': item_params.key, 'value': value})
                            # endregion
                            # region 获取body数据
                            obj_db_ApiBody = db_ApiBody.objects.filter(
                                is_del=0, apiId_id=item_testSet.apiId_id).order_by('index')
                            if itemApi['bodyRequestType'] == 'form-data':
                                for item_body in obj_db_ApiBody:
                                    if item_body.state:
                                        obj_db_CaseApiBody = db_CaseApiBody.objects.filter(
                                            is_del=0, testSet_id=item_testSet.id, key=item_body.key)

                                        if obj_db_CaseApiBody.exists():
                                            value = obj_db_CaseApiBody[0].value
                                        else:
                                            value = None
                                        fileList = [{'key': i.key, 'name': i.filePath.split('/')[-1], 'url': i.filePath}
                                                    for i in obj_db_CaseApiBody if i.state and i.filePath]
                                        itemApi['bodyData'].append(
                                            {'key': item_body.key, 'value': value, 'fileList': fileList})

                            elif itemApi['bodyRequestType'] in ('json', 'raw'):
                                obj_db_CaseApiBody = db_CaseApiBody.objects.filter(is_del=0, testSet_id=item_testSet.id)
                                if obj_db_CaseApiBody.exists():
                                    value = obj_db_CaseApiBody[0].value
                                else:
                                    value = None
                                itemApi['bodyData'] = value
                            else:
                                itemApi['bodyData'] = []
                            # endregion
                        else:
                            results['state'] = False
                            results['errorMsg'] = '当前选择的用例基础数据缺失!'
                    else:
                        obj_db_CaseApiBase = db_CaseApiBase.objects.filter(is_del=0, testSet_id=item_testSet.id)
                        if obj_db_CaseApiBase.exists():
                            itemApi['requestType'] = obj_db_CaseApiBase[0].requestType
                            itemApi['requestUrl'] = f'{environmentUrl}{obj_db_CaseApiBase[0].requestUrl}'
                            itemApi['apiUrl'] = obj_db_CaseApiBase[0].requestUrl
                            itemApi['requestParamsType'] = obj_db_CaseApiBase[0].requestParamsType
                            itemApi['bodyRequestType'] = obj_db_CaseApiBase[0].bodyRequestSaveType

                            # region 获取头部数据
                            obj_db_CaseApiHeaders = db_CaseApiHeaders.objects.filter(
                                is_del=0, testSet_id=item_testSet.id).order_by('index')
                            itemApi['headersData'] = [{'key': i.key, 'value': i.value}
                                                      for i in obj_db_CaseApiHeaders if i.state]
                            # endregion
                            # region 获取params数据
                            obj_db_CaseApiParams = db_CaseApiParams.objects.filter(
                                is_del=0, testSet_id=item_testSet.id).order_by('index')
                            itemApi['paramsData'] = [{'key': i.key, 'value': i.value}
                                                     for i in obj_db_CaseApiParams if i.state]
                            # endregion
                            # region 获取body数据
                            obj_db_CaseApiBody = db_CaseApiBody.objects.filter(
                                is_del=0, testSet_id=item_testSet.id).order_by('index')
                            if itemApi['bodyRequestType'] == 'form-data':
                                fileList = [{'key': i.key, 'name': i.filePath.split('/')[-1], 'url': i.filePath}
                                            for i in obj_db_CaseApiBody if i.state and i.filePath]
                                itemApi['bodyData'] = [{'key': i.key, 'value': i.value, 'fileList': fileList}
                                                       for i in obj_db_CaseApiBody if i.state]
                            elif itemApi['bodyRequestType'] in ('json', 'raw'):
                                itemApi['bodyData'] = obj_db_CaseApiBody[0].value
                            else:
                                itemApi['bodyData'] = []
                            # endregion
                        else:
                            results['state'] = False
                            results['errorMsg'] = '当前选择的用例基础数据缺失!'
                    # region 获取提取数据
                    obj_db_CaseApiExtract = db_CaseApiExtract.objects.filter(
                        is_del=0, testSet_id=item_testSet.id).order_by('index')
                    itemApi['extractData'] = [{'key': i.key, 'value': i.value}
                                              for i in obj_db_CaseApiExtract if i.state]
                    # endregion
                    # region 获取断言数据
                    obj_db_CaseApiValidate = db_CaseApiValidate.objects.filter(
                        is_del=0, testSet_id=item_testSet.id).order_by('index')
                    itemApi['validateData'] = [{'checkName': i.checkName, 'validateType': i.validateType,
                                                'valueType': i.valueType, 'expectedResults': i.expectedResults}
                                               for i in obj_db_CaseApiValidate if i.state]
                    # endregion
                    # region 获取前置数据
                    obj_db_CaseApiOperation = db_CaseApiOperation.objects.filter(
                        is_del=0, testSet_id=item_testSet.id).order_by('index')
                    obj_db_PreOperation = obj_db_CaseApiOperation.filter(location='Pre')
                    itemApi['PreOperation'] = [{'operationType': i.operationType,
                                                'methodsName': i.methodsName,
                                                'dataBase': i.dataBaseId,
                                                'sql': i.sql} for i in obj_db_PreOperation if i.state]

                    # 获取后置数据
                    obj_db_RearOperation = obj_db_CaseApiOperation.filter(location='Rear')
                    itemApi['RearOperation'] = [{'operationType': i.operationType,
                                                 'methodsName': i.methodsName,
                                                 'dataBase': i.dataBaseId,
                                                 'sql': i.sql} for i in obj_db_RearOperation if i.state]
                    # endregion
                    results['request'].append(itemApi)
            results['state'] = True
        else:
            results['state'] = False
            results['errorMsg'] = '当前选择的用例不存在,请刷新后在重新尝试!'
        return results

    # 核心-用例执行
    def execute_case(self, remindLabel, redisKey, testReportId, caseId, environmentId, userId, reportTaskItemId=None):
        results = {
            'state': True,
            'itemResults': []
        }
        redisData = {}
        getCaseData = self.get_case_data(caseId, environmentId)
        if getCaseData['state']:
            environmentUrl = getCaseData['environmentUrl']
            for item_index, item_request in enumerate(getCaseData['request'], 1):
                itemResults = {
                    'request': {
                        'requestType': '',
                        'requestUrl': '',
                        'environmentUrl': '',
                        'apiUrl': '',

                        'headersList': [],
                        'headersDict': [],
                        'requestData': {},
                    },
                    'response': {
                        'content': "",  # 返回主体 格式化的数据
                        'text': "",  # 返回主体,未格式化
                        'responseCode': '',
                        'time': '',
                        'reportState': '',

                        'headersList': [],  # 返回头部
                        'extractTable': [],  # 提取信息
                        'assertionTable': [],  # 断言信息
                        'preOperationTable': [],
                        'rearOperationTable': [],
                        'errorInfoTable:': [],
                    },
                    'errorMsg': ''
                }
                # 创建2级测试报告
                createReportItems = cls_ApiReport.create_report_items(
                    testReportId, item_request['apiId'], item_request['testName'],
                    caseId=caseId, reportTaskItemId=reportTaskItemId)
                if createReportItems['state']:
                    reportItemId = createReportItems['reportItemId']
                    itemResults['request']['environmentUrl'] = environmentUrl
                    itemResults['request']['apiUrl'] = item_request['apiUrl']
                    itemResults['request']['headersList'] = item_request['headersData']
                    itemResults['request']['requestType'] = item_request['requestType']

                    # 转换参数为最后请求的数据
                    conversionDataToRequestData = self.conversion_data_to_request_data(redisKey, item_request)
                    if conversionDataToRequestData['state']:
                        conversionRequestUrl = conversionDataToRequestData['conversionRequestUrl']
                        conversionHeadersData = conversionDataToRequestData['conversionHeadersData']
                        conversionRequestData = conversionDataToRequestData['conversionRequestData']
                        requestFile = conversionDataToRequestData['requestFile']

                        itemResults['request']['requestUrl'] = conversionRequestUrl
                        itemResults['request']['headersDict'] = conversionHeadersData
                        itemResults['request']['requestDataDict'] = conversionRequestData
                        if requestFile:
                            key = requestFile['name']
                            value = requestFile['url'].split('/')[-1]
                            itemResults['request']['requestDataDict'][key] = value
                        itemResults['request']['requestDataList'] = conversionDataToRequestData['requestData']
                        resultOfExecution = self.request_operation_extract_validate(
                            f"{remindLabel}【接口:{item_request['testName']}】", redisKey, item_request,
                            conversionRequestUrl,conversionHeadersData,conversionRequestData,
                            requestFile,
                            userId)
                        if resultOfExecution['state']:
                            itemResults['response']['responseCode'] = resultOfExecution['responseCode']
                            itemResults['response']['time'] = resultOfExecution['time']
                            itemResults['response']['content'] = resultOfExecution['content']
                            itemResults['response']['text'] = resultOfExecution['text']
                            itemResults['response']['reportState'] = resultOfExecution['reportState']

                            itemResults['response']['responseHeaders'] = resultOfExecution['responseHeaders']
                            itemResults['response']['extractTable'] = resultOfExecution['extractTable']
                            itemResults['response']['assertionTable'] = resultOfExecution['assertionTable']
                            itemResults['response']['preOperationTable'] = resultOfExecution['preOperationTable']
                            itemResults['response']['rearOperationTable'] = resultOfExecution['rearOperationTable']
                            itemResults['response']['errorInfoTable'] = resultOfExecution['errorInfoTable']
                            # 创建3级测试报告
                            cls_ApiReport.create_api_report(reportItemId, itemResults)
                            # region 创建警示信息
                            if itemResults['errorMsg']:
                                cls_ApiReport.create_warning_info(
                                    testReportId, 'Error', item_request['apiId'], item_request['testName'],
                                    itemResults['errorMsg'], userId)
                            for item_error in itemResults['response']['errorInfoTable']:
                                cls_ApiReport.create_warning_info(
                                    testReportId, 'Warning',
                                    item_request['apiId'], item_request['testName'], item_error['errorInfo'], userId)
                            # endregion
                            # 更新2级测试报告
                            cls_ApiReport.update_report_items(testReportId, reportItemId)
                            # region 创建Redis 数据
                            getLiftData = cls_ApiReport.get_report_top_data(testReportId)
                            if getLiftData['state']:
                                passTotal = getLiftData['topData']['passTotal']
                                failTotal = getLiftData['topData']['failTotal']
                                errorTotal = getLiftData['topData']['errorTotal']
                                failedTotal = getLiftData['topData']['failedTotal']
                                passRate = getLiftData['topData']['passRate']

                                runningTime = getLiftData['topData']['runningTime']
                                prePassTotal = getLiftData['topData']['prePassTotal']
                                rearPassTotal = getLiftData['topData']['rearPassTotal']
                                assertionsPassTotal = getLiftData['topData']['assertionsPassTotal']
                                extractPassTotal = getLiftData['topData']['extractPassTotal']
                            else:
                                passTotal = 0
                                failTotal = 0
                                errorTotal = 0
                                failedTotal = 0
                                passRate = 0

                                runningTime = 0
                                prePassTotal = 0
                                rearPassTotal = 0
                                assertionsPassTotal = 0
                                extractPassTotal = 0
                            redisData = {
                                'topData': {
                                    'leftData': {
                                        'passTotal': passTotal,
                                        'failTotal': failTotal,
                                        'errorTotal': errorTotal,
                                        'failedTotal': failedTotal,
                                        'passRate': passRate,
                                    },
                                    'rightData': {
                                        'runningTime': runningTime,
                                        'prePassTotal': prePassTotal,
                                        'rearPassTotal': rearPassTotal,
                                        'extractPassTotal': extractPassTotal,
                                        'assertionsPassTotal': assertionsPassTotal,
                                    },
                                },
                                'tableData': {
                                    'index': item_index,
                                    'testName': item_request['testName'],
                                    'requestType': item_request['requestType'],
                                    'apiUrl': item_request['apiUrl'],
                                    'code': resultOfExecution['responseCode'],
                                    'time': resultOfExecution['time'],
                                    'reportState': resultOfExecution['reportState'],
                                    'details': {
                                        'requestUrl': conversionRequestUrl,
                                        'requestType': item_request['requestType'],
                                        'code': resultOfExecution['responseCode'],
                                        'time': resultOfExecution['time'],
                                        'reportState': resultOfExecution['reportState'],
                                        'originalUrl': item_request['apiUrl'],
                                        'headersTableData': cls_Common.conversion_dict_to_kv(
                                            self, conversionHeadersData),
                                        'requestDataTableData': cls_Common.conversion_dict_to_kv(
                                            self, conversionRequestData),
                                        # 'requestDataTableData': conversionDataToRequestData['requestData'],
                                        'responseText': resultOfExecution['content'],
                                        'responseHeadersTableData': resultOfExecution['responseHeaders'],
                                        'extractTableData': resultOfExecution['extractTable'],
                                        'assertionTableData': resultOfExecution['assertionTable'],
                                        'preOperationTableData': resultOfExecution['preOperationTable'],
                                        'rearOperationTableData': resultOfExecution['rearOperationTable'],
                                        'errorInfoTableData': resultOfExecution['errorInfoTable'],

                                    }
                                }
                            }
                            # endregion
                        else:
                            itemResults['errorMsg'] = resultOfExecution['errorMsg']
                            # results['state'] = False
                    else:
                        itemResults['errorMsg'] = conversionDataToRequestData['errorMsg']
                        # results['state'] = False
                    # 添加Redis到
                    cls_RedisHandle.witer_type_list(redisKey, redisData)
                    results['itemResults'].append(itemResults)
                else:
                    results['errorMsg'] = createReportItems['errorMsg']
                    results['state'] = False
                    break
                    # return results
        else:
            results['errorMsg'] = getCaseData['errorMsg']
            results['state'] = False
        return results

    # 核心-定时任务执行
    def excute_task(self, testReportId, taskId, label, environmentId, userId, reportTaskItemId=None):
        results = {
            'state': True,
            'itemResults': []
        }
        obj_db_ApiTimingTaskTestSet = db_ApiTimingTaskTestSet.objects.filter(
            is_del=0, timingTask_id=taskId).order_by('index')
        for item_taskTestSet in obj_db_ApiTimingTaskTestSet:
            redisKey = cls_Common.generate_only_code(self)  # 1个用例1个key
            caseText = f"【用例:{item_taskTestSet.case.caseName}】>"
            remindLabel = label + caseText
            caseId = item_taskTestSet.case_id
            executeCase = self.execute_case(
                remindLabel, redisKey, testReportId, caseId, environmentId, userId, reportTaskItemId=reportTaskItemId)
            if executeCase['state']:
                results['itemResults'].append(executeCase['itemResults'])
            else:
                results['errorMsg'] = executeCase['errorMsg']
                break
        return results

    # 核心-批量任务执行
    def excute_batch(self, testReportId, batchId, label, userId):
        results = {
            'state': True,
            'itemResults': []
        }
        obj_db_ApiBatchTaskTestSet = db_ApiBatchTaskTestSet.objects.filter(
            is_del=0, batchTask_id=batchId).order_by('index')
        for item_task in obj_db_ApiBatchTaskTestSet:
            createReportTaskItems = cls_ApiReport.create_report_task_items(
                testReportId, item_task.task_id, item_task.task.taskName)
            if createReportTaskItems['state']:
                taskText = f"定时任务:{item_task.task.taskName}>:"
                label = label + taskText
                environmentId = item_task.task.environment_id
                reportTaskItemId = createReportTaskItems['reportTaskItemId']
                excuteTask = self.excute_task(
                    testReportId, item_task.task_id, label, environmentId, userId, reportTaskItemId=reportTaskItemId)
                if excuteTask['state']:
                    results['itemResults'].append(excuteTask['itemResults'])
                else:
                    results['errorMsg'] = excuteTask['errorMsg']
                    break
            else:
                results['errorMsg'] = createReportTaskItems['errorMsg']
                break
            # 更新2级的批量任务报告
            cls_ApiReport.update_report_task_items(testReportId)
        return results

    #  region 接口差异的对比 专属
    def conversion_api_dict(self, dictData):
        # 排除列表
        passKeyName = ['assignedUserId', 'pushTo']

        dicts = {}
        for item in dictData['BasicInfo']:
            if item not in passKeyName:
                dicts[item] = dictData['BasicInfo'][item]

        for item in dictData['ApiInfo']:
            if item not in passKeyName:
                if item == 'request':
                    for item_quest in dictData['ApiInfo']['request']:
                        if item_quest == 'body':
                            for item_body in dictData['ApiInfo']['request']['body']:
                                dicts[item_body] = dictData['ApiInfo']['request']['body'][item_body]
                        else:
                            dicts[item_quest] = dictData['ApiInfo']['request'][item_quest]
                else:
                    dicts[item] = dictData['ApiInfo'][item]
        return dicts

    def api_edit_dfif(self, oldData, newData):
        strData = ""
        passKeyName = ['deleteFileList']  # 忽略不处理的
        keyNameDict = {
            'pageId': '所属页面',
            'funId': '所属功能',
            'apiName': '接口名称',
            'environmentId': '页面环境',
            'apiState': '接口状态',
            'requestType': '请求类型',
            'requestUrlRadio': '备选URL',
            'requestUrl': '请求地址',
            'headers': 'headers参数',
            'params': 'params参数',
            'requestSaveType': 'body请求类型',
            'formData': 'bodyFormData请求参数',
            'raw': 'bodyRaw请求参数',
            'json': 'bodyJson请求参数',
            'extract': '提取参数',
            'validate': '断言参数',
            'preOperation': '前置操作参数',
            'rearOperation': '后置操作参数',
        }
        conversionOld = self.conversion_api_dict(oldData)
        conversionNew = self.conversion_api_dict(newData)
        # diffList = [{'new': {i: conversionNew[i]}, 'old': {i: conversionOld[i]}}
        #             for i in conversionNew.keys() if conversionOld[i] != conversionNew[i]]
        diffList = []
        for i in conversionNew.keys():
            if i not in passKeyName:
                if conversionOld[i] != conversionNew[i]:
                    diffList.append({'new': {i: conversionNew[i]}, 'old': {i: conversionOld[i]}})
        # if diffList:
        for item in diffList:
            newData = item['new']
            oldData = item['old']
            key = list(newData.keys())[0]
            newValue = newData[key]
            oldValue = oldData[key]
            if type(oldValue) == list:
                strData += f'<b>【{keyNameDict[key]}修改前】</b>:\n'
                for i in oldValue:
                    strData += f'{i}\n'
            else:
                strData += f'<b>【{keyNameDict[key]}修改前】</b>:{oldValue}\n'

            if type(newValue) == list:
                strData += f'<b>\n【{keyNameDict[key]}修改为】</b>:\n'
                for i in newValue:
                    strData += f'{i}\n'
            else:
                strData += f'<b>【{keyNameDict[key]}修改为】</b>:{newValue}\n'
            strData += '\n---------------------------------------------------------------------------------------\n'
            # strData += f'【{keyNameDict[key]}修改为】:{newValue}\n\n'
        return strData
    # endregion
