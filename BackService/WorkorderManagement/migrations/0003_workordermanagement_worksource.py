# Generated by Django 2.2.24 on 2021-12-01 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WorkorderManagement', '0002_auto_20211201_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='workordermanagement',
            name='workSource',
            field=models.IntegerField(default=0, verbose_name='工单来源(0:手工,1:系统)'),
            preserve_default=False,
        ),
    ]
