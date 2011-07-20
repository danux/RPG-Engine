import os
import string
import datetime
import re

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.conf import settings
from django.core import mail
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.test import TestCase
from django.test.client import Client

from rpgengine.game.forms import CreateQuestForm, JoinQuestForm, LeaveQuestForm, KickUserForm
from rpgengine.game.models import Quest, QuestMembership
from rpgengine.characters.models import Character
from rpgengine.world.models import Town


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
        self.test_member = User.objects.get(username='test_member')
        self.character_one = Character.objects.get(pk=1)
        self.character_two = Character.objects.get(pk=2)
        self.character_three = Character.objects.get(pk=3)
        self.character_four = Character.objects.get(pk=4)
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
    
    def testRemoveLeader(self):
        """
        Tests that a member of a quest can be promoted to quest leader
        """
        self.quest_one.add_character(self.character_one)
        self.quest_one.add_character(self.character_two)
        self.quest_one.make_leader(self.character_two)
        self.assertEqual(self.quest_one.current_leaders.count(), 2)
        self.quest_one.remove_leader(self.character_two)
        self.assertEqual(self.quest_one.current_leaders.count(), 1)
        self.assertRaises(QuestMembership.DoesNotExist,
                          lambda: self.quest_one.remove_leader(self.character_two))
    
    def testCannotRemoveLeaderIfOnlyMember(self):
        """
        Tests that a member of a quest can be promoted to quest leader
        """
        self.quest_one.add_character(self.character_one)
        self.assertRaises(Quest.NoLeaderConflict,
                          lambda: self.quest_one.remove_leader(self.character_one))
    
    def testRemoveLeaderAutoNewLeader(self):
        """
        Tests that if a user removes their own leadership of a quest a new
        one is selected
        """
        self.quest_one.add_character(self.character_one)
        self.quest_one.add_character(self.character_two)
        self.quest_one.remove_leader(self.character_one)
        self.assertTrue(self.quest_one.is_leader(self.character_two))
        
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
        
    def testUserInQuest(self):
        """
        Tests that a quest correctly returns true or false if a user is in a
        quest
        """
        self.quest_one.add_character(self.character_one)
        self.assertTrue(self.quest_one.has_user(self.test_member))
        self.assertFalse(self.quest_one.has_user(self.test_admin))
        
    def testUserInQuestAsLeader(self):
        """
        Tests that a quest correctly returns true or false if a user is in a
        quest as a leader
        """
        self.quest_one.add_character(self.character_one)
        self.assertTrue(self.quest_one.has_user_as_leader(self.test_member))
        self.assertFalse(self.quest_one.has_user_as_leader(self.test_admin))
        
    def testKickUser(self):
        """
        Tests that a character can be kicked from a quest
        """
        self.quest_one.add_character(self.character_one)
        self.assertFalse(self.quest_one.is_kicked(self.test_member))
        self.quest_one.kick_user(self.test_member)
        self.assertTrue(self.quest_one.is_kicked(self.test_member))
        
    def testCannotAddKickedUser(self):
        """
        A user who has been kicked should not be allowed to re-join
        """
        self.quest_one.add_character(self.character_one)
        self.quest_one.kick_user(self.test_member)
        self.assertRaises(Quest.KickedUserException,
                          lambda: self.quest_one.add_character(self.character_one))
    
class ForeignModelTestCase(QuestModelTestCase):
    """
    Tests that foreign models are able to correctly return information about
    themselves that may rely on game information
    """
    def testUserProfileAvailableCharacters(self):
        """
        Tests that a user profile is aware of the characters it has that
        are currently available
        """
        self.quest_one.add_character(self.character_one)
        self.assertFalse(
            (self.character_one in Quest.available_characters_by_user(self.test_member)))
        self.quest_one.remove_character(self.character_one)
        self.assertTrue(
            (self.character_one in Quest.available_characters_by_user(self.test_member)))

