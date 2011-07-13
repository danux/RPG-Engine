from django.conf.urls.defaults import *


urlpatterns = patterns("rpgengine.characters.views",
        url(r'^application-form/$',
            'application_form', {}, name="application-form"),
        url(r'^application-form/(?P<character_id>[\d]+)/$',
            'application_form', {}, name="amend-application-form"),)

urlpatterns += patterns("rpgengine.characters.admin_views",
        url(r'^admin/character-application/reject/(?P<character_id>[\d]+)/$',
            'reject_application_form', {}, name="reject-application-form"),
        url(r'^admin/character-application/approve/(?P<character_id>[\d]+)/$',
            'approve_application_form', {}, name="approve-application-form"),)