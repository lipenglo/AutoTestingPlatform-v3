# Generated by Django 2.2.24 on 2021-12-13 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api_IntMaintenance', '0014_remove_apiassociateduser_historyid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apibody',
            name='historyId',
        ),
        migrations.RemoveField(
            model_name='apiextract',
            name='historyId',
        ),
        migrations.RemoveField(
            model_name='apiheaders',
            name='historyId',
        ),
        migrations.RemoveField(
            model_name='apioperation',
            name='historyId',
        ),
        migrations.RemoveField(
            model_name='apiparams',
            name='historyId',
        ),
        migrations.RemoveField(
            model_name='apivalidate',
            name='historyId',
        ),
        migrations.AddField(
            model_name='apiassociateduser',
            name='historyCode',
            field=models.CharField(default=1, max_length=100, verbose_name='历史记录唯一码'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='apibody',
            name='historyCode',
            field=models.CharField(default=1, max_length=100, verbose_name='历史记录唯一码'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='apiextract',
            name='historyCode',
            field=models.CharField(default=1, max_length=100, verbose_name='历史记录唯一码'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='apiheaders',
            name='historyCode',
            field=models.CharField(default=1, max_length=100, verbose_name='历史记录唯一码'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='apihistory',
            name='onlyCode',
            field=models.CharField(default=1, max_length=100, verbose_name='历史记录唯一码,新增的时候会创建1个'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='apioperation',
            name='historyCode',
            field=models.CharField(default=1, max_length=100, verbose_name='历史记录唯一码'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='apiparams',
            name='historyCode',
            field=models.CharField(default=1, max_length=100, verbose_name='历史记录唯一码'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='apivalidate',
            name='historyCode',
            field=models.CharField(default=1, max_length=100, verbose_name='历史记录唯一码'),
            preserve_default=False,
        ),
    ]