from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'PyHq.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^characterscreen/', include('PyHq.apps.characterscreen.urls')),
    url(r'^settings/', include('PyHq.apps.settings.urls')),
    url(r'^skillplanner/', include('PyHq.apps.skillplanner.urls')),
    #url(r'^industry/', include('PyHq.apps.industry.urls')),
    url(r'^$', include('PyHq.apps.main.urls')),
    url('^', include('django.contrib.auth.urls'))
)
