from rest_framework import serializers
from insumeter import models
from django.contrib.auth import get_user_model


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Log
        fields = ('user', 'base_station_id', 'sensor_id', 'power_level',
                    'level_reading', 'timestamp')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')


class InsumeterUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = models.InsumeterUser
        fields = ('id', 'email_verified', 'user')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = get_user_model().objects.create_user(**user_data)
        insumeter_user = models.InsumeterUser.objects.create(user=user, **validated_data)
        return insumeter_user
        # base, sensor, base/user, sensor/base, login/ logoout,  registration,


class BaseStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BaseStation
        fields = ('base_id', 'region', 'nickname', 'user')


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sensor
        fields = ('sensor_id', 'base_id', 'nickname')
