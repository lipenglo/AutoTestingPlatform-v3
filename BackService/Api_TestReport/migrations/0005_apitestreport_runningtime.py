# Generated by Django 2.2.24 on 2021-12-14 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api_TestReport', '0004_auto_20211214_1448'),
    ]

    operations = [
        migrations.AddField(
            model_name='apitestreport',
            name='runningTime',
            field=models.FloatField(null=True, verbose_name='运行总时间'),
        ),
    ]
