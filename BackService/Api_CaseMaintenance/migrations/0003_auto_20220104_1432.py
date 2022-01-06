# Generated by Django 2.2.24 on 2022-01-04 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api_CaseMaintenance', '0002_caseapibase_caseapibody_caseapiextract_caseapiheaders_caseapioperation_caseapiparams_caseapivalidate'),
    ]

    operations = [
        migrations.AddField(
            model_name='caseapibody',
            name='filePath',
            field=models.TextField(null=True, verbose_name='文件保存地址'),
        ),
        migrations.AddField(
            model_name='caseapibody',
            name='paramsType',
            field=models.CharField(default=1, max_length=10, verbose_name='入参类型(Text,File)'),
            preserve_default=False,
        ),
    ]