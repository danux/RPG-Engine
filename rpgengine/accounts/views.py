"""Views used by the characters application."""
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from rpgengine.accounts.forms import UpdateAccountForm


@login_required
def my_account(request):
    context = {}
    return render_to_response("accounts/my-account.html", 
                              context, RequestContext(request))

@login_required
def update_profile(request):
    """
    This view allows a user to update their account and change their
    email address
    """
    data = {'email' : request.user.email,
            'timezone' : request.user.userprofile.timezone,
            'country' : request.user.userprofile.country,
            'english_first_language' :  request.user.userprofile.english_first_language, }
    if request.method == 'POST':
        form = UpdateAccountForm(request.POST, initial=data)
        if form.is_valid():
                request.user.email = form.cleaned_data['email']
                request.user.userprofile.timezone = form.cleaned_data['timezone']
                request.user.userprofile.country = form.cleaned_data['country']
                request.user.userprofile.english_first_language = form.cleaned_data['english_first_language']
                request.user.userprofile.save()
                request.user.save()
                return HttpResponseRedirect(reverse('accounts:my-account'))
    else:
        form = UpdateAccountForm(initial=data)

    context = { 'form' : form }
    return render_to_response("accounts/update-profile.html", 
                              context, RequestContext(request))