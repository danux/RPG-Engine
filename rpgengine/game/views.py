"""Views used by the main game."""
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from rpgengine.characters.models import Character
from rpgengine.game.forms import CreateQuestForm, QuestForm
from rpgengine.game.models import Quest
from rpgengine.world.models import Nation, Town
from rpgengine.utils.error_handler import handle_error


def realm(request):
    """
    Overview, or default game view. Displays a list of all towns, as well
    as info about their current state.
    """
    nations = Nation.objects.all()
    context = { 'nations' : nations }
    return render_to_response("game/realm.html", 
                              context,
                              RequestContext(request))

def view_town(request, town_slug):
    """
    Allows a user to see what is going on in a town, who is there, what
    quests there are, and also link to create a quest.
    """
    town = get_object_or_404(Town, slug=town_slug)
    context = { 'town' : town }
    return render_to_response("game/view-town.html", 
                              context,
                              RequestContext(request))

def view_quest(request, town_slug, quest_slug):
    """
    Allows a user to browse an actual quest, read previous posts and links
    to joining the quest.
    """
    quest = get_object_or_404(Quest, slug=quest_slug, town__slug=town_slug)
    context = { 'quest' : quest }
    return render_to_response("game/view-quest.html", 
                              context,
                              RequestContext(request))

@login_required
def create_quest(request, town_slug):
    """
    View that allows members to create a quest
    """
    town = get_object_or_404(Town, slug=town_slug)
    queryset = Character.available_characters_by_user(request.user)
    
    if len(queryset) < 1:
        return handle_error(request,
                            u'You do not have any available characters.',
                            town.get_absolute_url())
    
    if request.method == 'POST':
        form = CreateQuestForm(request.POST,
                               queryset=queryset)
        if form.is_valid():
            quest = form.save(commit=False)
            quest.is_open = True
            quest.town = town
            quest.save()
            quest.set_initial_member(form.cleaned_data['character'])
            return HttpResponseRedirect(quest.get_absolute_url())
    else:
        form = CreateQuestForm(queryset=queryset)
    context = { 'form' : form }
    return render_to_response("game/create-quest.html", 
                              context,
                              RequestContext(request))

@login_required
def join_quest(request, town_slug, quest_slug):
    """
    View that allows members to join quests
    """
    quest = get_object_or_404(Quest, slug=quest_slug, town__slug=town_slug)
    qs = Character.available_characters_by_user(request.user)
    
    if request.method == 'POST':
        form = QuestForm(request.POST, queryset=qs)
        if form.is_valid():
            quest.add_character(form.cleaned_data['character'])
            return HttpResponseRedirect(quest.get_absolute_url())
    else:
        form = QuestForm(queryset=qs)
    context = { 'form' : form }
    return render_to_response("game/join-quest.html", 
                              context,
                              RequestContext(request))

@login_required
def leave_quest(request, town_slug, quest_slug):
    """
    View that allows users to leave a quest
    """
    quest = get_object_or_404(Quest, slug=quest_slug, town__slug=town_slug)
    qs = Character.objects.filter(author__user=request.user,
                                  questmembership__quest=quest,
                                  questmembership__date_left__isnull=True)

    if request.method == 'POST':
        form = QuestForm(request.POST, queryset=qs)
        if form.is_valid():
            quest.remove_character(form.cleaned_data['character'])
            return HttpResponseRedirect(quest.get_absolute_url())
    else:
        form = QuestForm(queryset=qs)
    context = {'quest':quest, 'form':form}
    return render_to_response("game/leave-quest.html", 
                              context,
                              RequestContext(request))