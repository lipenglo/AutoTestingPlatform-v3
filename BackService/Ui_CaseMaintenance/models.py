from django.db import models


# Create your models here.
class UiCaseBaseData(models.Model):  # 基础数据
    pid = models.ForeignKey(to='ProjectManagement.ProManagement', to_field='id', on_delete=models.CASCADE)
    page = models.ForeignKey(to='PageManagement.PageManagement', to_field='id', on_delete=models.CASCADE)
    fun = models.ForeignKey(to='FunManagement.FunManagement', to_field='id', on_delete=models.CASCADE)
    environmentId = models.ForeignKey(to='PageEnvironment.PageEnvironment', to_field='id', on_delete=models.CASCADE)
    testType = models.CharField("测试类型(Function:功能,Smoke:冒烟)", max_length=20, null=False)
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


class UiAssociatedPage(models.Model):  # 关联页面
    case = models.ForeignKey(to='UiCaseBaseData', to_field='id', on_delete=models.CASCADE)
    page = models.ForeignKey(to='PageManagement.PageManagement', to_field='id', on_delete=models.CASCADE)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
    onlyCode = models.CharField('历史记录唯一码,新增的时候会创建1个', max_length=100, null=False)


class UiTestSet(models.Model):  # 测试集
    case = models.ForeignKey(to='UiCaseBaseData', to_field='id', on_delete=models.CASCADE)
    index = models.IntegerField("排序", null=False)
    state = models.IntegerField("是否启用(1:启用,0:禁用)", null=False)
    eventName = models.CharField('事件名称', max_length=50, null=True)
    elementId = models.IntegerField("元素ID", null=True)
    elementType = models.CharField('最终元素操作类型', max_length=100, null=True)
    inputData = models.CharField('输入/选择', max_length=500, null=True)
    assertType = models.CharField('断言类型', max_length=50, null=True)
    assertValueType = models.CharField('断言值类型', max_length=50, null=True)
    assertValue = models.TextField('断言值', null=True)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
    updateTime = models.DateTimeField('创建时间', auto_now=True)
    onlyCode = models.CharField('历史记录唯一码,新增的时候会创建1个', max_length=100, null=False)


class UiOperationSet(models.Model):  # 操作集
    case = models.ForeignKey(to='UiCaseBaseData', to_field='id', on_delete=models.CASCADE)
    index = models.IntegerField("排序", null=False)
    state = models.IntegerField("是否启用(1:启用,0:禁用)", null=False)
    location = models.CharField('位置 前/后(Pre,Rear)', max_length=20, null=False)
    operationType = models.CharField('操作类型(Methods,DataBase,TestCase)', max_length=20, null=False)
    methodsName = models.CharField('函数方法', max_length=100, null=True)
    dataBaseId = models.CharField('要执行的数据库连接ID', max_length=50, null=True)
    sql = models.TextField('SQL', null=True)
    caseId = models.CharField('要执行的用例ID', max_length=50, null=True)
    remarks = models.TextField('备注', null=True)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
    updateTime = models.DateTimeField('创建时间', auto_now=True)
    onlyCode = models.CharField('历史记录唯一码,新增的时候会创建1个', max_length=100, null=False)
