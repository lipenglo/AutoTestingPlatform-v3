# Generated by Django 2.2.24 on 2022-01-28 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ui_ElementMaintenance', '0006_elementdynamic'),
    ]

    operations = [
        migrations.AddField(
            model_name='elementhistory',
            name='textInfo',
            field=models.TextField(null=True, verbose_name='保存变动的文本信息'),
        ),
    ]
