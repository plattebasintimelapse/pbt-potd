from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^archives/$', views.archive, name="archive"),
    url(r'^archives/(?P<slug>[-\w]+)/$', views.archive_camera, name="archive_camera"),
    url(r'^archives/(?P<slug>[-\w]+)/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', views.archive_camera_day, name="archive_camera_day"),
    url(r'^(?P<slug>[-\w]+)/$', views.camera, name='camera'),
]