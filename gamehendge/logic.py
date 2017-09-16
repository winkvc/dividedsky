# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from .models import Mook
import polyline

# a function that moves every mook a little farther in its path
def move_mooks():
	mooks_list = Mook.objects.all()
	return_str = ""
	for mook in mooks_list:
		return_str += str(mook.path)
	#mooks_list = [{
    #        "position": {"lat": station.lat, "lng": station.lon}, 
    #        "icon" : STATION_TYPE_IMAGES[StationType(station.station_type)] 
    #        # later, add the callbackOptions
    #    } for mook in Mook.objects.all()]

	decoded_polylines = [{str(polyline.decode(mook.path.encoded_polyline))}for mook in mooks_list]
	#encoded_example = "_p~iF~ps|U_ulL~ugC_hgN~eq`@"
	#return_str = polyline.decode(encoded_example)
	return_str = str(decoded_polylines)

	return return_str
