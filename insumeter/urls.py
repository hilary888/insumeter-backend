from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # insumeter/time/
    url(r'^time/$', views.cur_time, name='cur_time'),
    # insumeter/logs/
    url(r'^logs/$', views.LogList.as_view()),
    # insumeter/<user_id>/                              - logs based on user
    url(r'^logs/(?P<user_id>[0-9]+)/$', views.UserLogs.as_view()),
    # insumeter/users/
    url(r'^users/$', views.UserList.as_view()),
    # insumeter/users/<user_id>/
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    # insumeter/base-stations/<user_id>                 - base stations belonging to a user
    url(r'^base-stations/(?P<user_id>[0-9]+)/$', views.BaseStationList.as_view()),
    # insumeter/base-stations/<base_station_id>/        - base station details.
    url(r'^base-station/(?P<pk>B[0-9]+)/$', views.BaseStationDetail.as_view()),
    # insumeter/sensors/<base_id>/                      - sensors belonging to a base_station
    url(r'^sensors/(?P<base_id>B[0-9]+)/$', views.SensorList.as_view()),
    # insumeter/sensor/<sensor_id>/                     - details of a sensor
    url(r'^sensor/(?P<pk>S[0-9]+)/$', views.SensorDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
