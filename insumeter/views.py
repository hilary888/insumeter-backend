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
from django.http import HttpResponse, JsonResponse
from datetime import datetime

class LogList(APIView):
    """
    List all logs, or create a new entry
    """
    alert_time_diff = False
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
        time = datetime.strptime(self.format_time_db(time),
                    "%Y-%m-%d %H:%M:%S")
        #request.data['timestamp'] = time


        if serializer.is_valid():
            serializer.save()
            if str(request.data['timestamp'])[:-5] == str(time)[:5]:
                print(request.data['timestamp'])
                print(time)
                return HttpResponse("success")
            else:
                cur_time = current_datetime()
                return HttpResponse(cur_time)
                #return Response(serializer.data, status=status.HTTP_201_CREATED)
            #return HttpResponse("1")
        #return HttpResponse("0")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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



class TankHeight(APIView):
    """
    Retrieve the height of a given sensor's tank
    """
    def get(self, request, sensor_id, format=None):
        sensor = get_object_or_404(models.Sensor, sensor_id=sensor_id)
        serializer = serializers.TankHeightSerializer(sensor)
        return Response(serializer.data)


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

def get_day_readings(request, sensor_id, date):
    # convert date string into datetime object
    selected_date = datetime.strptime(date, '%Y-%m-%d')
    day_readings = models.Log.objects.filter(sensor_id=sensor_id, timestamp__contains=selected_date.date())
    #print(day_readings.values())
    hour_readings = {}
    for reading in list(day_readings.values()):
        hour_readings[reading['timestamp'].hour] = []

    for reading in list(day_readings.values()):
        if reading['timestamp'].hour in hour_readings:
            hour_readings[reading['timestamp'].hour].append(float(reading['level_reading']))

    hour_water_used = []
    for key, value in hour_readings.items():
        hour_water_used.append(get_water_used(value))

    hour_labels = []
    for hour in hour_readings.keys():
        hour_labels.append(hour)

    hour_response = dict(zip(hour_labels, hour_water_used))
    return JsonResponse(hour_response)
    #print(hour_readings)
    #return JsonResponse(day_readings.values(), safe=False)
    #return HttpResponse("sth")


def get_week_readings(request, sensor_id):
    week_time_threshold = timezone.now() - timezone.timedelta(days=7)
    week_readings = models.Log.objects.filter(sensor_id=sensor_id, timestamp__gt=week_time_threshold)
    # daily_readings = {week_readings.timestamp.date():week_readings.level_reading for reading in week_readings}
    #ls = [week_readings.timestamp for reading in week_readings]
    day_readings = {}

    #print(list(week_readings.values()))
    for reading in list(week_readings.values()):
        #print(reading['timestamp'].date())
        day_readings[reading['timestamp'].date()] = []
    print(day_readings)

    for reading in list(week_readings.values()):
        if reading['timestamp'].date() in day_readings:
            day_readings[reading['timestamp'].date()].append(float(reading['level_reading']))
    #print(week_readings.values()[0])

    days = {0: "Sunday", 1:"Monday",
            2: "Tuesday", 3: "Wednesday",
            4: "Thursday", 5: "Friday",
            6: "Saturday"}
    day_labels = []
    for day in day_readings.keys():
        #day_labels.append(day.strftime("%d/%m/%y"))
        day_labels.append(days[day.weekday()])

    week_water_used = []
    # calculate the actual amount of water used
    for key, value in day_readings.items():
        week_water_used.append(get_water_used(value))
    #print(week_water_used)
    #print(day_labels)
    week_response = dict(zip(day_labels, week_water_used))
    return JsonResponse(week_response)


def get_year_readings(request, sensor_id):
    # 11 months -> 47.7977 weeks
    month_time_threshold = timezone.now() - timezone.timedelta(days=334.584)
    year_readings = models.Log.objects.filter(sensor_id=sensor_id, timestamp__gt=month_time_threshold)
    month_readings = {}

    #create dict with empty
    for reading in list(year_readings.values()):
        #print(reading['timestamp'].month)
        month_readings[reading['timestamp'].month] = []

    #print(reading['timestamp'].month)
    #print(type(month_readings.values()))

    for reading in list(year_readings.values()):
        if reading['timestamp'].month in month_readings.keys():
            month_readings[reading['timestamp'].month].append(float(reading['level_reading']))

    months = {1: 'January', 2: 'February', 3: 'March',
            4: 'April', 5: 'May', 6: 'June',
            7: 'July', 8: 'August', 9: 'September',
            10: 'October', 11: 'November', 12: 'December'}

    months2 = {
    {"Monday"}
    }

    month_labels = []
    # convert the months from month number to month name
    for month in month_readings.keys():
        month_labels.append(months[month])

    year_water_used = []
    # calculate the actual amount of water used
    for key, value in month_readings.items():
        year_water_used.append(get_water_used(value))

    year_response = dict(zip(month_labels, year_water_used))
    return JsonResponse(year_response)


def get_water_used(water_levels):
    """ Determines the amount of water used """
    total = 0
    for index, level in enumerate(water_levels):
        next = index + 1
        if next < len(water_levels):
            diff = level - water_levels[next]
            if diff >= 0:
                total += diff
    return total
