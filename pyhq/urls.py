from django.conf.urls import patterns, url

from pyhq import views

urlpatterns = patterns('',
    url(r'^character$', views.character, name='character'),
    url(r'^settings$', views.settings, name='settings'),
)