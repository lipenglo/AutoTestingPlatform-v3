# Generated by Django 2.2.24 on 2021-12-13 14:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Api_IntMaintenance', '0011_apihistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='apihistory',
            name='api',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Api_IntMaintenance.ApiBaseData'),
            preserve_default=False,
        ),
    ]