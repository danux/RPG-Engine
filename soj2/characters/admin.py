from mcnulty.dashboard.admin import VertexModelAdmin, site

from soj2.characters.models import Character

site.register(Character, VertexModelAdmin)