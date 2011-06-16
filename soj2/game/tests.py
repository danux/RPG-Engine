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

from soj2.game.models import Quest, QuestMembership
from soj2.characters.models import Character
from soj2.world.models import Town

class QuestModelTestCase(TestCase):
    """
    Tests basic functionality of the Quests model
    """
    fixtures = ['world_test_data.json',
                'accounts_test_data.json',
                'characters_test_data.json',
                'game_test_data.json']
    
    def setUp(self):
        """
        Sets up the initial data that is used by the characters app
        """
        self.test_admin = User.objects.get(username='test_admin')
        self.character_one = Character.objects.get(pk=1)
        self.character_two = Character.objects.get(pk=2)
        self.town_one = Town.objects.get(pk=4)
        self.quest_one = Quest.objects.get(pk=1)
    
    def testCreateQuests(self):
        """
        Tests that a user can create a new quest
        """
        quest = Quest()
        quest.name = "Test Quest"
        quest.town = self.town_one
        quest.is_open = True
        quest.save()
        
        quest.add_character(self.character_one)
        self.assertTrue(quest.has_character(self.character_one))
        self.assertEqual(quest.current_characters.count(), 1)
    
    def testJoinQuests(self):
        """
        Tests that a user can join a quest
        """
        self.quest_one.add_character(self.character_one)
        self.assertTrue(self.quest_one.has_character(self.character_one))
        self.assertEqual(self.quest_one.current_characters.count(), 1)
    
    def testOnlyOneQuest(self):
        """
        Tests that a character can only be on quest at a time
        """
        self.quest_one.add_character(self.character_two)
        self.assertRaises(Quest.MultipleQuestsException,
                          lambda: self.quest_one.add_character(self.character_two))
    
    def testCannotLeaveQuestNotOn(self):
        """
        Tests that a user cannot leave a quest they are not on
        """
        self.assertRaises(QuestMembership.DoesNotExist,
                          lambda: self.quest_one.remove_character(self.character_one))
    
    def testLeaveQuest(self):
        """
        Tests that a user can leave a quest, and then join another
        """
        self.quest_one.add_character(self.character_one)
        self.quest_one.add_character(self.character_two)
        self.quest_one.remove_character(self.character_two)
        self.assertEqual(self.quest_one.current_characters.count(), 1)
    
    def testQuestAutoQuestLeadership(self):
        """
        Tests that a user can leave a quest, and then join another
        """
        self.quest_one.add_character(self.character_one)
        self.assertTrue(self.quest_one.is_leader(self.character_one))
    
    def testQuestLeadership(self):
        """
        Tests that a user can leave a quest, and then join another
        """
        self.quest_one.add_character(self.character_one)
        self.quest_one.add_character(self.character_two, True)
        self.assertTrue(self.quest_one.is_leader(self.character_one))
    
    def testLeaveQuestAutoNewLeader(self):
        """
        Tests that when a quest leader leaves the quest, the next longest
        standing member of the quest becomes the quest leader
        """
        self.quest_one.add_character(self.character_one)
        self.quest_one.add_character(self.character_two)
        self.assertFalse(self.quest_one.is_leader(self.character_two))
        self.quest_one.remove_character(self.character_one)
        self.assertTrue(self.quest_one.is_leader(self.character_two))

    def testCloseQuest(self):
        """
        Tests that when a quest is closed that no further members can join
        """
        self.quest_one.is_open = False
        self.assertRaises(Quest.QuestClosed,
                          lambda: self.quest_one.add_character(self.character_one))
    
    def testAutoCloseQuest(self):
        """
        Tests that a quest with no members automatically closes
        """
        self.quest_one.add_character(self.character_one)
        self.quest_one.remove_character(self.character_one)
        self.assertFalse(self.quest_one.is_open)
    
    def testRejoinQuest(self):
        """
        Tests that when a user leaves a quest and rejoins, the history
        is correctly maintained
        """
        self.quest_one.add_character(self.character_one)
        self.quest_one.add_character(self.character_two)
        self.quest_one.remove_character(self.character_one)
        self.quest_one.add_character(self.character_one)
        self.assertEqual(self.quest_one.questmembership_set.count(), 3)
    
    def testMakeLeader(self):
        """
        Tests that a member of a quest can be promoted to quest leader
        """
        self.quest_one.add_character(self.character_one)
        self.quest_one.add_character(self.character_two)
        self.quest_one.make_leader(self.character_two)
        self.assertEqual(self.quest_one.current_leaders.count(), 2)
    
    def testMakeLeaderBoundaries(self):
        """
        Tests the boundaries of adding leaders, and checks all exceptions
        fire correctly for their given scenario
        """
        self.quest_one.add_character(self.character_one)
        self.assertRaises(Quest.MultipleLeaderException,
                          lambda: self.quest_one.make_leader(self.character_one))
        
        self.quest_one.add_character(self.character_two)
        self.quest_one.is_open = False
        self.assertRaises(Quest.QuestClosed,
                          lambda: self.quest_one.make_leader(self.character_two))
        
        self.quest_one.remove_character(self.character_two)
        self.quest_one.is_open = True
        self.assertRaises(QuestMembership.DoesNotExist,
                          lambda: self.quest_one.make_leader(self.character_two))

        