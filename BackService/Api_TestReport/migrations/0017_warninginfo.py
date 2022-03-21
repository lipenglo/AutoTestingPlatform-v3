# Generated by Django 2.2.24 on 2022-01-17 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0008_auto_20211129_1528'),
        ('Api_TestReport', '0016_apitestreport_createtime'),
    ]

    operations = [
        migrations.CreateModel(
            name='WarningInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('triggerType', models.CharField(max_length=20, verbose_name='触发类型(Warning,Error)')),
                ('taskId', models.CharField(max_length=10, verbose_name='ApiId/CaseId/TaskId/BatchId,根据任务类型来取')),
                ('taskName', models.CharField(max_length=50, verbose_name='接口/用例/定时任务的名称')),
                ('info', models.TextField(null=True, verbose_name='信息')),
                ('updateTime', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('testReport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Api_TestReport.ApiTestReport')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.UserTable')),
            ],
        ),
    ]
