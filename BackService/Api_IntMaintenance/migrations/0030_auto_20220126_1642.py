# Generated by Django 2.2.24 on 2022-01-26 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api_IntMaintenance', '0029_apihistory_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apidynamic',
            name='is_read',
            field=models.IntegerField(verbose_name='是否已读(1:已看,0:未看)'),
        ),
    ]
