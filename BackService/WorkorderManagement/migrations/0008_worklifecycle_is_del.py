# Generated by Django 2.2.24 on 2021-12-09 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WorkorderManagement', '0007_auto_20211209_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='worklifecycle',
            name='is_del',
            field=models.IntegerField(default=1, verbose_name='是否删除(1:删除,0:不删除)'),
            preserve_default=False,
        ),
    ]