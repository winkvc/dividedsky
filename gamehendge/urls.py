from django.conf.urls import url

from . import views

from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^station_locations/$', views.station_locations, name='station_locations'),
    url(r'^$', views.map, name='map'),
#    url(r'^/', views.map, name='map'),
    url(r'^move_mooks_good/$', views.move_mooks_webpage, name='movingmooksgreatagain'),
    url(r'^station_collect_energy/$', views.station_collect_energy),
    url(r'^build_station/$', views.build_station),
    url(r'^delete_station/$', views.delete_station),
    url(r'^change_target/$', views.change_target),
    url(r'^mook_locations/$', views.mook_locations),
    url(r'^text_mark/$', views.text_mark),
    url(r'^$', views.map, name='login'),
#               {'authentication_form': 'templates/gamehendge/map.html'},
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^admin/', admin.site.urls),
]
