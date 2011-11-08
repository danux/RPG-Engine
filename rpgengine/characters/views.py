"""Views used by the characters application."""
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from rpgengine.characters.forms import ApplicationForm
from rpgengine.characters.models import Character


@login_required
def application_form(request, character_id=None):
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
        if character_id is not None:
            form = ApplicationForm(request.POST, instance=character)
        else:
            form = ApplicationForm(request.POST)
        if form.is_valid():
            if character_id is not None:
                character = form.save()
            else:
                character = form.save(commit=False)
                character.author = request.user.userprofile
                character.save()
            try:
                request.POST['Submit']
            except KeyError:
                pass
            else:
                character.date_submitted = datetime.now()
                character.save()
            return HttpResponseRedirect(reverse('accounts:my-account'))
    else:
        if character_id is not None:
            form = ApplicationForm(instance=character)
        else:
            form = ApplicationForm()

    context = { 'form' : form }
    return render_to_response("characters/application-form.html", 
                              context, RequestContext(request))