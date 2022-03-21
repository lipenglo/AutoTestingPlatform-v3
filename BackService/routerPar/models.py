from django.db import models


# Create your models here.
class Router(models.Model):  # 路由菜单
    sysType = models.CharField("所属页面(HOME/API/UI/PTS)", max_length=10, null=True)
    level = models.IntegerField("菜单级别 1,2", null=False)
    index = models.CharField("菜单index", max_length=50, null=True)
    menuName = models.CharField("菜单名称", max_length=50, null=True)
    routerPath = models.CharField("路由地址", max_length=100, null=True)
    icon = models.CharField("菜单图标", max_length=50, null=True)
    belogId = models.IntegerField("上级id", null=True)
    sortNum = models.IntegerField("排序", null=True)
    is_del = models.IntegerField("是否删除(1:删除,0:不删除)", null=False)
    createTime = models.DateTimeField('创建时间', auto_now=True)
    updateTime = models.DateTimeField('更新时间', auto_now=True)
