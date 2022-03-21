from django.db import models


# Create your models here.
class PageEnvironment(models.Model):  # 页面环境
    sysType = models.CharField("所属系统", max_length=10, null=False)
    pid = models.ForeignKey("ProjectManagement.ProManagement", to_field='id', on_delete=models.CASCADE)
    environmentName = models.CharField('环境名称', max_length=150, null=True)
    environmentUrl = models.CharField('备注信息', max_length=300, null=True)
    remarks = models.TextField('备注', null=True)
    createTime = models.DateTimeField('创建时间', auto_now=True)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
    cuid = models.IntegerField("创建者用户", null=False)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
