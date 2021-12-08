from django.db import models


# Create your models here.

class GlobalVariable(models.Model):
    sysType = models.CharField("所属系统", max_length=10, null=False)
    pid = models.ForeignKey("ProjectManagement.ProManagement", to_field='id', on_delete=models.CASCADE)
    globalType = models.IntegerField("变量类型(0:普通变量,1:全局变量)", null=False)
    globalName = models.CharField('变量名称', max_length=100, null=True)
    globalValue = models.TextField('变量值', null=True)
    remarks = models.TextField('备注', null=True)
    createTime = models.DateTimeField('创建时间', auto_now=True)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
    cuid = models.IntegerField("创建者用户", null=False)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
