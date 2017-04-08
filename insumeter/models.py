from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from datetime import datetime


class InsumeterUser(models.Model):
    user = models.OneToOneField(User)
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username       # Think about last name instead


class BaseStation(models.Model):
    base_id = models.CharField(primary_key=True, max_length=10, null=False, unique=True)
    region = models.CharField(max_length=50)
    user = models.ForeignKey(InsumeterUser)

    def __str__(self):
        return self.base_id
# TODO increase max number of sensors since more sensors will be in use compated to base stations. Many to one.


class Sensor(models.Model):
    sensor_id = models.CharField(primary_key=True, max_length=10, null=False, unique=True)
    base_station_id = models.ForeignKey(BaseStation)

    def __str__(self):
        return self.sensor_id


class Log(models.Model):
    timestamp = models.DateTimeField(default=datetime.now)
    level_reading = models.DecimalField(null=False, decimal_places=2, max_digits=4)
    base_station_id = models.ForeignKey(BaseStation)
    sensor_id = models.ForeignKey(Sensor)
    power_level = models.DecimalField(null=False, decimal_places=2, max_digits=4)
