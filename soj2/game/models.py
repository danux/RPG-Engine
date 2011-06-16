from django.db import models
from django.db.models.signals import pre_save
from django.contrib.auth.models import User, Group

from mcnulty.dashboard.fields import HtmlField

from soj2.characters.models import Character
from soj2.world.models import Town
from soj2.utils.slug_generator import slug_generator


class Quest(models.Model):
    
    name = models.CharField(max_length=150)
    slug = models.SlugField()
    is_open = models.BooleanField()
    town = models.ForeignKey(Town)
    characters = models.ManyToManyField(Character, through="QuestMembership")
    
    class MultipleQuestsException(Exception):
        pass
    
    @property
    def current_characters(self):
        return self.questmembership_set.filter(date_left__isnull=True)
    
    def has_character(self, character):
        """
        Returns true or false if a character is on a quest
        """
        try:
            self.current_characters.get(character=character)
        except QuestMembership.DoesNotExist:
            return False
        else:
            return True
    
    def add_character(self, character, is_leader=False):
        """
        Adds a character to a quest, and raises an exception is the
        character is already on the quest
        """
        if self.has_character(character):
            raise Quest.MultipleQuestsException
        quest_membership = QuestMembership.objects.create(quest=self,
                                                          character=character,
                                                          is_leader=is_leader)
        quest_membership.save()
    
    def remove_character(self, character):
        """
        Adds a character to a quest, and raises an exception is the
        character is already on the quest
        """
        if self.has_character(character):
            quest_membership = QuestMembership.objects.get(quest=self,
                                                           character=character)
            quest_membership.delete()
        else:
            raise QuestMembership.DoesNotExist
        
class QuestMembership(models.Model):
    """
    Model to manage relationship between a character and a Quest
    """
    quest = models.ForeignKey(Quest)
    character = models.ForeignKey(Character)
    is_leader = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_left = models.DateTimeField(blank=True, null=True)

pre_save.connect(slug_generator, sender=Quest)