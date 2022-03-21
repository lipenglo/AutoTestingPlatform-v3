from django.db import models


# Create your models here.
class CaseBaseData(models.Model):
    pid = models.ForeignKey(to='ProjectManagement.ProManagement', to_field='id', on_delete=models.CASCADE)
    page = models.ForeignKey(to='PageManagement.PageManagement', to_field='id', on_delete=models.CASCADE)
    fun = models.ForeignKey(to='FunManagement.FunManagement', to_field='id', on_delete=models.CASCADE)
    # 页面环境
    environmentId = models.ForeignKey(to='PageEnvironment.PageEnvironment', to_field='id', on_delete=models.CASCADE)
    testType = models.CharField("测试类型(UnitTest:单元,HybridTest:混合)", max_length=20, null=False)
    label = models.CharField("用例标签(CommonCase:普通 ReturnCase:BUG回归)", max_length=20, null=False)
    priority = models.CharField("优先级(P0-P3)", max_length=10, null=False)
    caseName = models.CharField('用例名称', max_length=50, null=False)
    caseState = models.CharField('用例状态(InDev:研发中,Completed:已完成,Discard:弃用)', max_length=10, null=False)
    createTime = models.DateTimeField('创建时间', auto_now=True)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    cuid = models.IntegerField("创建者用户", null=False)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
    onlyCode = models.CharField('历史记录唯一码,新增的时候会创建1个', max_length=100, null=False)


class CaseTestSet(models.Model):  # 用例的测试集
    caseId = models.ForeignKey(to='CaseBaseData', to_field='id', on_delete=models.CASCADE)
    index = models.IntegerField("排序", null=False)
    apiId = models.ForeignKey(to='Api_IntMaintenance.ApiBaseData', to_field='id', on_delete=models.CASCADE)
    # 因为同1用例下出现多个相同的接口,和上面一个Id不等时取这个
    pluralIntId = models.CharField("多相同接口时用-1，-2来区别,只用编辑读取中用到此id", max_length=50, null=True)
    testName = models.CharField("测试名称", max_length=50, null=True)
    is_synchronous = models.IntegerField("是否开启同步(1:开启,0:不开启)", null=False)
    state = models.IntegerField("是否启用(1:启用,0:禁用)", null=False)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
    onlyCode = models.CharField('历史记录唯一码,新增的时候会创建1个', max_length=100, null=False)


class CaseApiBase(models.Model):
    testSet = models.ForeignKey(to='CaseTestSet', to_field='id', on_delete=models.CASCADE)
    requestType = models.CharField('请求类型(GET/POST)', max_length=50, null=True)
    requestUrl = models.CharField('请求地址', max_length=500, null=True)
    requestParamsType = models.CharField('请求参数类型(Params、Body)', max_length=50, null=True)
    bodyRequestSaveType = models.CharField('body数据保存类型(none,form-data,json,raw)', max_length=10, null=True)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
    onlyCode = models.CharField('历史记录唯一码,新增的时候会创建1个', max_length=100, null=False)


class CaseApiHeaders(models.Model):  # 头部参数
    testSet = models.ForeignKey(to='CaseTestSet', to_field='id', on_delete=models.CASCADE)
    index = models.IntegerField("数据排序", null=False)
    key = models.CharField('key', max_length=100, null=True)
    value = models.TextField('value', null=True)
    remarks = models.TextField('备注', null=True)
    state = models.IntegerField("是否启用(0:禁用,1:启用)", null=False)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
    updateTime = models.DateTimeField('创建时间', auto_now=True)
    onlyCode = models.CharField('历史记录唯一码,新增的时候会创建1个', max_length=100, null=False)


class CaseApiParams(models.Model):
    testSet = models.ForeignKey(to='CaseTestSet', to_field='id', on_delete=models.CASCADE)
    index = models.IntegerField("数据排序", null=False)
    key = models.CharField('key', max_length=100, null=True)
    value = models.TextField('value', null=True)
    remarks = models.TextField('备注', null=True)
    state = models.IntegerField("是否启用(0:禁用,1:启用)", null=False)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
    updateTime = models.DateTimeField('创建时间', auto_now=True)
    onlyCode = models.CharField('历史记录唯一码,新增的时候会创建1个', max_length=100, null=False)


