# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from .models import Player, Station, Path, Mook

admin.site.register(Player)
admin.site.register(Station)
admin.site.register(Path)
admin.site.register(Mook)