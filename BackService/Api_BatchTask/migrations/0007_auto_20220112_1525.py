# Generated by Django 2.2.24 on 2022-01-12 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api_BatchTask', '0006_apibatchtaskrunlog_versions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apibatchtaskrunlog',
            name='runType',
            field=models.CharField(max_length=10, verbose_name='运行类型(手动(Manual)/钩子(Hook))'),
        ),
    ]
