# Generated by Django 2.2.24 on 2022-01-21 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Ui_ElementEvent', '0003_elementevent_eventlogo'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElementEventComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField(verbose_name='数据排序')),
                ('label', models.CharField(max_length=20, verbose_name='')),
                ('value', models.CharField(max_length=20, verbose_name='')),
                ('remarks', models.TextField(null=True, verbose_name='备注')),
                ('state', models.IntegerField(verbose_name='是否启用(0:禁用,1:启用)')),
                ('is_del', models.IntegerField(verbose_name='是否删除(1:删除,0:不删除)')),
                ('updateTime', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Ui_ElementEvent.ElementEvent')),
            ],
        ),
    ]
