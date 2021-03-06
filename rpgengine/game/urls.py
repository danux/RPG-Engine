from django.conf.urls.defaults import *

urlpatterns = patterns("rpgengine.game.views",
                       url(r'^$',
                           'realm', 
                           name="realm"),
                       url(r'^(?P<town_slug>[\w-]+)/create-quest/$',
                           'create_quest', 
                           name="create-quest"),
                       url(r'^(?P<town_slug>[\w-]+)/(?P<quest_slug>[\w-]+)/join/$',
                           'join_quest', 
                           name="join-quest"),
                      url(r'^(?P<town_slug>[\w-]+)/(?P<quest_slug>[\w-]+)/leave/$',
                          'leave_quest', 
                          name="leave-quest"),
#                       url(r'^(?P<town_slug>[\w-]+)/(?P<quest_slug>[\w-]+)/make-leader/$',
#                           'make_quest_leader', 
#                           name="make-quest-leader"),
#                       url(r'^(?P<town_slug>[\w-]+)/(?P<quest_slug>[\w-]+)/remove-leader/$',
#                           'remove_quest_leader', 
#                           name="remove-quest-leader"),
                       url(r'^(?P<town_slug>[\w-]+)/(?P<quest_slug>[\w-]+)/$',
                           'view_quest', 
                           name="view-quest"),
                       url(r'^(?P<town_slug>[\w-]+)/$',
                           'view_town', 
                           name="view-town"),)