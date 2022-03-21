from django.db import models


# Create your models here.
class DataBase(models.Model):
    # sysType = models.CharField("所属系统", max_length=10, null=False)
    dbType = models.CharField('数据库类型(MySql,)', max_length=50, null=False)
    dataBaseIp = models.CharField('IP', max_length=50, null=False)
    port = models.CharField('端口', max_length=10, null=False)
    userName = models.CharField('用户名', max_length=50, null=False)
    passWord = models.CharField('密码', max_length=50, null=False)
    remarks = models.TextField("备注信息", null=True)
    createTime = models.DateTimeField('创建时间', auto_now=True)
    updateTime = models.DateTimeField('修改时间', auto_now=True)
    uid = models.ForeignKey(to='login.UserTable', to_field='id', on_delete=models.CASCADE)  # 用户Id
    cuid = models.IntegerField("创建者用户", null=False)
    is_del = models.IntegerField("是否删除(0:删除,1:不删除)", null=False)
