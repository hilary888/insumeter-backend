from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from datetime import datetime


class InsumeterUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username       # Think about last name instead


# Handles OneToOneField backward deletion. InsumeterUser del -> User del
@receiver(post_delete, sender=InsumeterUser)
def post_delete_user(sender, instance, *args, **kwargs):
    if instance.user:       # Just in case user is not specified
        instance.user.delete()


class BaseStation(models.Model):
    base_id = models.CharField(primary_key=True, max_length=10, null=False, unique=True)
    region = models.CharField(max_length=50)
    user = models.ForeignKey(InsumeterUser, related_name='base_station_set')
    nickname = models.CharField(max_length=100, null=True)     # For easy identification by user

    def __str__(self):
        return self.base_id
# TODO increase max number of sensors since more sensors will be in use compated to base stations. Many to one.


class Sensor(models.Model):
    sensor_id = models.CharField(primary_key=True, max_length=10, null=False, unique=True)
    base_id = models.ForeignKey(BaseStation)
    nickname = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.sensor_id

    def base_id_to_string():
        base_name = base_id
        return str(base_name)

class Log(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    level_reading = models.DecimalField(null=False, decimal_places=2, max_digits=5)
    base_station_id = models.ForeignKey(BaseStation)
    sensor_id = models.ForeignKey(Sensor)
    power_level = models.DecimalField(null=False, decimal_places=2, max_digits=5)
    user = models.ForeignKey(InsumeterUser)
