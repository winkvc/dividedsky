# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from enum import Enum
from django.utils import timezone

# Create your models here.

class Team(Enum):
	red = 1
	blue = 2
TEAM_CHOICES = ((team.value, team.name) for team in Team)

class StationType(Enum):
	energy = 1
	shooters = 2
	lightning = 3
STATION_TYPE_CHOICES = ((station_type.value, station_type.name) for station_type in StationType)

STATION_TYPE_IMAGES = {
	StationType.energy: "https://img.pokemondb.net/sprites/ruby-sapphire/{}/ditto.png",
	StationType.shooters: "https://img.pokemondb.net/sprites/ruby-sapphire/{}/hitmonchan.png",
	StationType.lightning: "https://img.pokemondb.net/sprites/ruby-sapphire/{}/raichu.png",
}

class MookType(Enum):
    shooters = 2
    lightning = 3
MOOK_TYPE_CHOICES = ((mook_type.value, mook_type.name) for mook_type in MookType)

MOOK_TYPE_IMAGES = {
    MookType.shooters: "https://img.pokemondb.net/sprites/ruby-sapphire/{}/tyrogue.png",
    MookType.lightning: "https://img.pokemondb.net/sprites/ruby-sapphire/{}/pikachu.png",
}

class Player(models.Model):
    user = models.ForeignKey(User)
    energy = models.IntegerField()
    team = models.IntegerField(choices=TEAM_CHOICES)
    phone_number = models.CharField(max_length=50, blank=True)

    def __str__(self):
    	return str(self.user)

class Station(models.Model):
    station_type = models.IntegerField(choices=STATION_TYPE_CHOICES, default=StationType.energy)
    team = models.IntegerField(choices=TEAM_CHOICES)
    lat = models.FloatField()
    lon = models.FloatField()
    target = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(Player, on_delete=models.CASCADE)
    gathered_energy = models.IntegerField(default=0)
    health = models.IntegerField(default=100)

    def __str__(self):
    	return str(self.owner) + "'s " + StationType(self.station_type).name + " station"

class Path(models.Model):
    source = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="source_paths")
    dest = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="dest_paths")
    encoded_polyline = models.TextField()

    def __str__(self):
        return str(self.source) + " TO " + str(self.dest)

class Mook(models.Model):
    mook_type = models.IntegerField(choices=STATION_TYPE_CHOICES)
    team = models.IntegerField(choices=TEAM_CHOICES)
    path = models.ForeignKey(Path, on_delete=models.CASCADE)
    launch_time = models.DateTimeField(default=timezone.now)
    lat = models.FloatField()
    lon = models.FloatField()
    health = models.IntegerField(default=25)

    @property
    def owner(self):
        return self.path.source.owner

    def __str__(self):
        return "MOOK TYPE " + str(self.mook_type) + " PATH " + str(self.path)