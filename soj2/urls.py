from django.conf.urls.defaults import *
from mcnulty.urls import *

urlpatterns += patterns("",
                       url(r"^accounts/",
                           include("soj2.accounts.urls", 
                                   namespace='accounts', )),
                       url(r"^characters/",
                           include("soj2.characters.urls", 
                                   namespace='characters', )),
                       url(r"^", include("mcnulty.pages.urls")),)