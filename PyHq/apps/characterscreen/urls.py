from django.conf.urls import patterns, url

from PyHq.apps.characterscreen import views

urlpatterns = patterns('',
    url(r'^debug$', views.debug, name='character'),
    url(r'^$', views.character, name='character'),

)