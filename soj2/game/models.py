from datetime import datetime

from django.db import models
from django.db.models.signals import pre_save
from django.contrib.auth.models import User, Group

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

    class MultipleLeaderException(Exception):
        pass

    class QuestClosed(Exception):
        pass

    @property
    def current_characters(self):
        return self.questmembership_set.filter(date_left__isnull=True)

    @property
    def current_leaders(self):
        return self.current_characters.filter(is_leader=True)

    @staticmethod
    def available_characters_by_user(user):
        """
        Returns all of the available characters for a given user. I.e.
        the characters are not currently on a quest
        """
        return user.userprofile.character_set.exclude(questmembership__date_left__isnull=True,
                                                      questmembership__pk__isnull=False,).filter(date_approved__isnull=False)

    def memberships_by_user(self, user):
        """
        Returns all of the memberships this user has in the quest 
        """
        return self.current_characters.filter(character__author__user=user)

    def has_user(self, user):
        """
        Returns true or false if a user has a character on a quest
        """
        if len(self.memberships_by_user(user)) > 0:
            return True
        return False

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

    def is_leader(self, character):
        """
        Returns True or False if the character passed is a leader on the quest
        """
        try:
            self.current_leaders.get(character=character)
        except QuestMembership.DoesNotExist:
            return False
        else:
            return True

    def add_character(self, character, is_leader=False):
        """
        Adds a character to a quest, and raises an exception is the
        character is already on the quest
        """
        if self.is_open is not True:
            raise Quest.QuestClosed

        if self.current_characters.count() == 0:
            is_leader = True

        if self.has_character(character):
            raise Quest.MultipleQuestsException
        quest_membership = QuestMembership.objects.create(quest=self,
                                                          character=character,
                                                          is_leader=is_leader)

    def remove_character(self, character):
        """
        Adds a character to a quest, and raises an exception is the
        character is already on the quest
        """
        if self.has_character(character):
            quest_membership = QuestMembership.objects.get(quest=self,
                                                           character=character)
            quest_membership.date_left = datetime.now()
            quest_membership.save()

            if self.current_characters.count() == 0:
                self.is_open = False
                self.save()
                return

            if quest_membership.is_leader is True and self.current_leaders.count() == 0:
                new_leader = list(self.current_characters.order_by('date_created'))[0]
                new_leader.is_leader = True
                new_leader.save()
        else:
            raise QuestMembership.DoesNotExist

    def make_leader(self, character):
        """
        Makes the character passed in a leader of the quest, if they are
        already a member
        """
        if self.is_open is not True:
            raise Quest.QuestClosed
        
        if not self.has_character(character):
            raise QuestMembership.DoesNotExist
        
        if self.is_leader(character):
            raise Quest.MultipleLeaderException
        
        membership = self.current_characters.get(character=character)
        membership.is_leader = True
        membership.save()

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