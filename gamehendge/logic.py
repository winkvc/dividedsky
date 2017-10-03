# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.db import transaction

from .models import Mook, MookType, Station, StationType, Path
import polyline
import math
import googlemaps
from random import shuffle

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


# a function that calculates every mook a little farther in its path
# for now, assumes first lat,lon in polyline is exactly where the mook starts
# does a choppy polyline follow (does not interpolate between points; a problem if polyline points are far apart)
def move_mooks():
	mook_speed = .3 # in miles per hour
	mooks_list = Mook.objects.all()
	moved_mooks = []
	exploding_mooks = []
	for mook in mooks_list:

		mook_new_lat_lon = [mook.lat, mook.lon]
		# have mook follow the polyline from its starting position (beginning of polyline) for a distance
		# according to how long it has been in existence and how fast it moves
		points = polyline.decode(mook.path.encoded_polyline)
		travel_time = (timezone.now() - mook.launch_time).total_seconds() / 3600. # in hours
		distance_to_travel = mook_speed * travel_time
		distance_travelled = 0.
		mook.lat = points[0][0]
		mook.lon = points[0][1]
		for i in range(0,len(points)-1):
			lat1 = points[i][0]
			lon1 = points[i][1]
			lat2 = points[i+1][0]
			lon2 = points[i+1][1]
			distance_travelled += great_circle_distance(lat1,lon1,lat2,lon2)
			if distance_travelled < distance_to_travel:
				mook.lat = lat2
				mook.lon = lon2
		
		if distance_to_travel > distance_travelled:
			exploding_mooks.append(mook)
		else:
			moved_mooks.append(mook)

	with transaction.atomic():
		for mook in moved_mooks:
			mook.save()
		targets = set()
		for mook in exploding_mooks:
			# TODO: unhardcode this
			target = mook.path.dest
			target.health -= 25
			mook.delete()
			targets.add(target)

		for target in targets:
			if target.health <= 0:
				target.delete()
			else:
				target.save()
		


def within(latlon1, latlon2, miles):
	# TODO: write code to check distance
	(lat1, lon1) = latlon1
	(lat2, lon2) = latlon2

	return great_circle_distance(lat1, lon1, lat2, lon2) <= miles

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

def sort_by_initiative(list_of_mooks_and_towers):
	shuffle(list_of_mooks_and_towers)
	return list_of_mooks_and_towers

def calculate_shooter_attack(attacker, sorted_attackers):

	closest = None
	best_distance = 0.3

	for defender in sorted_attackers:
		# todo: unmagicnumber this line
		if attacker.owner != defender.owner:
			distance = great_circle_distance(attacker.lat, attacker.lon, defender.lat, defender.lon)
			if distance <= best_distance:
				closest = defender
				best_distance = distance

	attacker_damage = 2
	if type(attacker) == Station:
		attacker_damage = 3

	if closest:
		closest.health -= attacker_damage

def calculate_lightning_attack(attacker, sorted_attackers):

	# TODO: unhardcode
	threshold_distance = 0.3
	defenders = []

	for defender in sorted_attackers:
		# todo: unmagicnumber this line
		if attacker.owner != defender.owner:
			distance = great_circle_distance(attacker.lat, attacker.lon, defender.lat, defender.lon)
			if distance <= threshold_distance:
				defenders.append(defender)

	attacker_damage = 1
	if type(attacker) == Station:
		attacker_damage = 2

	for defender in defenders:
		defender.health -= attacker_damage

def calculate_attacks():
	# get all attacking objects
	all_attackers = [m for m in Mook.objects.all()] + [s for s in Station.objects.all()]

	# sort by initiative
	sorted_attackers = sort_by_initiative(all_attackers)

	# run damange
	for attacker in sorted_attackers:
		if attacker.health <= 0:
			continue

		attacker_type_name = None
		if type(attacker) == Mook:
			attacker_type_name = MookType(attacker.mook_type).name
		elif type(attacker) == Station:
			attacker_type_name = StationType(attacker.station_type).name
		else:
			print 'Fell through with type: ' + str(type(attacker))

		if attacker_type_name == 'shooters':
			calculate_shooter_attack(attacker, sorted_attackers)
		elif attacker_type_name == 'lightning':
			calculate_lightning_attack(attacker, sorted_attackers)
		else:
			print 'Fell through with attacker_type: ' + attacker_type_name

	for attacker in sorted_attackers:
		if attacker.health > 0 and type(attacker) == Station:
			attacker.health += 1
			if attacker.health > 100:
				attacker.health = 100

	with transaction.atomic():
		for attacker in sorted_attackers:
			if attacker.health > 0:
				attacker.save()
			else:
				attacker.delete()

def spawn_mooks():
	# get all stations
	stations = Station.objects.all()
	new_mooks = []

	gmaps = None

	# for each station
	for station in stations:
		# if they have a target and they aren't energy
		if station.target and station.station_type != StationType.energy:
			# create a mook

			# ensure the path exists:
			paths = Path.objects.filter(source=station, dest=station.target)
			print len(paths)

			if len(paths) == 0:
				# gotta make one
				if gmaps == None:
					gmaps = googlemaps.Client(key='AIzaSyBEEyNDsD9uaj2k2B07mtt_yEbDeuMVM84')
				directions = gmaps.directions(
					{u'lat': station.lat, u'lng': station.lon},
					{u'lat': station.target.lat, u'lng': station.target.lon},
					mode="driving")

				path_polyline = directions[0]['overview_polyline']['points']

				new_path = Path(
					source = station, dest = station.target,
					encoded_polyline = path_polyline
				)
				new_path.save()

				paths = [new_path]


			mook = Mook(
				mook_type=station.station_type,
				team=station.team,
				lat=station.lat,
				lon=station.lon,
				path=paths[0]
			)

			new_mooks.append(mook)

	with transaction.atomic():
		for mook in new_mooks:
			mook.save()

