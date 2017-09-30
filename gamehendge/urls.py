from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^station_locations/$', views.station_locations, name='station_locations'),
    url(r'^$', views.map, name='map'),
    url(r'^move_mooks_good/$', views.move_mooks_webpage, name='movingmooksgreatagain'),
    url(r'^station_collect_energy/$', views.station_collect_energy),
    url(r'^build_station/$', views.build_station),
    url(r'^delete_station/$', views.delete_station),
    url(r'^change_target/$', views.change_target),
    url(r'^mook_locations/$', views.mook_locations)
]