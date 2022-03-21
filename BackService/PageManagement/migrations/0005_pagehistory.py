# Generated by Django 2.2.24 on 2021-12-13 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ProjectManagement', '0013_auto_20211213_1048'),
        ('PageManagement', '0004_delete_history'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pageName', models.CharField(max_length=20, verbose_name='页面名称')),
                ('onlyCode', models.CharField(max_length=100, verbose_name='历史记录唯一码,新增的时候会创建1个')),
                ('operationType', models.CharField(max_length=10, verbose_name='操作类型(Add,Edit,Delete)')),
                ('restoreData', models.TextField(null=True, verbose_name='恢复数据')),
                ('createTime', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PageManagement.PageManagement')),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ProjectManagement.ProManagement')),
            ],
        ),
    ]
