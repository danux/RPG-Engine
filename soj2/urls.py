from django.conf.urls.defaults import *
from mcnulty.urls import *

urlpatterns += patterns("",
                       url(r"^accounts/", include("soj2.accounts.urls", namespace='accounts', )),
                       url(r"^", include("mcnulty.pages.urls")),
)