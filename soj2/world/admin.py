from django.contrib import admin
from django.contrib.admin import site

from soj2.world.models import Race, Town, Nation


site.register(Race)
site.register(Town)
site.register(Nation)