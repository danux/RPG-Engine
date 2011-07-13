from django.contrib.admin import site, ModelAdmin
from rpgengine.characters.models import Character


site.register(Character, ModelAdmin)