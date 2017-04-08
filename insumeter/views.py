from django.shortcuts import render
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from insumeter import models
from insumeter.serializers import LogSerializer
import datetime

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

    def get(self, request, format=None):
        logs = models.Log.objects.all()
        serializer = LogSerializer(logs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LogSerializer(data=request.data)
        time = request.data['timestamp']
        print(time)
        time = datetime.datetime.strptime(self.format_time_db(time),
                    "%Y-%m-%d %H:%M:%S")
        request.data['timestamp'] = time
        print(request.data['timestamp'])
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # TODO cannot post if base_id or sensor_id is non-existent. Is this ok?

class UserList(APIView):
    """
    List users, or create a new one
    """
    def get(self, request, format=None):
        users = models.InsumeterUser.objects.all()
        s

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


def index(request):
    return render(request, 'insumeter/index.html')

def cur_time(request):
    cur_datetime = current_datetime()
    context = {'time': cur_datetime}
    return render(request, 'insumeter/time.html', context)
