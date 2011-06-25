from django.conf.urls.defaults import *

urlpatterns = patterns("soj2.game.views",
                       url(r'^$',
                           'realm', 
                           name="realm"),
                       url(r'^create-quest/$',
                           'create_quest', 
                           name="create-quest"),
                       url(r'^(?P<town_slug>[\w-]+)/(?P<quest_slug>.*)/$',
                           'view_quest', 
                           name="view-quest"),
                       url(r'^(?P<town_slug>[\w-]+)/$',
                           'view_town', 
                           name="view-town"),)