class ViewRenderingAndContextTestCase(QuestModelTestCase):
    """
    Tests the quest views, specifically forms
    """
    def setUp(self):
        super(ViewRenderingAndContextTestCase, self).setUp()
        self.client.login(username='test_member', password='test')

    def testQuestCreationViewRenders(self):
        """
        Tests that getting the character page gives a 200 response, and
        contains a form
        """
        response = self.client.get(reverse('game:create-quest',
                                           args=[self.town_one.slug,
                                                 self.character_one.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.context['form'], forms.ModelForm))

    def testOverviewRenders(self):
        """
        Tests that there is a view that renders all of the towns
        """
        response = self.client.get(reverse('game:realm'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['nations'].count(), 1)

    def testTownRenders(self):
        """
        Tests that a town can be rendered as a view in the game
        """
        response = self.client.get(reverse('game:view-town',
                                           args=[self.quest_one.town.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['town'], self.town_one)

    def testQuestRenders(self):
        """
        Tests that a quest can be rendered as a view in the game
        """
        response = self.client.get(reverse('game:view-quest',
                                           args=[self.quest_one.town.slug,
                                                 self.quest_one.slug,]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['quest'], self.quest_one)
        
class JoinExitQuestViewsTestCase(ViewRenderingAndContextTestCase):
    """
    Tests the views that lets users join and leave quests.
    """
    def addToQuest(self, character, quest):
        """
        Helper that adds a character to a quest via a view
        """
        data = { 'character' : character.pk, }
        response = self.client.post(reverse('game:join-quest',
                                            args=[quest.town.slug,
                                                  quest.slug,]),
                                    data)
        return response
    
    def removeFromQuest(self, character, quest):
        """
        Helper that adds a character to a quest via a view
        """
        data = { 'character' : character.pk, }
        response = self.client.post(reverse('game:leave-quest',
                                            args=[quest.town.slug,
                                                  quest.slug,]),
                                    data)
        return response

    def testCreateQuest(self):
        """
        Tests the views for creating a quest, ensures that the creating
        character is the leader
        """
        response = self.client.get(reverse('game:create-quest',
                                           args=[self.quest_one.town.slug,
                                                 self.character_one.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.context['form'], CreateQuestForm))
        
        data = {'name' : 'test quest again'}
        response = self.client.post(reverse('game:create-quest',
                                            args=[self.town_one.slug,
                                                 self.character_one.slug]),
                                    data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             reverse('game:view-quest', args=[self.town_one.slug,
                                                              'test-quest-again']))
        
        quest = Quest.objects.get(slug='test-quest-again')
        self.assertTrue(quest.is_leader(self.character_one))
        
    def testCreateQuestAlreadyInQuest(self):
        """
        Test to make sure no one can join a quest if their character is
        already in a quest
        """
        self.quest_one.add_character(self.character_one)
        response = self.client.get(reverse('game:create-quest',
                                           args=[self.quest_one.town.slug,
                                                 self.character_one.slug]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             reverse('game:view-town', args=[self.town_one.slug]))
        
    def testUnapprovedCannotStart(self):
        """
        Make sure un-approved characters cannot start a quest.
        """
        response = self.client.get(reverse('game:create-quest',
                                           args=[self.quest_one.town.slug,
                                                 self.character_four.slug]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             reverse('game:view-town', args=[self.town_one.slug]))
        
    def testJoinQuest(self):
        """
        Test that a character can join a quest and then get redirected
        back to the quest
        """
        response = self.client.get(reverse('game:join-quest',
                                           args=[self.quest_one.town.slug,
                                                 self.quest_one.slug,]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.context['form'], JoinQuestForm))
        
        response = self.addToQuest(self.character_one, self.quest_one)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('game:view-quest',
                                               args=[self.quest_one.town.slug,
                                                     self.quest_one.slug,]))
        self.assertTrue(self.quest_one.has_character(self.character_one)) 
        
    def testOnlyMyCharacterJoinQuest(self):
        """
        Tests that a user can only join a quest with their own characters
        """
        self.addToQuest(self.character_three, self.quest_one)
        self.assertFalse(self.quest_one.has_character(self.character_three)) 
        
    def testAlreadyInQuest(self):
        """
        Tests what happens when a character is already in a quest
        """
        response = self.addToQuest(self.character_one, self.quest_one)
        self.assertTrue(self.quest_one.has_character(self.character_one))
        self.assertEqual(self.quest_one.current_characters.count(), 1)
        response = self.addToQuest(self.character_one, self.quest_one)
        self.assertEqual(self.quest_one.current_characters.count(), 1)

    def testUserHasAvailableCharacter(self):
        """
        Tests that a user cannot join a quest, or get to the view, if they
        have no available character
        """
        self.addToQuest(self.character_one, self.quest_one)
        self.addToQuest(self.character_two, self.quest_one)
        response = self.client.get(reverse('game:join-quest',
                                           args=[self.quest_one.town.slug,
                                                 self.quest_one.slug,]))
        self.assertRedirects(response, reverse('game:view-quest',
                                               args=[self.quest_one.town.slug,
                                                     self.quest_one.slug,]))

    def testCanLeaveQuest(self):
        """
        Ensures a character can leave a quest
        """
        self.quest_one.add_character(self.character_one)
        response = self.client.get(reverse('game:leave-quest',
                                           args=[self.quest_one.town.slug,
                                                 self.quest_one.slug,]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.quest_one.current_characters.count(), 1)
        response = self.removeFromQuest(self.character_one, self.quest_one)
        self.assertRedirects(response, reverse('game:view-quest',
                                               args=[self.quest_one.town.slug,
                                                     self.quest_one.slug,]))
        self.assertEqual(self.quest_one.current_characters.count(), 0)

    def testCanLeaveQuestOnlyIfOn(self):
        """
        Ensures a character must be on a quest to leave it
        """
        response = self.removeFromQuest(self.character_one, self.quest_one)
        self.assertRedirects(response, reverse('game:view-quest',
                                               args=[self.quest_one.town.slug,
                                                     self.quest_one.slug,]))

    def testAutoCloseQuests(self):
        """
        Tests that an empty quest becomes closed
        """
        self.addToQuest(self.character_one, self.quest_one)
        self.assertTrue(self.quest_one.is_open)
        self.removeFromQuest(self.character_one, self.quest_one)
        test_quest = Quest.objects.get(pk=1)
        self.assertFalse(test_quest.is_open)

    def testCanOnlyRemoveMyCharacter(self):
        """
        Ensures that a user can only remove their own characters from a quest
        """
        self.quest_one.add_character(self.character_one)
        self.quest_one.add_character(self.character_three)
        self.removeFromQuest(self.character_three, self.quest_one)
        self.assertTrue(self.quest_one.has_character(self.character_three))

    def testAssignsNewLeader(self):
        """
        Ensures a new quest leader is automatically assigned if the current
        leader leaves the quest
        """
        self.quest_one.add_character(self.character_one)
        self.assertTrue(self.quest_one.is_leader(self.character_one))
        self.quest_one.add_character(self.character_two)
        self.quest_one.remove_character(self.character_one)
        self.assertTrue(self.quest_one.is_leader(self.character_two))
      
class LeadershipQuestViewsTestCase(ViewRenderingAndContextTestCase):
    """
    Tests the functions that the leader of a quest has at their disposal
    """  
    
    def makeLeader(self, character, quest):
        """
        Helper that adds a character to a quest via a view
        """
        data = { 'character' : character.pk, }
        response = self.client.post(reverse('game:make-quest-leader',
                                            args=[quest.town.slug,
                                                  quest.slug,]),
                                    data)
        return response
    
    def testMakeNewLeader(self):
        """
        Tests that the creator of a quest can assign a character to be leader
        """
        self.quest_one.add_character(self.character_one)
        response = self.client.get(reverse('game:make-quest-leader',
                                           args=[self.quest_one.town.slug,
                                                 self.quest_one.slug,]))
        self.assertEqual(response.status_code, 200)
        self.quest_one.add_character(self.character_two)
        self.assertFalse(self.quest_one.is_leader(self.character_two))
        self.makeLeader(self.character_two, self.quest_one)
        self.assertTrue(self.quest_one.is_leader(self.character_two))
        
    def testOnlyLeaderCanMakeLeader(self):
        """
        Tests that only the leader of a quest can assign a character to be
        the leader
        """
        self.quest_one.add_character(self.character_three)
        self.quest_one.add_character(self.character_two)
        self.assertFalse(self.quest_one.is_leader(self.character_two))
        self.makeLeader(self.character_two, self.quest_one)
        self.assertFalse(self.quest_one.is_leader(self.character_two))
        
    def testRemoveLeader(self):
        """
        Tests that leaders can be removed through a view
        """
        self.quest_one.add_character(self.character_one)
        self.quest_one.add_character(self.character_two)
        self.makeLeader(self.character_one, self.quest_one)
        response = self.client.get(reverse('game:remove-quest-leader',
                                           args=[self.quest_one.town.slug,
                                                 self.quest_one.slug,]))
        self.assertEqual(response.status_code, 200)
        data = { 'character' : self.character_one.pk }
        response = self.client.post(reverse('game:remove-quest-leader',
                                            args=[self.quest_one.town.slug,
                                                  self.quest_one.slug,]),
                                            data)
        self.assertFalse(self.character_one in self.quest_one.current_leaders)
        
    def testMustBeLeaderToRemoveLeader(self):
        """
        Tests that one must be a quest leader to remove other leaders
        """
        self.quest_one.add_character(self.character_three)
        self.makeLeader(self.character_three, self.quest_one)
        response = self.client.get(reverse('game:remove-quest-leader',
                                           args=[self.quest_one.town.slug,
                                                 self.quest_one.slug,]))
        self.assertEqual(response.status_code, 302)
        
    def testRemoveLeaderViewAssignsNewLeader(self):
        """
        Examines what happens when a leader removes themselves (a new leader
        should be picked)
        """
        self.quest_one.add_character(self.character_one)
        self.quest_one.add_character(self.character_two)
        data = { 'character' : self.character_one.pk }
        response = self.client.post(reverse('game:remove-quest-leader',
                                            args=[self.quest_one.town.slug,
                                                  self.quest_one.slug,]),
                                            data)
        self.assertTrue(self.quest_one.is_leader(self.character_two))
        
    def testCanRemoveOnlyCharacterLeader(self):
        """
        Tests that you cannot remove leadership from a single character
        """
        self.quest_one.add_character(self.character_one)
        response = self.client.get(reverse('game:remove-quest-leader',
                                           args=[self.quest_one.town.slug,
                                                 self.quest_one.slug,]))
        self.assertEqual(response.status_code, 302)
        
    def kickUserFromQuestRenders(self):
        """
        Tests that a disruptive user can be kicked from a quest
        """
        response = self.client.get(reverse('game:kick-quest-member'),
                                   args[self.quest_one.slug,
                                        self.quest_one.town.slug])
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(self.resposne.context['form'],
                                   KickUserForm))