# Generated by Django 2.2.24 on 2021-11-29 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0007_userbindrole'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbindrole',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='usertable',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]