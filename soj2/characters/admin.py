from django.contrib.admin import site, ModelAdmin
from soj2.characters.models import Character


site.register(Character, ModelAdmin)