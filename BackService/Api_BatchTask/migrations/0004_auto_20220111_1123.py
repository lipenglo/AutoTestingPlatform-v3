# Generated by Django 2.2.24 on 2022-01-11 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api_BatchTask', '0003_apibatchtaskhistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apibatchtaskhistory',
            name='historyCode',
            field=models.CharField(max_length=100, null=True, verbose_name='历史记录唯一码'),
        ),
    ]
