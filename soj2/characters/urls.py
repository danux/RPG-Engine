from django.conf.urls.defaults import *


urlpatterns = patterns("soj2.characters.views",
        url(r'^application-form/$',
            'application_form', {}, name="application-form"),
        url(r'^application-form/(?P<character_id>[\d]+)/$',
            'application_form', {}, name="amend-application-form"),)

#urlpatterns += patterns("soj2.characters.",
#        url(r'^admin/reject-character-application/(?P<character_id>[\d]+)$',
#            'reject_application_form', {}, name="reject-application-form"),)