from django.conf.urls import patterns, url

from PyHq.apps.skillplanner import views

urlpatterns = patterns('',
    url(r'^$', views.skillplanner, name='skillplanner'),
)