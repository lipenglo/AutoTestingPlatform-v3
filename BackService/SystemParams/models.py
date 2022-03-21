from django.db import models


# Create your models here.
class SystemParams(models.Model):
    sysType = models.CharField("所属系统", max_length=10, null=False)
    label = models.CharField("标签", max_length=20, null=False)
    keyName = models.CharField("参数名称", max_length=100, null=False)
    value = models.CharField("参数值", max_length=100, null=True)
    valueType = models.CharField("参数类型(Input,Bool)", max_length=10, null=False)
    remarks = models.CharField("备注信息", max_length=100, null=True)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
