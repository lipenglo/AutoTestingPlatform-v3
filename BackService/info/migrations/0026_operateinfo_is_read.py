# Generated by Django 2.2.24 on 2021-12-06 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0025_auto_20211202_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='operateinfo',
            name='is_read',
            field=models.IntegerField(null=True, verbose_name='是否已读，只用error才会有此数据(0:未读,1:已读)'),
        ),
    ]
