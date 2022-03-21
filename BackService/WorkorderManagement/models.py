from django.db import models


# Create your models here.
class WorkorderManagement(models.Model):  # 工单管理
    sysType = models.CharField("所属系统", max_length=10, null=False)
    pid = models.ForeignKey(to='ProjectManagement.ProManagement', to_field='id', on_delete=models.CASCADE)
    page = models.ForeignKey(to='PageManagement.PageManagement', to_field='id', on_delete=models.CASCADE)
    fun = models.ForeignKey(to='FunManagement.FunManagement', to_field='id', on_delete=models.CASCADE)
    workSource = models.IntegerField("工单来源(0:手工,1:系统)", null=False)
    workType = models.CharField("工单类型(Add,Edit,Delete,Other)", max_length=20, null=False)
    workState = models.IntegerField("工单状态(0:待受理,1:受理中,2:已解决,3:已关闭)", null=False)
    workName = models.CharField("工单名称", max_length=20, null=False)
    # message = models.TextField("工单信息", null=True)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    createTime = models.DateTimeField('创建时间', auto_now=True)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
    cuid = models.IntegerField("创建者用户", null=False)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)


class WorkBindPushToUsers(models.Model):  # 新增工单时填写的推送To的用户
    work = models.ForeignKey(to='WorkorderManagement', to_field='id', on_delete=models.CASCADE)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    createTime = models.DateTimeField('创建时间', auto_now=True)


class HistoryInfo(models.Model):  # 工单历史回复信息
    work = models.ForeignKey(to='WorkorderManagement', to_field='id', on_delete=models.CASCADE)
    message = models.TextField("工单信息", null=True)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
    createTime = models.DateTimeField('创建时间', auto_now=True)


class WorkLifeCycle(models.Model):  # 工单生命周期
    work = models.ForeignKey(to='WorkorderManagement', to_field='id', on_delete=models.CASCADE)
    workState = models.IntegerField("工单状态(0:待受理,1:受理中,2:已解决,3:已关闭)", null=False)
    operationType = models.CharField("操作类型(Add,Edit,Close)", max_length=10, null=False)
    operationInfo = models.TextField("操作信息字典类型", null=True)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
