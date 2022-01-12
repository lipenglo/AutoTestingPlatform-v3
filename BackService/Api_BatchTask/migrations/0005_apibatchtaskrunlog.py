# Generated by Django 2.2.24 on 2022-01-12 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Api_TestReport', '0015_auto_20220111_1427'),
        ('login', '0008_auto_20211129_1528'),
        ('Api_BatchTask', '0004_auto_20220111_1123'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiBatchTaskRunLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('runType', models.CharField(max_length=10, verbose_name='运行类型(手动(Manual)/自动(Hook))')),
                ('updateTime', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('batchTask', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Api_BatchTask.ApiBatchTask')),
                ('testReport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Api_TestReport.ApiTestReport')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.UserTable')),
            ],
        ),
    ]
