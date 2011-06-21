"""Views used by the characters application."""
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from soj2.game.forms import CreateQuestForm
from soj2.game.models import Quest
from soj2.world.models import Nation, Town

def realm(request):
    nations = Nation.objects.all()
    context = { 'nations' : nations }
    return render_to_response("game/realm.html", 
                              context, RequestContext(request))

def view_town(request, town_id):
    town = get_object_or_404(Town, slug=town_id)
    context = { 'town' : town }
    return render_to_response("game/view-town.html", 
                              context, RequestContext(request))

@login_required
def create_quest(request):
    """
    View that allows members to create a quest
    """
    form = CreateQuestForm()
    form.set_character_queryset(Quest.available_characters_by_user(
        request.user))
    
    context = { 'form' : form }
    return render_to_response("game/create-quest.html", 
                              context, RequestContext(request))