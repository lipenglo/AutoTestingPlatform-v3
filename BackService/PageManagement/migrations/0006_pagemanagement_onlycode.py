# Generated by Django 2.2.24 on 2022-01-12 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PageManagement', '0005_pagehistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagemanagement',
            name='onlyCode',
            field=models.CharField(default=1, max_length=100, verbose_name='历史记录唯一码,新增的时候会创建1个'),
            preserve_default=False,
        ),
    ]