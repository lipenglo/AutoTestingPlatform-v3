# Generated by Django 2.2.24 on 2021-12-01 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0018_auto_20211129_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='operateinfo',
            name='toPro',
            field=models.CharField(max_length=100, null=True, verbose_name='所属项目'),
        ),
        migrations.AlterField(
            model_name='operateinfo',
            name='info',
            field=models.TextField(null=True, verbose_name='信息'),
        ),
        migrations.AlterField(
            model_name='operateinfo',
            name='level',
            field=models.IntegerField(verbose_name='提醒等级(错误(1),警告(2),新增/修改/删除(3),其他(4))'),
        ),
        migrations.AlterField(
            model_name='operateinfo',
            name='remindType',
            field=models.CharField(max_length=10, verbose_name='提醒类别 Error,Warning,Add,Edit,Delete,Other'),
        ),
    ]