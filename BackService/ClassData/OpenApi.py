from ClassData.Logger import Logging as cls_Logging
from ClassData.FileOperations import FileOperations

import ast

cls_FileOperations = FileOperations()


class Swagger(cls_Logging):
    # 处理JSON文件转换为列表类型
    def analysisJsonData(self, filePath):
        results = {}
        readFile = cls_FileOperations.read_file(filePath)  # 读取文件
        if readFile['state']:
            jsonStr = readFile['data']
            try:
                jsonStr = ast.literal_eval(jsonStr.replace('true', "True").replace('false', "False"))
            except BaseException as e:
                results['state'] = False
                results['errorMsg'] = f'解析文件失败:{e}'
            else:
                pathJson = jsonStr['paths']

                jsonTable = self.swagger3_to_table(pathJson)
                if jsonTable['state']:
                    results['state'] = True
                    results['dataTable'] = jsonTable['dataTable']
                else:
                    results['state'] = False
                    results['errorMsg'] = jsonTable['errorMsg']
        else:
            results['state'] = False
            results['errorMsg'] = readFile['errorMsg']
        return results

    # swagger3 模式的列表
    def swagger3_to_table(self, jsonData):
        results = {}
        dataTable = []
        passType = ['delete', 'put']
        try:
            for i in jsonData:
                requestUrl = i
                for k, v in jsonData[i].items():
                    headersData = []  # 头部请求
                    requestData = []  # 主体请求
                    apiName = v['summary']
                    requestType = k
                    requestStyleTxt = 'form-data'

                    # region 请求参数类型 Params,body 目前只做2个
                    if requestType == 'get':
                        requestParamsType = 'Params'
                    else:
                        requestParamsType = 'Body'
                    # endregion
                    if requestType not in passType:
                        parameters = v['parameters']
                        requestBody = v['requestBody'] if 'requestBody' in v else []

                        # region 筛选出header 参数
                        for item_header in parameters:
                            if item_header['in'] == 'header':
                                key = item_header['name']  # key值
                                value = item_header[
                                    'example'] if 'example' in item_header else None  # Swagger 所有的VALUE值都是None
                                remarks = item_header['description'] if 'description' in item_header else None  # 描述
                                headersData.append({'key': key, 'value': value, 'remarks': remarks})
                        # endregion
                        # region 筛选出主体 参数
                        if requestType == "get":
                            for item_params in parameters:
                                if item_params['in'] != 'header':
                                    key = item_params['name']  # key值
                                    value = item_params[
                                        'example'] if 'example' in item_params else None  # Swagger 所有的VALUE值都是None
                                    remarks = item_params['description'] if 'description' in item_params else None  # 描述

                                    requestData.append({'key': key, 'value': value, 'remarks': remarks})
                        else:
                            requestStyle = None
                            content = requestBody['content']
                            for item_body in content:
                                requestStyle = item_body
                            if requestStyle == "multipart/form-data":
                                requestStyleTxt = 'form-data'
                            elif requestStyle == "application/x-www-form-urlencoded":
                                requestStyleTxt = 'x-www-form-urlencoded'
                            elif requestStyle == "application/json":
                                requestStyleTxt = 'json'
                            elif requestStyle == "text/plain":
                                requestStyleTxt = 'raw'
                            else:
                                requestStyleTxt = 'none'

                            if requestStyle in ["multipart/form-data", "application/x-www-form-urlencoded"]:
                                properties = content[requestStyle]['schema']['properties']  # body的请求参数
                                for item_body in properties:
                                    # 这2种form-data类型这样获取
                                    key = item_body  # key值
                                    value = properties[item_body]['example'] if 'example' in properties[
                                        item_body] else None  # Swagger 所有的VALUE值都是None
                                    remarks = properties[item_body]['description'] if 'description' in properties[
                                        item_body] else None  # 描述

                                    requestData.append({'key': key, 'value': value, 'remarks': remarks})
                            else:
                                # 一般到这里的都是JSON格式的了
                                value = content[requestStyle]['example']  # body的请求参数
                                requestData = {'key': None, 'value': value, 'remarks': None}
                        # endregion
                        dataTable.append({
                            'apiName': apiName,
                            'requestUrl': requestUrl,
                            'requestType': requestType.upper(),
                            'requestParamsType': requestParamsType,
                            'requestStyle': requestStyleTxt,
                            'request': {
                                'headersDataList': headersData,
                                'requestDataList': requestData,
                            }
                        })
        except BaseException as e:
            results['state'] = False
            results['errorMsg'] = f"文件解析失败:{e}"
        else:
            results['state'] = True
            results['dataTable'] = dataTable
        return results

    # 转换swagger列表的数据为API通用的列表
    def conversion_swagger_table_to_api_table(self, proId, pageId, funId, environmentId, roleId, userId, swaggerTable):
        results = {}
        saveList = []
        try:
            for item_api in swaggerTable:
                if item_api.requestStyle == 'x-www-form-urlencoded':
                    requestStyle = 'form-data'
                else:
                    requestStyle = item_api.requestStyle
                # region headers
                headers = []
                for index, item_headers in enumerate(item_api.request.headersDataList, 0):
                    headers.append({
                        'index': index,
                        'key': item_headers.key,
                        'value': item_headers.value,
                        'remarks': item_headers.remarks,
                        'state': 1,
                    })
                # endregion
                # region params/body
                params = []
                bodyRormData = []
                raw = ''
                jsonStr = ''
                if item_api.requestParamsType == 'Params':
                    for index, item_params in enumerate(item_api.request.requestDataList, 0):
                        params.append({
                            'index': index,
                            'key': item_params.key,
                            'value': item_params.value,
                            'remarks': item_params.remarks,
                            'state': 1,
                        })
                else:
                    if item_api.requestStyle in ['form-data', 'x-www-form-urlencoded']:
                        for index, item_body in enumerate(item_api.request.requestDataList, 0):
                            bodyRormData.append({
                                'index': index,
                                'key': item_body.key,
                                'value': item_body.value,
                                'remarks': item_body.remarks,
                                'state': 1,
                            })
                    elif requestStyle == 'json':
                        jsonStr = {'index': 0,
                                   'key': None,
                                   'value': item_api.request.requestDataList.value._object_maker__data,
                                   'remarks': None,
                                   'state': 1}
                    else:
                        raw = {'index': 0,
                               'key': None,
                               'value': item_api.request.requestDataList.value,
                               'remarks': None,
                               'state': 1}
                # endregion
                saveList.append({
                    'BasicInfo': {
                        'proId': proId,
                        'pageId': pageId,
                        'funId': funId,
                        'apiName': item_api.apiName,
                        'environmentId': environmentId,
                        'apiState': 'Completed',
                        'assignedUserId': userId,
                        'pushTo': [[roleId, userId]]
                    },
                    'ApiInfo': {
                        'requestParamsType': item_api.requestParamsType,
                        'requestType': item_api.requestType,
                        'requestUrlRadio': 1,
                        'requestUrl': {
                            'url1': item_api.requestUrl,
                            'url2': '',
                            'url3': '',
                        },
                        'request': {
                            'headers': headers,
                            'params': params,
                            'body': {
                                'requestSaveType': requestStyle,
                                'formData': bodyRormData,
                                'raw': raw,
                                'json':jsonStr,
                            },
                        },
                    },
                })
        except BaseException as e:
            results['state'] = False
            results['errorMsg'] = f'数据转换失败:{e}'
        else:
            results['state'] = True
            results['tableData'] = saveList
        return results
