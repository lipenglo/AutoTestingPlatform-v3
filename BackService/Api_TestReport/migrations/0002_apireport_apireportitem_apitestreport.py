# Generated by Django 2.2.24 on 2021-12-14 10:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Api_IntMaintenance', '0015_auto_20211213_1620'),
        ('ProjectManagement', '0013_auto_20211213_1048'),
        ('login', '0008_auto_20211129_1528'),
        ('Api_TestReport', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiTestReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reportName', models.CharField(max_length=50, verbose_name='报告名称')),
                ('reportType', models.CharField(max_length=10, verbose_name='报告类型(API:单接口,CASE:测试用例,TASK:定时任务,BATCH:批量任务)')),
                ('taskId', models.CharField(max_length=10, verbose_name='ApiId/CaseId/TaskId/BatchId,根据任务类型来取')),
                ('apiTotal', models.IntegerField(verbose_name='统计总需要执行的接口数量')),
                ('reportStatus', models.CharField(max_length=10, verbose_name='测试报告状态(Pass,Fail,Error,Running)')),
                ('updateTime', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_del', models.IntegerField(verbose_name='是否删除(1:删除,0:不删除)')),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ProjectManagement.ProManagement')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.UserTable')),
            ],
        ),
        migrations.CreateModel(
            name='ApiReportItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apiName', models.CharField(max_length=50, null=True, verbose_name='接口名称')),
                ('ctbId', models.IntegerField(null=True, verbose_name='单接口没有此ID/Case,Task,Batch类型时这里显示CaseId')),
                ('runningTime', models.FloatField(null=True, verbose_name='运行总时间')),
                ('successTotal', models.IntegerField(verbose_name='成功数')),
                ('failTotal', models.IntegerField(verbose_name='失败数')),
                ('errorTotal', models.IntegerField(verbose_name='错误数')),
                ('updateTime', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_del', models.IntegerField(verbose_name='是否删除(1:删除,0:不删除)')),
                ('apiId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Api_IntMaintenance.ApiBaseData')),
                ('testReport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Api_TestReport.ApiTestReport')),
            ],
        ),
        migrations.CreateModel(
            name='ApiReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requestUrl', models.CharField(max_length=100, verbose_name='请求地址')),
                ('requestType', models.CharField(max_length=50, verbose_name='请求类型(GET/POST)')),
                ('requestHeaders', models.TextField(null=True, verbose_name='请求头部')),
                ('requestData', models.TextField(null=True, verbose_name='请求数据')),
                ('requestFile', models.TextField(null=True, verbose_name='请求文件')),
                ('reportStatus', models.IntegerField(verbose_name='测试报告状态(0:Pass,1:Fail,2:Error)')),
                ('statusCode', models.IntegerField(verbose_name='返回代码')),
                ('responseHeaders', models.TextField(null=True, verbose_name='返回头部')),
                ('responseInfo', models.TextField(null=True, verbose_name='返回信息')),
                ('requestExtract', models.TextField(null=True, verbose_name='请求提取信息')),
                ('requestValidate', models.TextField(null=True, verbose_name='请求断言信息')),
                ('responseValidate', models.TextField(null=True, verbose_name='返回断言信息')),
                ('responseMethods', models.TextField(null=True, verbose_name='返回调用方法信息')),
                ('errorInfo', models.TextField(null=True, verbose_name='错误信息')),
                ('runningTime', models.CharField(max_length=50, null=True, verbose_name='运行总时间')),
                ('updateTime', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_del', models.IntegerField(verbose_name='是否删除(1:删除,0:不删除)')),
                ('reportItem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Api_TestReport.ApiReportItem')),
            ],
        ),
    ]