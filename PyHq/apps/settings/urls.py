from django.conf.urls import patterns, url

from PyHq.apps.settings import views

urlpatterns = patterns('',
    url(r'^$', views.settings, name='settings'),
)