from django.conf.urls import patterns, url

from PyHq.apps.characterscreen import views

urlpatterns = patterns('',
    url(r'^$', views.character, name='character'),
    url(r'^settings$', views.settings, name='settings'),
)