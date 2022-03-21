from django.db import models


# Create your models here.
class ProManagement(models.Model):
    sysType = models.CharField("所属系统", max_length=10, null=False)
    proName = models.CharField("项目名称", max_length=20, null=False)
    remarks = models.CharField("备注信息", max_length=100, null=True)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    createTime = models.DateTimeField('创建时间', auto_now=True)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
    cuid = models.IntegerField("创建者用户", null=False)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
    onlyCode = models.CharField('历史记录唯一码,新增的时候会创建1个', max_length=100, null=False)


class ProBindMembers(models.Model):  # 项目绑定成员
    pid = models.ForeignKey(to='ProManagement', to_field='id', on_delete=models.CASCADE)
    role = models.ForeignKey(to='role.BasicRole', to_field='id', on_delete=models.CASCADE)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    createTime = models.DateTimeField('创建时间', auto_now=True)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)


class ProHistory(models.Model):  # 历史记录，恢复使用
    pid = models.ForeignKey("ProManagement", to_field='id', on_delete=models.CASCADE)
    proName = models.CharField("项目名称", max_length=20, null=False)
    onlyCode = models.CharField('历史记录唯一码,新增的时候会创建1个', max_length=100, null=False)
    # 如果是删除的话，在恢复数据时取上一个操作的数据
    operationType = models.CharField("操作类型(Add,Edit,Delete)",max_length=10, null=False)
    restoreData = models.TextField('恢复数据,此数据主要保存基础数据', null=True)
    # textInfo = models.TextField('保存变动的文本信息', null=True)
    createTime = models.DateTimeField('创建时间', auto_now=True)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id