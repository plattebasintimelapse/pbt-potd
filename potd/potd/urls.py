from django.conf.urls import patterns, include, url
from django.contrib import admin
import timelapse
from timelapse import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'potd.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', timelapse.views.index, name='index'),
    url(r'^archives/$', timelapse.views.archive, name="archive"),
    url(r'^archives/(?P<slug>[-\w]+)/$', timelapse.views.archive_camera, name="archive_camera"),
    url(r'^archives/(?P<slug>[-\w]+)/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', timelapse.views.archive_camera_day, name="archive_camera_day"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<slug>[-\w]+)/$', timelapse.views.camera, name='camera'),
)
