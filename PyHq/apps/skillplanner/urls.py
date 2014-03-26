from django.conf.urls import patterns, url

from PyHq.apps.skillplanner import views

urlpatterns = patterns('',
    url(r'^api/get_skills/', views.get_skills, name='get_skills'),
    url(r'^$', views.skillplanner, name='skillplanner'),
)