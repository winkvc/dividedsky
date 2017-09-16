from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^station_locations/$', views.station_locations, name='station_locations'),
    url(r'^$', views.map, name='map'),
    url(r'^move_mooks_good/$', views.move_mooks_webpage, name='movingmooksgreatagain')
]