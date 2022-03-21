from django.db import models


# Create your models here.

class NoticeInfo(models.Model):
    abstract = models.CharField('公告简介', max_length=100, null=True)
    info = models.TextField('公告信息', null=True)
    state = models.IntegerField("展示状态(1:展示,0:不展示)", null=False)
    createTime = models.DateTimeField('创建时间', auto_now=True)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
    cuid = models.IntegerField("创建者用户", null=False)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
