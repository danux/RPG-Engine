"""Views used by the main game."""
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from rpgengine.characters.models import Character
from rpgengine.game.forms import CreateQuestForm, JoinQuestForm, LeaveQuestForm
from rpgengine.game.forms import MakeQuestLeaderForm, RemoveQuestLeaderForm
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
def create_quest(request, town_slug, character_slug):
    """
    View that allows members to create a quest
    """
    town = get_object_or_404(Town, slug=town_slug)
    try:
        character = Quest.available_characters_by_user(request.user).get(slug=character_slug)
    except Character.DoesNotExist:
        return handle_error(request,
                            'The character you selected is not available for you to quest with.',
                            reverse('game:view-town', args=[town_slug]))

    if request.method == 'POST':
        form = CreateQuestForm(request.POST)
        if form.is_valid():
            quest = form.save(commit=False)
            quest.town = town
            quest.is_open = True
            quest.save()
            quest.add_character(character)
            messages.add_message(request,
                                 messages.INFO,
                                 "Your quest, %s, has begun! You can get started by yourself, or wait for others to join you" % quest.name)
            return HttpResponseRedirect(reverse('game:view-quest',
                                                args=[town.slug,
                                                      quest.slug]))
    else:
        form = CreateQuestForm()
    context = {'form' : form,
               'town' : town,
               'character' : character}
    return render_to_response("game/create-quest.html", 
                              context,
                              RequestContext(request))

@login_required
def join_quest(request, town_slug, quest_slug):
    """
    View that allows a user to join a quest
    """
    quest = get_object_or_404(Quest, slug=quest_slug, town__slug=town_slug)
    
    if Quest.available_characters_by_user(request.user).count() < 1:
        return handle_error(request,
                            'You have no available characters',
                            reverse('game:view-quest', args=[town_slug,
                                                             quest_slug]))
    if request.method == 'POST':
        form = JoinQuestForm(request.POST)
        form.set_character_queryset(Quest.available_characters_by_user(request.user))
        if form.is_valid():
            quest_membership = form.save(commit=False)
            quest_membership.quest = quest
            quest_membership.save()
            messages.add_message(request,
                                 messages.INFO,
                                 "%s has joined %s!" % (quest_membership.character.name,
                                                        quest.name))
            return HttpResponseRedirect(reverse('game:view-quest',
                                                args=[town_slug,
                                                      quest.slug]))
    else:
        form = JoinQuestForm()
        form.set_character_queryset(Quest.available_characters_by_user(request.user))
    
    context = { 'form' : form, 'quest' : quest }
    return render_to_response("game/join-quest.html", 
                              context, RequestContext(request))
    
@login_required
def leave_quest(request, town_slug, quest_slug):
    """
    View that allows a character to leave a quest
    """
    quest = get_object_or_404(Quest, slug=quest_slug, town__slug=town_slug)
    
    if quest.has_user(request.user) is not True:
        return handle_error(request,
                            'You have no characters on this quest',
                            reverse('game:view-quest', args=[town_slug,
                                                             quest_slug]))
    if request.method == 'POST':
        form = LeaveQuestForm(request.POST)
        form.set_character_queryset(quest.memberships_by_user(request.user))
        if form.is_valid():
            character = quest.current_characters.get(character__pk = form.cleaned_data['character'],
                                                    character__author__user = request.user).character
            quest.remove_character(character)
            messages.add_message(request,
                                 messages.INFO,
                                 "%s has left %s!" % (character.name,
                                                      quest.name))
            return HttpResponseRedirect(reverse('game:view-quest',
                                                args=[town_slug,
                                                      quest.slug]))
    else:
        form = LeaveQuestForm()
        form.set_character_queryset(quest.memberships_by_user(request.user))
    
    context = { 'form' : form, 'quest' : quest }
    return render_to_response("game/leave-quest.html", 
                              context, RequestContext(request))
    
@login_required
def make_quest_leader(request, town_slug, quest_slug):
    """
    View that allows the quest leader to make new characters the leader
    """
    quest = get_object_or_404(Quest, slug=quest_slug, town__slug=town_slug)
    
    if quest.has_user_as_leader(request.user) is not True:
        return handle_error(request,
                            'You are not leader of this quest',
                            reverse('game:view-quest', args=[town_slug,
                                                             quest_slug]))
    if request.method == 'POST':
        form = MakeQuestLeaderForm(request.POST)
        form.set_character_queryset(quest.non_leaders)
        if form.is_valid():
            character = quest.current_characters.get(character__pk = form.cleaned_data['character']).character
            quest.make_leader(character)
            messages.add_message(request,
                                 messages.INFO,
                                 "%s has left %s!" % (character.name,
                                                      quest.name))
            return HttpResponseRedirect(reverse('game:view-quest',
                                                args=[town_slug,
                                                      quest.slug]))
    else:
        form = MakeQuestLeaderForm()
        form.set_character_queryset(quest.non_leaders)
    
    context = { 'form' : form, 'quest' : quest }
    return render_to_response("game/make-quest-leader.html", 
                              context, RequestContext(request))
    
@login_required
def remove_quest_leader(request, town_slug, quest_slug):
    """
    Removes a leader from a quest
    """
    quest = get_object_or_404(Quest, slug=quest_slug, town__slug=town_slug)
    
    if quest.has_user_as_leader(request.user) is not True:
        return handle_error(request,
                            'You are not leader of this quest',
                            reverse('game:view-quest', args=[town_slug,
                                                             quest_slug]))
    
    if len(quest.current_characters) == 1:
        return handle_error(request,
                            'You have the only character on this quest, therefore you must remain leader',
                            reverse('game:view-quest', args=[town_slug,
                                                             quest_slug]))
        
    if request.method == 'POST':
        form = RemoveQuestLeaderForm(request.POST)
        form.set_character_queryset(quest.current_leaders)
        if form.is_valid():
            character = quest.current_leaders.get(character__pk=form.cleaned_data['character']).character
            quest.remove_leader(character)
            messages.add_message(request,
                                 messages.INFO,
                                 "%s is no longer a quest leader on %s!" % (character.name,
                                                      quest.name))
            return HttpResponseRedirect(reverse('game:view-quest',
                                                args=[town_slug,
                                                      quest.slug]))
    else:
        form = RemoveQuestLeaderForm()
        form.set_character_queryset(quest.current_leaders)
    
    context = { 'form' : form, 'quest' : quest }
    return render_to_response("game/remove-quest-leader.html", 
                              context, RequestContext(request))

@login_required
def kick_from_quest(request, town_slug, quest_slug):
    """
    Allows a quest leader to kick another character from a quest
    """
    quest = get_object_or_404(Quest, slug=quest_slug, town__slug=town_slug)
    
    if quest.has_user_as_leader(request.user) is not True:
        return handle_error(request,
                            'You are not leader of this quest',
                            reverse('game:view-quest', args=[town_slug,
                                                             quest_slug]))
    
    