from django.db import models


# Create your models here.
class ApiBatchTask(models.Model):
    pid = models.ForeignKey(to='ProjectManagement.ProManagement', to_field='id', on_delete=models.CASCADE)  # 项目id
    batchName = models.CharField('任务名称', max_length=20, null=False)
    priority = models.CharField("优先级(P0-P3)", max_length=10, null=False)
    pushTo = models.CharField('接收邮件', max_length=100, null=True)
    remarks = models.TextField("备注信息", null=True)
    hookId = models.CharField('钩子ID，是一个随机码的唯一值', max_length=100, null=False)
    hookState = models.IntegerField("是否开启(0:未开启,1:开启)", null=False)
    createTime = models.DateTimeField('创建时间', auto_now=True)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    cuid = models.IntegerField("创建人", null=False)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
    is_del = models.IntegerField("是否删除(0:删除,1:不删除)", null=False)
    onlyCode = models.CharField('历史记录唯一码,新增的时候会创建1个', max_length=100, null=False)


class ApiBatchTaskTestSet(models.Model):  # 任务排序数据
    batchTask = models.ForeignKey(to='ApiBatchTask', to_field='id', on_delete=models.CASCADE)
    index = models.IntegerField("排序", null=False)
    task = models.ForeignKey(to='Api_TimingTask.ApiTimingTask', to_field='id', on_delete=models.CASCADE)
    state = models.IntegerField("是否启用(0:禁用,1:启用)", null=False)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
    is_del = models.IntegerField("是否删除(0:删除,1:不删除)", null=False)
    onlyCode = models.CharField('历史记录唯一码,新增的时候会创建1个', max_length=100, null=False)


class ApiBatchTaskHistory(models.Model):  # 历史记录，恢复使用
    batchTask = models.ForeignKey(to='ApiBatchTask', to_field='id', on_delete=models.CASCADE)
    batchName = models.CharField('任务名称', max_length=20, null=False)
    onlyCode = models.CharField('历史记录唯一码,新增的时候会创建1个', max_length=100, null=False)
    # 如果是删除的话，在恢复数据时取上一个操作的数据
    operationType = models.CharField("操作类型(Add,Edit,Delete)", max_length=10, null=False)
    restoreData = models.TextField('恢复数据,用来存放基础数据', null=True)
    createTime = models.DateTimeField('创建时间', auto_now=True)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id


class ApiBatchTaskRunLog(models.Model):  # 运行记录
    batchTask = models.ForeignKey(to='ApiBatchTask', to_field='id', on_delete=models.CASCADE)
    versions = models.CharField('版本号', max_length=20, null=True)
    runType = models.CharField('运行类型(手动(Manual)/钩子(Hook))', max_length=10, null=False)
    testReport = models.ForeignKey(to='Api_TestReport.ApiTestReport', to_field='id', on_delete=models.CASCADE)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
