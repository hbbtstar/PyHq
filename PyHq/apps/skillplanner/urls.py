from django.conf.urls import patterns, url

from PyHq.apps.skillplanner import views

urlpatterns = patterns('',
    url(r'^api/get_skills/', views.get_skills, name='get_skills'),
    url(r'^api/load_skills/', views.load_skills, name='load_skills'),
    url(r'^$', views.skillplanner, name='skillplanner'),
    url(r'^api/add_to_queue/', views.add_to_queue, name='add_to_queue'),
)