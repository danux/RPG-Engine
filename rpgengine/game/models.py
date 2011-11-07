from datetime import datetime

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.contrib.auth.models import User, Group

from rpgengine.characters.models import Character
from rpgengine.world.models import Town
from rpgengine.utils.slug_generator import slug_generator
from rpgengine.game.managers import QuestManager


class Quest(models.Model):
    """
    Representation of a Quest in the game. A quest is essentially a thread
    in the message board, with a leader.
    """
    name = models.CharField(max_length=150)
    slug = models.SlugField()
    is_open = models.BooleanField()
    town = models.ForeignKey(Town)
    characters = models.ManyToManyField(Character, through="QuestMembership",
        blank=True, null=True)
    leaders = models.ManyToManyField(User, blank=True, null=True, related_name='quests_lead')
    kicked_users = models.ManyToManyField(User, blank=True, null=True,
        related_name='quests_kicked_from')

    objects = QuestManager()

    class IllegalQuestOperation(Exception):
        """
        Raised for generic, one-of errors that may occur when working
        with quests
        """

    class UnsuitableCharacterException(IllegalQuestOperation):
        """
        Raised when a character is supplied to a quest method that is not
        suitable; i.e. someone has tried to add a character who is already
        on another quest
        """

    def set_initial_member(self, character):
        """
        Adds the first member of a quest, and makes them leader
        """
        if self.characters.count() > 0:
            raise Quest.IllegalQuestOperation
        if not character.is_approved:
            raise Quest.UnsuitableCharacterException
        quest_membership = self.add_character(character)
        self.leaders.add(character.author.user)
        self.save()
        return quest_membership

    def is_leader(self, user):
        """
        Return true or false is a user is a leader or not
        """
        if user in self.leaders.all():
            return True
        return False
    
    def add_character(self, character):
        """
        Adds a character to a quest
        """
        if self.is_open is not True:
            raise Quest.IllegalQuestOperation
        try:
            Quest.objects.get_by_character(character)
            raise Quest.UnsuitableCharacterException
        except Quest.DoesNotExist:
            quest_membership = QuestMembership.objects.create(quest=self,
                                                              character=character)
            return quest_membership

    def remove_character(self, character):
        """
        Removes a character from a quest, returns false if character
        is not on the quest
        """
        membership = self.questmembership_set.get(character=character,
                                                  date_left__isnull=True)
        membership.date_left = datetime.now()
        membership.save()
        return True

    def active_characters(self):
        """
        Yields all the characters currently on this quest
        """
        return [questmembership.character for questmembership 
                in self.questmembership_set.filter(date_left__isnull=True)]

<<<<<<< HEAD
    def get_absolute_url(self):
        return reverse('game:view-quest', args=[self.town.slug, self.slug])

=======
>>>>>>> dbc4ad4d416bb8af5e1cce39f4c316c20c3600be
class QuestMembership(models.Model):
    """
    Model to manage relationship between a character and a Quest
    """
    quest = models.ForeignKey(Quest)
    character = models.ForeignKey(Character)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_left = models.DateTimeField(blank=True, null=True)

pre_save.connect(slug_generator, sender=Quest)