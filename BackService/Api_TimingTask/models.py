from django.db import models


# Create your models here.
class ApiTimingTask(models.Model):
    pid = models.ForeignKey(to='ProjectManagement.ProManagement', to_field='id', on_delete=models.CASCADE)  # 项目id
    taskName = models.CharField('任务名称', max_length=20, null=False)
    environment = models.ForeignKey(  # 页面环境
        to='PageEnvironment.PageEnvironment', to_field='id', on_delete=models.CASCADE)
    timingConfig = models.CharField('定时配置', max_length=50, null=False)
    priority = models.CharField("优先级(P0-P3)", max_length=10, null=False)
    pushTo = models.CharField('接收邮件', max_length=100, null=True)
    taskStatus = models.IntegerField("任务状态(0:禁用,1:启用)", null=False)
    remarks = models.TextField("备注信息", null=True)
    # periodicTask = models.ForeignKey(to='djcelery.PeriodicTask', to_field='id', on_delete=models.CASCADE)  # 内置任务ID
    periodicTask_id = models.IntegerField("内置任务ID", null=True)
    createTime = models.DateTimeField('创建时间', auto_now=True)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    cuid = models.IntegerField("创建人", null=False)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
    is_del = models.IntegerField("是否删除(0:删除,1:不删除)", null=False)
    onlyCode = models.CharField('历史记录唯一码,新增的时候会创建1个', max_length=100, null=False)


class ApiTimingTaskTestSet(models.Model):  # 用例排序数据
    timingTask = models.ForeignKey(to='ApiTimingTask', to_field='id', on_delete=models.CASCADE)
    index = models.IntegerField("排序", null=False)
    case = models.ForeignKey(to='Api_CaseMaintenance.CaseBaseData', to_field='id', on_delete=models.CASCADE)
    state = models.IntegerField("是否启用(0:禁用,1:启用)", null=False)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
    is_del = models.IntegerField("是否删除(0:删除,1:不删除)", null=False)
    onlyCode = models.CharField('历史记录唯一码,新增的时候会创建1个', max_length=100, null=False)


class ApiTimingTaskHistory(models.Model):  # 历史记录，恢复使用
    timingTask = models.ForeignKey(to='ApiTimingTask', to_field='id', on_delete=models.CASCADE)
    taskName = models.CharField('任务名称', max_length=20, null=False)
    onlyCode = models.CharField('历史记录唯一码,新增的时候会创建1个', max_length=100, null=False)
    # 如果是删除的话，在恢复数据时取上一个操作的数据
    operationType = models.CharField("操作类型(Add,Edit,Delete)", max_length=10, null=False)
    restoreData = models.TextField('恢复数据,用来存放基础数据', null=True)
    createTime = models.DateTimeField('创建时间', auto_now=True)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id


class ApiTimingTaskRunLog(models.Model):  # 运行记录
    timingTask = models.ForeignKey(to='ApiTimingTask', to_field='id', on_delete=models.CASCADE)  # 项目id
    taskName = models.CharField('任务名称', max_length=20, null=False)
    runType = models.CharField('运行类型(手动(Manual)/自动(Auto))', max_length=10, null=False)
    testReport = models.ForeignKey(to='Api_TestReport.ApiTestReport', to_field='id', on_delete=models.CASCADE)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
