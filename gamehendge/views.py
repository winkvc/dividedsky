# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from .models import Station, STATION_TYPE_IMAGES, StationType

import logic

# Create your views here.

def station_locations(request):
    #if request.user.is_authenticated():
    stations_list = [{
            "position": {"lat": station.lat, "lng": station.lon}, 
            "icon" : STATION_TYPE_IMAGES[StationType(station.station_type)] 
            # later, add the callbackOptions
        } for station in Station.objects.all()]

    return JsonResponse({"data" : stations_list})
    #else:
    #    return HttpResponse("Maybe login first?")

def map(request):
	return render(request, 'gamehendge/map.html')

def move_mooks_webpage(request):
    return HttpResponse(logic.move_mooks())