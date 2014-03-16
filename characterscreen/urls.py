from django.conf.urls import patterns, url

from characterscreen import views

urlpatterns = patterns('',
    url(r'index$', views.character, name='character'),
    url(r'^settings$', views.settings, name='settings'),
)