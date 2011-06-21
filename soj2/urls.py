from django.conf.urls.defaults import *
from mcnulty.urls import *

urlpatterns += patterns("",
                       url(r"^accounts/",
                           include("soj2.accounts.urls", 
                                   namespace='accounts', )),
                       url(r"^characters/",
                           include("soj2.characters.urls", 
                                   namespace='characters', )),
                       url(r"^game/",
                           include("soj2.game.urls", 
                                   namespace='game', )),
                       url(r"^", include("mcnulty.pages.urls")),)