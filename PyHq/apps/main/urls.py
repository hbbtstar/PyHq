from django.conf.urls import patterns, url, include

from PyHq.apps.main import views

urlpatterns = patterns('',
    #url(r'^debug$', views.debug, name='debug'),
    url(r'^$', views.main_view, name='main_view'),

)