# Generated by Django 2.2.24 on 2022-01-07 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api_TimingTask', '0008_apitimingtask_historycode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apitimingtask',
            name='historyCode',
            field=models.CharField(default=1, max_length=100, verbose_name='历史记录唯一码'),
            preserve_default=False,
        ),
    ]