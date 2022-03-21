from ClassData.Logger import Logging as cls_Logging


class Element(cls_Logging):
    # 元素对比专用-差异对比
    def select_edit_element_dfif(self, oldData, newData):
        strData = ""
        passKeyName = ['proId', 'elementId']  # 忽略不处理的
        keyNameDict = {
            'proId': '所属项目',
            'pageId': '所属页面',
            'funId': '所属功能',
            'elementName': '元素名称',
            'elementType': '元素类型',
            'elementState': '元素状态',
            'elementLocation': '定位列表',

        }
        conversionOld = self.conversion_element_dict(oldData)
        conversionNew = self.conversion_element_dict(newData)
        # diffList = [{'new': {i: conversionNew[i]}, 'old': {i: conversionOld[i]}}
        #             for i in conversionNew.keys() if conversionOld[i] != conversionNew[i]]
        diffList = []
        for i in conversionNew.keys():
            if i not in passKeyName:
                if conversionOld[i] != conversionNew[i]:
                    diffList.append({'new': {i: conversionNew[i]}, 'old': {i: conversionOld[i]}})
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

    # 元素对比专用-重组数据
    def conversion_element_dict(self, dictData):
        # 排除列表
        passKeyName = []

        dicts = {}
        for item in dictData['baseData']:
            if item not in passKeyName:
                dicts[item] = dictData['baseData'][item]
        dicts['elementLocation'] = dictData['elementLocation']
        return dicts