class CaseApiBody(models.Model):
    testSet = models.ForeignKey(to='CaseTestSet', to_field='id', on_delete=models.CASCADE)
    index = models.IntegerField("数据排序", null=False)
    key = models.CharField('key', max_length=100, null=True)
    paramsType = models.CharField('入参类型(Text,File)', max_length=10, null=False)
    value = models.TextField('value/Raw参数/file', null=True)
    filePath = models.TextField('文件保存地址', null=True)
    # fileMD5 = models.TextField('用于判断这个文件有没有被修改', null=True)
    remarks = models.TextField('备注', null=True)
    state = models.IntegerField("是否启用(0:禁用,1:启用)", null=False)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
    updateTime = models.DateTimeField('创建时间', auto_now=True)
    onlyCode = models.CharField('历史记录唯一码,新增的时候会创建1个', max_length=100, null=False)


class CaseApiExtract(models.Model):  # 提取
    testSet = models.ForeignKey(to='CaseTestSet', to_field='id', on_delete=models.CASCADE)
    index = models.IntegerField("数据排序", null=False)
    key = models.CharField('key', max_length=100, null=True)
    value = models.TextField('value', null=True)
    remarks = models.TextField('备注', null=True)
    state = models.IntegerField("是否启用(0:禁用,1:启用)", null=False)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
    updateTime = models.DateTimeField('创建时间', auto_now=True)
    onlyCode = models.CharField('历史记录唯一码,新增的时候会创建1个', max_length=100, null=False)


class CaseApiValidate(models.Model):  # 断言参数
    testSet = models.ForeignKey(to='CaseTestSet', to_field='id', on_delete=models.CASCADE)
    index = models.IntegerField("数据排序", null=False)
    checkName = models.CharField('检查值', max_length=100, null=False)
    validateType = models.CharField('断言类型', max_length=50, null=False)
    valueType = models.CharField('断言值类型', max_length=50, null=False)
    expectedResults = models.TextField('预期结果', null=False)
    remarks = models.TextField('备注', null=True)
    state = models.IntegerField("是否启用(0:禁用,1:启用)", null=False)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
    updateTime = models.DateTimeField('创建时间', auto_now=True)
    onlyCode = models.CharField('历史记录唯一码,新增的时候会创建1个', max_length=100, null=False)


class CaseApiOperation(models.Model):  # 前后置操作
    testSet = models.ForeignKey(to='CaseTestSet', to_field='id', on_delete=models.CASCADE)
    index = models.IntegerField("数据排序", null=False)
    location = models.CharField('位置 前/后(Pre,Rear)', max_length=20, null=False)
    operationType = models.CharField('操作类型(Methods,DataBase)', max_length=20, null=False)
    methodsName = models.CharField('函数方法', max_length=100, null=False)
    dataBaseId = models.CharField('要执行的数据库连接ID', max_length=50, null=False)
    sql = models.TextField('Sql数据', null=False)
    remarks = models.TextField('备注', null=True)
    state = models.IntegerField("是否启用(0:禁用,1:启用)", null=False)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
    updateTime = models.DateTimeField('创建时间', auto_now=True)
    onlyCode = models.CharField('历史记录唯一码,新增的时候会创建1个', max_length=100, null=False)


class ApiCaseHistory(models.Model):  # 历史记录，恢复使用
    pid = models.ForeignKey("ProjectManagement.ProManagement", to_field='id', on_delete=models.CASCADE)
    page = models.ForeignKey("PageManagement.PageManagement", to_field='id', on_delete=models.CASCADE)
    fun = models.ForeignKey("FunManagement.FunManagement", to_field='id', on_delete=models.CASCADE)
    case = models.ForeignKey("CaseBaseData", to_field='id', on_delete=models.CASCADE)
    caseName = models.CharField("页面名称", max_length=100, null=False)
    onlyCode = models.CharField('历史记录唯一码,新增的时候会创建1个', max_length=100, null=False)
    # 如果是删除的话，在恢复数据时取上一个操作的数据
    operationType = models.CharField("操作类型(Add,Edit,Delete)", max_length=10, null=False)
    restoreData = models.TextField('恢复数据', null=True)
    # textInfo = models.TextField('保存变动的文本信息', null=True)
    createTime = models.DateTimeField('创建时间', auto_now=True)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
