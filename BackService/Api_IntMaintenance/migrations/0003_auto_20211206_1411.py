# Generated by Django 2.2.24 on 2021-12-06 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api_IntMaintenance', '0002_apiheaders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apibasedata',
            name='apiState',
            field=models.CharField(max_length=10, verbose_name='接口状态(InDev,Completed,Discard)'),
        ),
    ]