# Generated by Django 3.2.9 on 2021-11-25 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0011_auto_20211125_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operateinfo',
            name='level',
            field=models.IntegerField(default=4, verbose_name='提醒等级(错误(1),警告(2),新增和修改(3),其他(4))'),
            preserve_default=False,
        ),
    ]
