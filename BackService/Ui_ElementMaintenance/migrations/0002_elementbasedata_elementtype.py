# Generated by Django 2.2.24 on 2022-01-21 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ui_ElementMaintenance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='elementbasedata',
            name='elementType',
            field=models.CharField(default=1, max_length=50, verbose_name='元素类型'),
            preserve_default=False,
        ),
    ]
