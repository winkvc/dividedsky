from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^station_locations/$', views.station_locations, name='station_locations'),
    url(r'^$', views.map, name='map'),
    url(r'^move_mooks_good/$', views.move_mooks_webpage, name='movingmooksgreatagain'),
    url(r'^station_collect_energy/$', views.station_collect_energy)
]