from django.contrib import messages
from django.http import HttpResponseRedirect


def handle_error(request, error, point_to):
    """
    A graceful way of handling generic errors throughout the site. The error
    is placed in to the user's message queue, ready to be picked up and displayed
    the next time the master template get used (i.e. the next page they see
    will show them the error). An error must also redirect to a page. This could
    be back to where they came from, or a customised error page specifically
    for that view - the choice is yours.
    
    The use of this util is very specific. It is for errors that a user should
    never actually see. For example, trying to edit another user's profile,
    or joining a quest that they can't.
    
    It is the responsibility of the frontend to prevent normal usage from
    ever bringing up one of these errors. So, if a user cannot join a quest,
    they should never be displayed a link to join it. However, if the user
    were to manipulate a URL, or change values on a form, they would be
    passed through this error handler.
    
    Basically, this is a high level security/permission handler that will
    tell script kiddies off. Of course, there are legitimate occassions,
    such as if someone follows a pasted link, most likely because someone
    who could see it linked them to it.
    """
    messages.add_message(request, messages.ERROR, error)
    return HttpResponseRedirect(point_to)