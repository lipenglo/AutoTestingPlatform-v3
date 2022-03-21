from django.db import models


# Create your models here.
class PageManagement(models.Model):  # 页面管理
    sysType = models.CharField("所属系统", max_length=10, null=False)
    pid = models.ForeignKey("ProjectManagement.ProManagement", to_field='id', on_delete=models.CASCADE)
    pageName = models.CharField('页面名称', max_length=150, null=True)
    remarks = models.CharField('备注信息', max_length=300, null=True)
    createTime = models.DateTimeField('创建时间', auto_now=True)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
    cuid = models.IntegerField("创建者用户", null=False)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
    onlyCode = models.CharField('历史记录唯一码,新增的时候会创建1个', max_length=100, null=False)


class PageHistory(models.Model):  # 历史记录，恢复使用
    pid = models.ForeignKey("ProjectManagement.ProManagement", to_field='id', on_delete=models.CASCADE)
    page = models.ForeignKey("PageManagement", to_field='id', on_delete=models.CASCADE)
    pageName = models.CharField("页面名称", max_length=20, null=False)
    onlyCode = models.CharField('历史记录唯一码,新增的时候会创建1个', max_length=100, null=False)
    # 如果是删除的话，在恢复数据时取上一个操作的数据
    operationType = models.CharField("操作类型(Add,Edit,Delete)", max_length=10, null=False)
    restoreData = models.TextField('恢复数据', null=True)
    createTime = models.DateTimeField('创建时间', auto_now=True)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
