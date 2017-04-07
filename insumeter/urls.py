from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^time/$', views.cur_time, name='cur_time'),
    url(r'^logs/$', views.LogList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
