"""Views used by the characters admin."""
from datetime import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from soj2.characters.models import Character
from soj2.characters.admin_forms import RejectCharacterForm


@staff_member_required
def reject_application_form(request, character_id=None):
    """
    This views handles the character application process. Users are able to
    save a draft of their application, post the application, or re-submit if
    rejected.
    """
    if character_id is not None:
        try:
            character = request.user.userprofile.character_set.get(
                    pk=character_id,
                    date_approved__isnull=True,
                    approved_by__isnull=True,
                    date_submitted__isnull=True)
        except Character.DoesNotExist:
            raise Http404('Could not find character application')

    if request.method == 'POST':
        form = RejectCharacterForm(request.POST, instance=character)
    else:
        form = RejectCharacterForm()

    context = { 'form' : form, 'object_id' : character_id }
    return render_to_response("admin/reject-character-application.html", 
                              context, RequestContext(request))