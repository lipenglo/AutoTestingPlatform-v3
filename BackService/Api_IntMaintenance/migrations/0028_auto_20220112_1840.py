# Generated by Django 2.2.24 on 2022-01-12 18:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Api_IntMaintenance', '0027_auto_20220112_1838'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apibasedata',
            old_name='historyCode',
            new_name='onlyCode',
        ),
        migrations.RenameField(
            model_name='apiheaders',
            old_name='historyCode',
            new_name='onlyCode',
        ),
        migrations.RenameField(
            model_name='apiparams',
            old_name='historyCode',
            new_name='onlyCode',
        ),
    ]
