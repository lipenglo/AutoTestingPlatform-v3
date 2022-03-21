from django.db import models


# Create your models here.
class DebugTalk(models.Model):
    codeInfo = models.TextField('代码信息', null=True)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
