from django.conf.urls.defaults import *


urlpatterns = patterns("soj2.characters.views",
        url(r'^application-form/$',
            'application_form', {}, name="application-form"),
        url(r'^application-form/(?P<character_id>[\d]+)/$',
            'application_form', {}, name="amend-application-form"),)