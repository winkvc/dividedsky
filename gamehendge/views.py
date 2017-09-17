# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from .models import Station, STATION_TYPE_IMAGES, StationType, Player

import logic

from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def station_json(station):
    return {
        "position": {"lat": station.lat, "lng": station.lon}, 
        "icon" : STATION_TYPE_IMAGES[StationType(station.station_type)] ,
        "station_type" : StationType(station.station_type).name ,
        "gathered_energy" : station.gathered_energy,
        "db_id" : station.pk
        # later, add the callbackOptions
    }

def station_locations(request):
    #if request.user.is_authenticated():
    stations_list = [station_json(station) for station in Station.objects.all()]

    return JsonResponse({"data" : stations_list})
    #else:
    #    return HttpResponse("Maybe login first?")

def map(request):
	return render(request, 'gamehendge/map.html')

def move_mooks_webpage(request):
    return HttpResponse(logic.move_mooks())

@csrf_exempt
def station_collect_energy(request):
    pk = request.POST["pk"]
    lat = request.POST["latitude"]
    lon = request.POST["longitude"]

    station = Station.objects.get(pk=pk)
    if logic.within((lat, lon), (station.lat, station.lon), 0.1):
        if request.user.is_authenticated:
            if station.owner == Player.objects.get(user=request.user):
                station.owner.energy += station.gathered_energy
                station.gathered_energy = 0
                station.owner.save()
                station.save()

    return JsonResponse({"station_json" : station_json(station)})
    #what? new station description I think.