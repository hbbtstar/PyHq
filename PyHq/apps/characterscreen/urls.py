from django.conf.urls import patterns, url

from PyHq.apps.characterscreen import views

urlpatterns = patterns('',
    url(r'^debug$', views.debug, name='debug'),
    url(r'^$', views.character, name='character_overview'),

)