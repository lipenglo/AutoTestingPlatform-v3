# Generated by Django 3.2.9 on 2021-11-23 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_delete_errormsg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertable',
            name='userImg',
            field=models.TextField(null=True, verbose_name='用户图片base64'),
        ),
    ]
