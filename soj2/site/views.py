from django import template
from django.http import Http404
from django.shortcuts import render_to_response
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return render_to_response("logout.html", {}, template.RequestContext(request))

def subscribe(request):
    try:
        feed_url = request.GET["feed_url"]
    except KeyError:
        raise Http404, "You need to specify a feed URL."
    else:
        context = {"feed_url": feed_url}
        return render_to_response("subscribe.html", context, template.RequestContext(request))
    
    
