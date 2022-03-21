# Generated by Django 3.2.9 on 2021-11-25 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0013_alter_operateinfo_remindtype'),
    ]

    operations = [
        migrations.AddField(
            model_name='operateinfo',
            name='updateTime',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='operateinfo',
            name='sysType',
            field=models.CharField(max_length=10, verbose_name='系统类型(Login/Home/API/UI/PTS)'),
        ),
    ]
