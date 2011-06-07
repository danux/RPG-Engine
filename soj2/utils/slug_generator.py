from django.template.defaultfilters import slugify

def find_available_slug(object, instance, slug):
    """
    Recursive method that will add underscores to a slug field
    until a free value is located
    """
    try:
        sender_node = object.objects.get(slug=slug)
    except object.DoesNotExist:
        instance.slug = slug
    else:
        slug = '%s_' % slug
        find_available_slug(object, instance, slug)
    return

def slug_generator(sender, **kwargs):
    """ Generates a unique slug for a node """
    instance = kwargs['instance']
    if instance.slug is not '':
        return
    slug = slugify(instance.name)
    find_available_slug(sender, instance, slug)