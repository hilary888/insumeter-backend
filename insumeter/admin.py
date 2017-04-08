from django.contrib import admin
from insumeter import models

admin.site.register(models.Log)       # for logs to appear in admin
admin.site.register(models.BaseStation)    # for base station
admin.site.register(models.Sensor)
admin.site.register(models.InsumeterUser)       # for users
