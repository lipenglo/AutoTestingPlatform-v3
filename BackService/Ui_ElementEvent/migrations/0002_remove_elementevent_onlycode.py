# Generated by Django 2.2.24 on 2022-01-21 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Ui_ElementEvent', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='elementevent',
            name='onlyCode',
        ),
    ]
