# Generated by Django 2.2.24 on 2022-01-12 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Api_IntMaintenance', '0026_apibasedata_historycode'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apiassociateduser',
            old_name='historyCode',
            new_name='onlyCode',
        ),
        migrations.RenameField(
            model_name='apibody',
            old_name='historyCode',
            new_name='onlyCode',
        ),
        migrations.RenameField(
            model_name='apiextract',
            old_name='historyCode',
            new_name='onlyCode',
        ),
        migrations.RenameField(
            model_name='apioperation',
            old_name='historyCode',
            new_name='onlyCode',
        ),
        migrations.RenameField(
            model_name='apivalidate',
            old_name='historyCode',
            new_name='onlyCode',
        ),
    ]
