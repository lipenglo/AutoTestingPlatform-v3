# Generated by Django 2.2.24 on 2021-12-02 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0023_pushinfo_is_read'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operateinfo',
            name='is_read',
        ),
        migrations.AlterField(
            model_name='operateinfo',
            name='level',
            field=models.IntegerField(verbose_name='提醒等级(错误(1),警告(2),新增/修改/删除(3)),其他(4)'),
        ),
    ]
