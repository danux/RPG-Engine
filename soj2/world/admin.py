from django.contrib import admin

from mcnulty.dashboard.admin import VertexModelAdmin, site
from mcnulty.pages.admin import PageAdmin

from soj2.world.models import Race, Language, Town, Nation


site.register(Race, VertexModelAdmin)
site.register(Language, VertexModelAdmin)
site.register(Town, VertexModelAdmin)
site.register(Nation, VertexModelAdmin)