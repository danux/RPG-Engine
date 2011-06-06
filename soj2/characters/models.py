from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify

from soj2.accounts.models import UserProfile as Author
from soj2.world.models import Town, Race, Language


class Character(models.Model):
    """
    Class representing a character. A character is a participant within the
    games and stories, and each author may have several characters within the
    game.
    
    Before a character is given access to the whole game it must be approved,
    however, there is a newbie holding pen, where new characters must play
    until they have demonstrated the basic understandings of pbp.
    """
    author = models.ForeignKey(Author)
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    race = models.ForeignKey(Race)
    hometown = models.ForeignKey(Town)
    languages = models.ManyToManyField(Language)
    back_story = models.TextField()
    physical_appearence = models.TextField()
    gm_notes = models.TextField(blank=True, null=True)
    approved_by = models.ForeignKey(User, related_name="approved_characters",
                                    blank=True, null=True)
    date_approved = models.DateTimeField(blank=True, null=True)
    date_submitted = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
    
    @property
    def is_approved(self):
        if self.approved_by is not None and self.approved_on is not None:
            return True
        return False
    
    @property
    def status(self):
        if self.is_approved is True:
            return 'approved'
        elif self.gm_notes is not None:
            return 'unsuccessful'
        elif self.date_submitted is not None:
            return 'pending'
        else:
            return 'draft'

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
    """ Generates a unique slug for a character """
    instance = kwargs['instance']
    if instance.slug is not None:
        return
    slug = slugify(instance.name)
    find_available_slug(sender, instance, slug)
        
pre_save.connect(slug_generator, sender=Character)