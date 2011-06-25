from django.conf.urls.defaults import *
from django.contrib import admin


urlpatterns = patterns("",
                       (r'^admin/', include(admin.site.urls)),
                       url(r"^accounts/",
                           include("soj2.accounts.urls", 
                                   namespace='accounts', )),
                       url(r"^characters/",
                           include("soj2.characters.urls", 
                                   namespace='characters', )),
                       url(r"^game/",
                           include("soj2.game.urls", 
                                   namespace='game', )),)