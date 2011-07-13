from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns("",
                       (r'^admin/', include(admin.site.urls)),
                       url(r"^accounts/",
                           include("rpgengine.accounts.urls", 
                                   namespace='accounts', )),
                       url(r"^characters/",
                           include("rpgengine.characters.urls", 
                                   namespace='characters', )),
                       url(r"^game/",
                           include("rpgengine.game.urls", 
                                   namespace='game', )),)