from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from insumeter import models
from insumeter import serializers
import datetime
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse

class LogList(APIView):
    """
    List all logs, or create a new entry
    """
    def format_time_db(self, time_string):
        time = "20" + time_string
        time = time.replace('/', '-')
        time = time.replace(',', ' ')
        time = time[0:-3]
        return time

    # maybe get isn't a good idea since no permission is required for post
    def get(self, request, format=None):
        logs = models.Log.objects.all()
        serializer = serializers.LogSerializer(logs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.LogSerializer(data=request.data)
        time = request.data['timestamp']
        print(time)
        time = datetime.datetime.strptime(self.format_time_db(time),
                    "%Y-%m-%d %H:%M:%S")
        request.data['timestamp'] = time
        print(request.data['timestamp'])
        if serializer.is_valid():
            serializer.save()
            return HttpResponse("Success!")
            #return Response(serializer.data, status=status.HTTP_201_CREATED)
        return HttpResponse("Failed!")
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # TODO cannot post if base_id or sensor_id is non-existent. Is this ok?


class UserLogs(APIView):
    """
    Lists the logs related to a given user (identified by user_id)
    """
    # TODO only authenticated
    def get(self, request, user_id, format=None):
        logs = models.Log.objects.filter(sensor_id__base_id__user_id=user_id)
        serializer = serializers.LogSerializer(logs, many=True)
        return Response(serializer.data)

class UserSensors(APIView):
    """
    List all sensors belonging to a given user
    """
    def get(self, request, user_id, format=None):
        sensors = models.Sensor.objects.filter(base_id__user_id=user_id)
        serializer = serializers.SensorSerializer(sensors, many=True)
        return Response(serializer.data)


class UserList(APIView):
    """
    List users, or create a new one
    """
    # TODO maybe get shouldn't be here too
    def get(self, request, format=None):
        users = models.InsumeterUser.objects.all()
        serializer = serializers.InsumeterUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.InsumeterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserDetail(APIView):
    """
    Retrieve, update, or delete
    """
    # TODO only authenticated
    def get(self, request, pk, format=None):
        user = get_object_or_404(models.InsumeterUser, id=pk)
        serializer = serializers.InsumeterUserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = get_object_or_404(models.InsumeterUser, id=pk)
        serializer = serializers.InsumeterUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = get_object_or_404(models.InsumeterUser, id=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class BaseStationList(APIView):
    """
    List base stations belonging to a user, or create one
    """
    # TODO only authenticated
    def get_object(self, user_id):
        try:
            return models.BaseStation.objects.filter(user=user_id)
        except models.BaseStation.DoesNotExist:
            raise Http404

    def get(self, request, user_id, format=None):
        base_stations = self.get_object(user_id)
        serializer = serializers.BaseStationSerializer(base_stations, many=True)
        return Response(serializer.data)

    def post(self, request, user_id, format=None):
        # user is appended from endpoint
        request.data['user'] = user_id
        serializer = serializers.BaseStationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BaseStationDetail(APIView):
    """
    Retrieve, update, or delete a base station
    """
    # TODO add permission here, only admin can change base_id
    def get(self, request, pk, format=None):
        base_station = get_object_or_404(models.BaseStation, base_id=pk)
        serializer = serializers.BaseStationSerializer(base_station)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        base_station = get_object_or_404(models.BaseStation, base_id=pk)
        serializer = serializers.BaseStationSerializer(base_station, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        base_station = get_object_or_404(models.BaseStation, base_id=pk)
        base_station.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SensorList(APIView):
    """
    List all sensors assigned to a base station, or create one
    """
    # TODO permissions? Only user and admin shd be able to add sensors
    def get_object(self, base_id):
        try:
            return models.Sensor.objects.filter(base_id=base_id)
        except models.Sensor.DoesNotExist:
            raise Http404

    def get(self, request, base_id, format=None):
        sensors = self.get_object(base_id)
        serializer = serializers.SensorSerializer(sensors, many=True)
        return Response(serializer.data)

    def post(self, request, base_id, format=None):
        request.data['base_id'] = base_id
        serializer = serializers.SensorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SensorDetail(APIView):
    """
    Retrieve, update, or delete a sensor
    """
    # TODO only authenticated
    def get(self, request, pk, format=None):
        sensor = get_object_or_404(models.Sensor, sensor_id=pk)
        serializer = serializers.SensorSerializer(sensor)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        sensor = get_object_or_404(models.Sensor, sensor_id=pk)
        serializer = serializers.SensorSerializer(sensor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        sensor = get_object_or_404(models.Sensor, id=pk)
        sensor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




def current_datetime():
    """ () -> DateTime

    Returns the current time in the following format:
    YY/MM/DD,HH:MM:SS+T
    where T is Timezone with +00 indicating UTC and so on.

    >>> current_datetime()
    17/03/28,02:05:07+00
    """
    cur_datetime = str(timezone.now())
    cur_datetime1 = cur_datetime[2:19]
    cur_datetime2 = cur_datetime[-6:-3]
    cur_datetime = cur_datetime1 + cur_datetime2
    cur_datetime = cur_datetime.replace('-','/')
    cur_datetime = cur_datetime.replace(' ', ',')
    return cur_datetime

def cur_time(request):
    cur_datetime = current_datetime()
    context = {'time': cur_datetime}
    return render(request, 'insumeter/time.html', context)


def index(request):
    return render(request, 'insumeter/index.html')
