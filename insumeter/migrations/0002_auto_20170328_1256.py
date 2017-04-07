# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-28 12:56
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('insumeter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InsumeterUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_verified', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='basestation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insumeter.InsumeterUser'),
        ),
        migrations.AlterField(
            model_name='logs',
            name='timestamp',
            field=models.DateField(default=datetime.datetime(2017, 3, 28, 12, 56, 28, 310542, tzinfo=utc)),
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='insumeteruser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
