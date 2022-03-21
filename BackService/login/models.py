from django.db import models


# Create your models here.
class UserTable(models.Model):
    userId = models.IntegerField("内置用户ID", null=False)  # Dango内置的用户，因为要用到token数据
    userName = models.CharField(max_length=50, null=False)
    nickName = models.CharField(max_length=200, null=False)
    userImg = models.TextField('用户图片base64', null=True)
    imgMD5 = models.CharField(max_length=100, null=True)
    emails = models.CharField(max_length=100, null=True)
    is_lock = models.IntegerField("是否锁定(0:不锁定,1:锁定)", null=False)
    is_activation = models.IntegerField("是否激活(0:未激活,1:已激活)", null=False)
    is_del = models.IntegerField(null=False, verbose_name="是否删除(0:不删除,1:删除)")
    createTime = models.DateTimeField('创建时间', auto_now=True)
    updateTime = models.DateTimeField('更新时间', auto_now=True)


class UserBindRole(models.Model):  # 用户绑定基础角色,新增用户的时候选择绑定
    user = models.ForeignKey("UserTable", to_field='id', on_delete=models.CASCADE)  # 用户ID
    role = models.ForeignKey("role.BasicRole", to_field='id', on_delete=models.CASCADE)  # 基础角色ID
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
    createTime = models.DateTimeField('创建时间', auto_now=True)
    updateTime = models.DateTimeField('更新时间', auto_now=True)
