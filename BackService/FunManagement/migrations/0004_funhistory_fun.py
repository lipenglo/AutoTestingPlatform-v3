# Generated by Django 2.2.24 on 2021-12-13 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FunManagement', '0003_funhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='funhistory',
            name='fun',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='FunManagement.FunManagement'),
            preserve_default=False,
        ),
    ]
