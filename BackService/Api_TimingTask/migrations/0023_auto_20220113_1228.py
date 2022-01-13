# Generated by Django 2.2.24 on 2022-01-13 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api_TimingTask', '0022_auto_20220111_1626'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apitimingtask',
            name='historyCode',
        ),
        migrations.RemoveField(
            model_name='apitimingtaskhistory',
            name='historyCode',
        ),
        migrations.RemoveField(
            model_name='apitimingtasktestset',
            name='historyCode',
        ),
        migrations.AddField(
            model_name='apitimingtask',
            name='onlyCode',
            field=models.CharField(default=1, max_length=100, verbose_name='历史记录唯一码,新增的时候会创建1个'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='apitimingtaskhistory',
            name='onlyCode',
            field=models.CharField(default=1, max_length=100, verbose_name='历史记录唯一码,新增的时候会创建1个'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='apitimingtaskhistory',
            name='taskName',
            field=models.CharField(default=1, max_length=20, verbose_name='任务名称'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='apitimingtasktestset',
            name='onlyCode',
            field=models.CharField(default=1, max_length=100, verbose_name='历史记录唯一码,新增的时候会创建1个'),
            preserve_default=False,
        ),
    ]
