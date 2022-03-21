# Generated by Django 2.2.24 on 2021-12-06 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api_IntMaintenance', '0008_apioperation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apioperation',
            old_name='opertionType',
            new_name='operationType',
        ),
        migrations.AlterField(
            model_name='apioperation',
            name='location',
            field=models.CharField(max_length=20, verbose_name='位置 前/后(Pre,Rear)'),
        ),
    ]
