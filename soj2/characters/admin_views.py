"""Views used by the characters admin."""
from datetime import datetime

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from soj2.characters.models import Character
from soj2.characters.admin_forms import RejectCharacterApplicationForm


@staff_member_required
def reject_application_form(request, character_id=None):
    """
    This views allows a GM to reject a character application form, but they
    must provide a GM Notes reason for rejecting to the user
    """
    if character_id is not None:
        try:
            character = request.user.userprofile.character_set.get(
                    pk=character_id,
                    date_approved__isnull=True,
                    approved_by__isnull=True,
                    date_submitted__isnull=False)
        except Character.DoesNotExist:
            raise Http404(
                    'Could not find character application %d' % int(character_id))

    if request.method == 'POST':
        form = RejectCharacterApplicationForm(request.POST, instance=character)
        if form.is_valid():
            form.save()
            messages.add_message(
                                 request,
                                 messages.INFO,
                                 'You have rejected %s.' % character.name)
            return HttpResponseRedirect('/admin/characters/')
    else:
        form = RejectCharacterApplicationForm()

    context = { 'form' : form, 'character' : character }
    return render_to_response("admin/reject-character-application.html", 
                              context, RequestContext(request))
    
@staff_member_required
def approve_application_form(request, character_id=None):
    """
    This view simply approves a character
    """
    if character_id is not None:
        try:
            character = request.user.userprofile.character_set.get(
                    pk=character_id,
                    date_approved__isnull=True,
                    approved_by__isnull=True,
                    date_submitted__isnull=False)
            
            messages.add_message(
                         request,
                         messages.INFO,
                         'You have approved %s.' % character.name)

            character.approved_by = request.user
            character.date_approved = datetime.now()
            character.save()
            return HttpResponseRedirect('/admin/characters/')
        
        except Character.DoesNotExist:
            raise Http404('Could not find character application')