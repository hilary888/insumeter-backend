from rest_framework import serializers
from insumeter.models import Log

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ('base_station_id', 'sensor_id', 'power_level', 'level_reading',
                    'timestamp')

class InsumeterUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'username', 'password')
