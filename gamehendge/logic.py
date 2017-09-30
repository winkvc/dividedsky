# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.db import transaction

from .models import Mook, Station, StationType
import polyline
import math

# gives distance (in miles) between two (lat,lon) points
def great_circle_distance(lat1, lon1, lat2, lon2):
	radius = 3959.
	dlat = math.radians(lat1-lat2)
	dlon = math.radians(lon2-lon1)
	a = math.sin(dlat/2.) * math.sin(dlat/2.) + math.cos(math.radians(lat1)) \
		* math.cos(math.radians(lat2)) * math.sin(dlon/2.) * math.sin(dlon/2.)
	c = 2. * math.atan2(math.sqrt(a), math.sqrt(1.-a))
	d = radius * c
	return d


# a function that moves every mook a little farther in its path
# for now, assumes first lat,lon in polyline is exactly where the mook starts
# does a choppy polyline follow (does not interpolate between points; a problem if polyline points are far apart)
def move_mooks():
	mook_speed = .3 # in miles per hour
	mooks_list = Mook.objects.all()
	mook_new_lat_lon_list = []
	for mook in mooks_list:

		mook_new_lat_lon = [mook.lat, mook.lon]
		# have mook follow the polyline from its starting position (beginning of polyline) for a distance
		# according to how long it has been in existence and how fast it moves
		print len(mook.path.encoded_polyline)
		print mook.path.encoded_polyline
		print type(mook.path.encoded_polyline)

		print (mook.path.encoded_polyline == u"ssmcFd}thVa@xC_@S]KyG{AiAUu@Os@UqBkAa@_@S_@c@b@b@n@^b@n@b@j@VbAZRB~A@b@DvG~Af@NZTPRPf@Fb@?|@YvBMrAMbBW`Dm@vEEr@Hv@F`@ZpA`@t@h@v@^\\^Vd@Vv@PRBTFALIp@Id@Qn@Yn@a@h@s@|@Yn@Uv@K`AI~GIj@Mn@g@z@s@b@w@RYNm@f@[^pDxF|ElHzAvB~AnBjBpBn@`@pAj@dCtA|@l@j@b@bAjAjAhBhDxFbHbLvAjCzAxDb@vAv@dDPx@")

		points = polyline.decode(mook.path.encoded_polyline)
		print mook.mook_type
		#print points
		#print mook.lat
		#print mook.lon
		#print mook.launch_time
		#print timezone.now()
		travel_time = (timezone.now() - mook.launch_time).total_seconds() / 3600. # in hours
		#print travel_time
		distance_to_travel = mook_speed * travel_time
		#print distance_to_travel
		distance_travelled = 0.
		for i in range(0,len(points)-1):
			lat1 = points[i][0]
			lon1 = points[i][1]
			lat2 = points[i+1][0]
			lon2 = points[i+1][1]
			distance_travelled += great_circle_distance(lat1,lon1,lat2,lon2)
			if distance_travelled < distance_to_travel:
				print 'mook lat,lon updated'
				# this is where you want to update the mook's lat,lon like this
				mook.lat = lat2
				mook.lon = lon2
				


			#print 'lat1'
			#print lat1
			#print points[i]
			#print i

		mook_new_lat_lon_list.append(mook_new_lat_lon)
		#return_str += str(polyline.decode(mook.path.encoded_polyline))
		#return_str += str(mook.path)
	#mooks_list = [{
    #        "position": {"lat": station.lat, "lng": station.lon}, 
    #        "icon" : STATION_TYPE_IMAGES[StationType(station.station_type)] 
    #        # later, add the callbackOptions
    #    } for mook in Mook.objects.all()]

	#decoded_polylines = [{str(polyline.decode(mook.path.encoded_polyline))}for mook in mooks_list]
	#encoded_example = "_p~iF~ps|U_ulL~ugC_hgN~eq`@"
	#return_str = polyline.decode(encoded_example)
	#return_str = str(decoded_polylines)

	#return_str = str(great_circle_distance(37.423128,-122.200249,37.424231,-122.198296))

	#return_str = polyline.encode([(37.424622,-122.194203),(37.423898,-122.195737),(37.424128,-122.197862)],5)

	with transaction.atomic():
		for mook in mooks_list:
			mook.save()

def within(latlon1, latlon2, miles):
	# TODO: write code to check distance
	return True

def credit_energy():
	# get all energy towers
	energy_towers = Station.objects.filter(station_type = StationType["energy"].value)

	#print len(energy_towers)

	# add one to their gathered_energy
	for tower in energy_towers:
		tower.gathered_energy += 1
		if tower.gathered_energy > 10:
			tower.gathered_energy = 10
		#print tower.gathered_energy

	# update
	with transaction.atomic():
		for tower in energy_towers:
			tower.save()