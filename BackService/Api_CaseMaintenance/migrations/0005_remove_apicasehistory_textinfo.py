# Generated by Django 2.2.24 on 2022-01-12 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Api_CaseMaintenance', '0004_auto_20220112_1525'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apicasehistory',
            name='textInfo',
        ),
    ]
