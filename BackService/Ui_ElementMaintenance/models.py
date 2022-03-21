from django.db import models


# Create your models here.
class ElementBaseData(models.Model):
    pid = models.ForeignKey(to='ProjectManagement.ProManagement', to_field='id', on_delete=models.CASCADE)
    page = models.ForeignKey(to='PageManagement.PageManagement', to_field='id', on_delete=models.CASCADE)
    fun = models.ForeignKey(to='FunManagement.FunManagement', to_field='id', on_delete=models.CASCADE)
    elementName = models.CharField('元素名称', max_length=100, null=False)
    elementType = models.CharField('元素类型', max_length=50, null=False)
    elementState = models.IntegerField("是否启用(1:启用,0:禁用)", null=False)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 最后更新者
    cuid = models.IntegerField("创建者用户", null=False)
    createTime = models.DateTimeField('创建时间', auto_now=True)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
    onlyCode = models.CharField('历史记录唯一码', max_length=100, null=False)


class ElementLocation(models.Model):  # 元素定位表
    element = models.ForeignKey(to='ElementBaseData', to_field='id', on_delete=models.CASCADE)
    index = models.IntegerField("数据排序", null=False)
    targetingType = models.CharField('定位类型', max_length=20, null=False)
    targetingPath = models.CharField('定位地址', max_length=500, null=False)
    remarks = models.TextField('备注', null=True)
    state = models.IntegerField("是否启用(0:禁用,1:启用)", null=False)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
    updateTime = models.DateTimeField('创建时间', auto_now=True)
    onlyCode = models.CharField('历史记录唯一码', max_length=100, null=False)


class ElementDynamic(models.Model):  # 元素更变动态表
    element = models.ForeignKey(to='ElementBaseData', to_field='id', on_delete=models.CASCADE)
    case = models.ForeignKey(to='Ui_CaseMaintenance.UiCaseBaseData', to_field='id', on_delete=models.CASCADE)
    is_read = models.IntegerField("是否已读(1:已看,0:未看)", null=False)
    createTime = models.DateTimeField('创建时间', auto_now=True)
    updateTime = models.DateTimeField('更新时间', auto_now=True)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
    cuid = models.IntegerField("创建者用户", null=False)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)


class ElementHistory(models.Model):  # 历史记录，恢复使用
    pid = models.ForeignKey("ProjectManagement.ProManagement", to_field='id', on_delete=models.CASCADE)
    page = models.ForeignKey("PageManagement.PageManagement", to_field='id', on_delete=models.CASCADE)
    fun = models.ForeignKey("FunManagement.FunManagement", to_field='id', on_delete=models.CASCADE)
    element = models.ForeignKey(to='ElementBaseData', to_field='id', on_delete=models.CASCADE)
    elementName = models.CharField("元素名称", max_length=20, null=False)
    onlyCode = models.CharField('历史记录唯一码,新增的时候会创建1个', max_length=100, null=False)
    # 如果是删除的话，在恢复数据时取上一个操作的数据
    operationType = models.CharField("操作类型(Add,Edit,Delete)", max_length=10, null=False)
    restoreData = models.TextField('恢复数据', null=True)
    textInfo = models.TextField('保存变动的文本信息', null=True)
    createTime = models.DateTimeField('创建时间', auto_now=True)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
