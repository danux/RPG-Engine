from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import pre_save

from rpgengine.accounts.models import UserProfile as Author
from rpgengine.utils.slug_generator import slug_generator
from rpgengine.world.models import Town, Race


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
    name = models.CharField(max_length=100, unique=True, db_index=True)
    slug = models.CharField(max_length=100, unique=True, db_index=True)
    race = models.ForeignKey(Race)
    hometown = models.ForeignKey(Town)
    back_story = models.TextField()
    physical_appearence = models.TextField()
    avatar = models.ImageField(blank=True, null=True, 
                               upload_to="dynamic/characters/character/avatars")
    gm_notes = models.TextField(blank=True, null=True)
    approved_by = models.ForeignKey(User, related_name="approved_characters",
                                    blank=True, null=True)
    date_approved = models.DateTimeField(blank=True, null=True)
    date_submitted = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        permissions = (
            ("can_moderate", "Can moderate characters"),)
    
    @property
    def is_approved(self):
        if self.approved_by is not None and self.date_approved is not None:
            return True
        return False
    
    @property
    def status(self):
        '''
        Calculates the characters current state. This could be stored as
        an option in the model, but a dynamic solution provides greater
        flexibility and normalisation
        '''
        if self.is_approved is True:
            return 'approved'
        elif self.gm_notes is not None:
            return 'unsuccessful'
        elif self.date_submitted is not None:
            return 'pending'
        else:
            return 'draft'

    @staticmethod
    def approved_characters_by_user(user):
        """
        Returns all approved characters for a given user
        """
        return user.userprofile.character_set.exclude(date_approved__isnull=True)

    @staticmethod
    def available_characters_by_user(user):
        """
        Returns all of the available characters for a given user. I.e.
        the characters are not currently on a quest
        """
        return Character.approved_characters_by_user(user).exclude(questmembership__date_left__isnull=True,
                                                                   questmembership__pk__isnull=False)

pre_save.connect(slug_generator, sender=Character)