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

from rpgengine.game.forms import CreateQuestForm, QuestForm
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
        self.quest_two = Quest.objects.get(pk=2)
        self.client.login(username='test_member', password='test')
        
    def testAvailableCharacters(self):
        """
        Tests that the Quest object has a static method that can
        return available characters for a user
        """
        self.assertEqual(len(Character.available_characters_by_user(self.test_member)), 2)
        self.assertEqual(len(Character.available_characters_by_user(self.test_admin)), 1)
        
    def testRealmRenders(self):
        """
        Tests to ensure the basic realm page renders
        """
        response = self.client.get(reverse('game:realm'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game/realm.html')
        
    def testTownRenders(self):
        """
        Tests to ensure the basic town page renders
        """
        response = self.client.get(reverse('game:view-town', args=[self.town_one.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game/view-town.html')
        
class CreateQuestsTestCase(QuestModelTestCase):
    """
    Series of tests ensuring that creating a quest works correctly
    """
    def testCreateQuestModel(self):
        """
        Models must provide a single method to create quests. The quest
        must generate its own slug
        """
        quest = Quest.objects.start_quest(name='Quest Test Case',
                                          town=self.town_one)
        self.assertEqual(quest.slug, 'quest-test-case')
        self.assertTrue(quest.is_open)

    def testCanSetInitialMember(self):
        """
        A quest must provide a method of setting the initial member
        """
        self.quest_one.set_initial_member(self.character_one)
        self.assertEqual(len(self.quest_one.characters.all()), 1)
        
    def testInitialMemberOnlyCalledOnce(self):
        """
        Once a quest has an initial member, it cannot be added again
        """
        self.quest_one.set_initial_member(self.character_one)
        self.assertRaises(Quest.IllegalQuestOperation,
                          lambda: self.quest_one.set_initial_member(self.character_two))
                          
    def testInitialMemberIsLeader(self):
        """
        The initial member of a quest must be made leader
        """
        self.assertFalse(self.quest_one.is_leader(self.test_member))
        self.quest_one.set_initial_member(self.character_one)
        self.assertTrue(self.quest_one.is_leader(self.test_member))
        
    def testUnapprovedCharactersCannotStartQuests(self):
        """
        A character who is not approved cannot start a quest
        """
        self.assertRaises(Quest.UnsuitableCharacterException,
                          lambda: self.quest_one.set_initial_member(self.character_four))
        
    def testInitialMemberNotOnQuest(self):
        """
        The initial member of a quest must not already be on another quest
        """
        self.quest_one.set_initial_member(self.character_one)
        self.assertRaises(Quest.UnsuitableCharacterException,
                          lambda: self.quest_two.set_initial_member(self.character_one))

    def testCreateQuestFormRenders(self):
        """
        A view must render, and it must produce a form pre-populated with
        a given user's available characters
        """
        response = self.client.get(reverse('game:create-quest',
                                           args=[self.town_one.slug]))
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'game/create-quest.html')
        self.assertTrue(isinstance(response.context['form'], CreateQuestForm))
        self.assertEquals(2, len(response.context['form'].fields['character'].choices))
        
    def testCreateFormCannotRenderWithNoFreeCharacters(self):
        """
        A user should not be able to create a quest if the do not have any free
        characters.
        """
        self.quest_one.set_initial_member(self.character_one)
        self.quest_one.add_character(self.character_two)
        response = self.client.get(reverse('game:create-quest',
                                           args=[self.town_one.slug]))
        self.assertRedirects(response, 
                             reverse('game:view-town', args=[self.town_one.slug,]))

    def testPostCreateQuestForm(self):
        """
        A post to the view that renders the form must create the quest and
        redirect the user to the quest's page once rendered. Also ensure
        the user is correct set as the leader.
        """
        data = {'name' : 'Test Case Quest',
                'character' : self.character_one.pk}
        response = self.client.post(reverse('game:create-quest',
                                            args=[self.town_one.slug]),
                                    data)
        self.assertRedirects(response, 
                             reverse('game:view-quest', args=[self.town_one.slug,
                                                              'test-case-quest']))
        quest = Quest.objects.get(slug='test-case-quest')
        self.assertTrue(quest.is_leader(self.test_member))

class JoinQuestsTestCase(QuestModelTestCase):
    """
    Series of tests ensuring that joining a quest works correctly
    """
    def testJoinQuestModels(self):
        """
        The model must provide a method of characters being added to a quest
        """
        self.assertEqual(self.quest_one.characters.count(), 0)
        self.quest_one.add_character(self.character_two)
        self.assertEqual(self.quest_one.characters.count(), 1)

    def testJoinMemberNotOnQuest(self):
        """
        A user cannot join a quest if they are already on another quest
        """
        self.quest_one.add_character(self.character_one)
        self.assertRaises(Quest.UnsuitableCharacterException,
                          lambda: self.quest_two.add_character(self.character_one))

    def testCannotJoinClosedQuest(self):
        """
        A user cannot join a quest if it is closed
        """
        self.quest_one.is_open = False
        self.assertRaises(Quest.IllegalQuestOperation,
                          lambda: self.quest_one.add_character(self.character_one))

    def testJoinQuestFormRenders(self):
        """
        A view must render, and it must produce a form pre-populated with
        a given user's available characters
        """
        response = self.client.get(reverse('game:join-quest',
                                           args=[self.town_one.slug,
                                                 self.quest_one.slug]))
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'game/join-quest.html')
        self.assertTrue(isinstance(response.context['form'], QuestForm))
        self.assertEquals(2, len(response.context['form'].fields['character'].choices))
        
    def testPostJoinQuestForm(self):
        """
        Tests that a valid submission of the JoinQuestForm adds a character
        to a quest. Once joined, the form must redirect to the quest
        """
        self.assertEqual(self.quest_one.characters.count(), 0)
        data = {'name' : 'Test Case Quest',
                'character' : self.character_one.pk}
        response = self.client.post(reverse('game:join-quest',
                                            args=[self.town_one.slug,
                                                  self.quest_one.slug]),
                                    data)
        self.assertEqual(self.quest_one.characters.count(), 1)
        self.assertRedirects(response,
                             reverse('game:view-quest', args=[self.town_one.slug,
                                                              self.quest_one.slug]))

    def testPostJoinQuestFormInvalidCharacter(self):
        """
        A form error is displayed if the user submits an invalid character value
        """
        data = {'name' : 'Test Case Quest',
                'character' : self.character_three.pk}
        response = self.client.post(reverse('game:join-quest',
                                            args=[self.town_one.slug,
                                                  self.quest_one.slug]),
                                    data)
        self.assertFormError(response, "form", 'character',
                "Select a valid choice. That choice is not one of the available choices.")

class LeaveQuestsTestCase(QuestModelTestCase):
    """
    Series of tests ensuring that leaving a quest workons correctly
    """
    def testLeaveQuestsModels(self):
        """
        The quests model must provide a method for removing a character from 
        a quest
        """
        self.quest_one.add_character(self.character_one)
        self.assertTrue(self.quest_one.remove_character(self.character_one))
        self.assertEqual(len(self.quest_one.active_characters()), 0)

    def testLeaveQuestNotOn(self):
        """
        An exception must be raised when a character is not on a quest and
        it is asked to be removed
        """
        self.assertRaises(QuestMembership.DoesNotExist,
                          lambda: self.quest_one.remove_character(self.character_one))

    def testLeaveQuestForm(self):
        """
        A form must be rendered allowing an author to remove their characters
        from a quest. The form must render with a select field that correctly
        contains the characters on a quest
        """
        self.quest_one.add_character(self.character_one)
        response = self.client.get(reverse('game:leave-quest',
                                           args=[self.town_one.slug, self.quest_one.slug]))
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'game/leave-quest.html')
        self.assertTrue(isinstance(response.context['form'], QuestForm))
        self.assertEquals(1, len(response.context['form'].fields['character'].choices))

    def testPostLeaveQuestForm(self):
        """
        Posting the form to the server should remove the character selected
        from the quest
        """
        self.quest_one.add_character(self.character_one)
        data = {'character' : self.character_one.pk}
        response = self.client.post(reverse('game:leave-quest',
                                            args=[self.town_one.slug,
                                                  self.quest_one.slug]),
                                    data)
        self.assertEqual(len(self.quest_one.active_characters()), 0)
        self.assertRedirects(response,
                             reverse('game:view-quest', args=[self.town_one.slug,
                                                              self.quest_one.slug]))

    def testRemoveOtherPeoplesCharacter(self):
        """
        An invalid character error should be displayed on the form when it is
        submitted with the ID of another user's characters
        """
        data = {'character' : self.character_three.pk}
        response = self.client.post(reverse('game:leave-quest',
                                            args=[self.town_one.slug,
                                                  self.quest_one.slug]),
                                    data)
        self.assertFormError(response, "form", 'character',
                "Select a valid choice. That choice is not one of the available choices.")

    def testRemoveCharacterNotOnQuest(self):
        """
        Attempting to remove a character that is not on a quest but does
        belong to the required user cannot be removed
        """
        data = {'character' : self.character_one.pk}
        response = self.client.post(reverse('game:leave-quest',
                                            args=[self.town_one.slug,
                                                  self.quest_one.slug]),
                                    data)
        self.assertFormError(response, "form", 'character',
                "Select a valid choice. That choice is not one of the available choices.")
    
    def testRemoveCharacterAlreadyRemoved(self):
        """
        Test that a form error is created when attempting to remove a character
        that has already been removed
        """
        self.quest_one.add_character(self.character_one)
        self.quest_one.remove_character(self.character_one)
        data = {'character' : self.character_one.pk}
        response = self.client.post(reverse('game:leave-quest',
                                            args=[self.town_one.slug,
                                                  self.quest_one.slug]),
                                    data)
        self.assertFormError(response, "form", 'character',
                "Select a valid choice. That choice is not one of the available choices.")