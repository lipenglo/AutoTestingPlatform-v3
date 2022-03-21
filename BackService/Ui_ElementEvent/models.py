from django.db import models


# Create your models here.
class ElementEvent(models.Model):
    index = models.IntegerField("数据排序", null=False)
    eventName = models.CharField("事件名称", max_length=20, null=False)
    eventLogo = models.CharField("事件标识", max_length=50, null=False)
    remarks = models.TextField("备注信息", null=True)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    createTime = models.DateTimeField('创建时间', auto_now=True)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
    cuid = models.IntegerField("创建者用户", null=False)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
    onlyCode = models.CharField('历史记录唯一码', max_length=100, null=False)


class ElementEventComponent(models.Model):#元素组件表
    event = models.ForeignKey(to='ElementEvent', to_field='id', on_delete=models.CASCADE)
    index = models.IntegerField("数据排序", null=False)
    label = models.CharField('', max_length=20, null=False)
    value = models.CharField('', max_length=100, null=False)
    remarks = models.TextField('备注', null=True)
    state = models.IntegerField("是否启用(0:禁用,1:启用)", null=False)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
    updateTime = models.DateTimeField('创建时间', auto_now=True)
    onlyCode = models.CharField('历史记录唯一码', max_length=100, null=False)