# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-28 04:09
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseStation',
            fields=[
                ('base_id', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('region', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateField(default=datetime.datetime(2017, 3, 28, 4, 9, 30, 671831, tzinfo=utc))),
                ('level_reading', models.DecimalField(decimal_places=2, max_digits=4)),
                ('power_level', models.DecimalField(decimal_places=2, max_digits=4)),
                ('base_station_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insumeter.BaseStation')),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('sensor_id', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('base_station_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insumeter.BaseStation')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=200)),
                ('first_name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('email_verified', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='logs',
            name='sensor_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insumeter.Sensor'),
        ),
        migrations.AddField(
            model_name='basestation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insumeter.User'),
        ),
    ]
