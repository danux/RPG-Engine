import os
import string
import datetime
import re

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.conf import settings
from django.core import mail
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.test import TestCase
from django.test.client import Client

from soj2.game.models import Quest

class QuestModelTestCase(TestCase):
    """
    Tests basic functionality of the Quests model
    """
    fixtures = ['quest-test-data.json']
    
    def setUp(self):
        """
        Sets up the initial data that is used by the characters app
        """
        self.test_admin = User.objects.get(username='test_admin')
    
    def testCreateQuests(self):
        """
        Tests that a user can create a new quest
        """
        quest = Quest()
        quest.name = "Test Quest"
        quest.town = self.town_1
        quest.is_open = True
        quest.save()
        
        quest.add_character(self.character_one)
        
        self.assertEqual(quest.current_members[0], self.character_one)
        self.assertEqual(quest.current_members.count(), 1)
    
    def testJoinQuests(self):
        """
        Tests that a user can join a quest
        """
        self.quest_one.add_character(self.character_two)
        
        self.assertEqual(quest.current_members[-1], self.character_two)
        self.assertEqual(quest.current_members.count(), 2)
    
    def testOnlyOneQuest(self):
        """
        Tests that a character can only be on quest at a time
        """
        self.quest_one.add_character(self.character_two)
        self.assertRaises(Quest.MultipleQuestsException,
                          lambda: self.quest_one.add_character(self.character_two))
    
    def testLeaveQuest(self):
        """
        Tests that a user can leave a quest, and then join another
        """
        self.quest_one.add_character(self.character_two)
        self.quest_one.remove_character(self.character_two)
        self.assertEqual(self.quest.count(), 1)
    
    def testLeaveQuestAutoNewLeader(self):
        """
        Tests that when a quest leader leaves the quest, the next longest
        standing member of the quest becomes the quest leader
        """
        pass

    def testCloseQuest(self):
        """
        Tests that when a quest is closed that no further members can join
        """
        pass
    
    def testAutoCloseQuest(self):
        """
        Tests that a quest with no members automatically closes
        """
        pass
    
    def testRejoinQuet(self):
        """
        Tests that when a user leaves and quest and rejoins, the history
        is correctly maintained
        """
        pass