# Generated by Django 2.2.24 on 2021-11-30 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('role', '0003_auto_20211129_1528'),
        ('ProjectManagement', '0004_auto_20211130_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='probindmembers',
            name='role',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='role.BasicRole'),
            preserve_default=False,
        ),
    ]
