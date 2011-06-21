from django.conf.urls.defaults import *

urlpatterns = patterns("soj2.game.views",
                       url(r'^$',
                           'realm', 
                           name="realm"),
                       url(r'^town/(?P<town_id>.*)/$',
                           'view_town', 
                           name="view-town"),
                       url(r'^create-quest/$',
                           'create_quest', 
                           name="create-quest"),)