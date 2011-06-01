from mcnulty.dashboard.admin import site
from mcnulty.media import admin
from mcnulty.contentpages import admin
from mcnulty.news import admin
from mcnulty.media.models import File

site._registered_links.clear()
site.register_link(File)

