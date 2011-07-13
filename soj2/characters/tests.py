import os, string, datetime

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core import mail
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.test import TestCase
from django.test.client import Client

from soj2.accounts.forms import RegistrationFormWithFields
from soj2.accounts.models import UserProfile
from soj2.characters.models import Character


class CharacterCreationTestCase(TestCase):
    """
    Tests various aspects of creating characters
    """
    fixtures = ['world_test_data.json',
                'accounts_test_data.json',
                'characters_test_data.json',
                'game_test_data.json']
    
    def setUp(self):
        self.test_admin = User.objects.get(pk=1)
        self.test_member = User.objects.get(pk=2)

        self.client.login(username="test_member", password='test')

    def tearDown(self):
        pass
    
    def submit_application_form(self, submit=False, 
                                url=reverse('characters:application-form')):
        """
        Quick, re-usable method to submit and create a character
        """
        post_data = {
            'physical_appearence' : 'test_appearance',
            'back_story' : 'test_back_story',
            'race' : 2,
            'hometown' : 4,
            'name' : 'Test Name',
        }
        if submit is not False:
            post_data['Submit'] = True
        else:
            post_data['Save'] = True
        response = self.client.post(url, 
                                    post_data)
        self.assertEqual(response.status_code, 200)

    def testBlankForm(self):
        response = self.client.get(reverse('characters:application-form'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('characters:amend-application-form',
                                           args=[0]))
        self.assertEqual(response.status_code, 404)

    def testCreationForm(self):
        """
        Tests aspects of the creation form, namely that a form can be saved
        or submitted for GM review. 
        """
        self.submit_application_form()
        character = Character.objects.get(pk=5)
        self.assertTrue(character is not None)
        self.assertEquals(character.status, 'draft')
    
    def testModifyingCreationForm(self):
        """
        Tests the loading of a saved character sheet, and then submitting it
        for approval. Also tests that a character that has been submitted cannot
        be modified.
        """
        self.submit_application_form()
        character = Character.objects.get(pk=5)
        self.assertFalse(character.is_approved)
        
        self.submit_application_form(submit=True,
                url=reverse('characters:amend-application-form', args=[5]))
        character = Character.objects.get(pk=5)
        self.assertEquals(character.status, 'pending')
        
        response = self.client.get(
                reverse('characters:amend-application-form', args=[5]))
        self.assertEqual(response.status_code, 404)
        
    def testSlugGeneration(self):
        """ Tests that characters are generated a unique slug """
        self.submit_application_form(submit=True,
                                     url=reverse('characters:application-form'))
        
        post_data = {
            'physical_appearence' : 'test_appearance',
            'back_story' : 'test_back_story',
            'race' : 2,
            'hometown' : 4,
            'name' : 'Test-Name',
            'Submit' : True
        }
        response = self.client.post(reverse('characters:application-form'), 
                                    post_data)
        self.assertEqual(response.status_code, 200)
        
        post_data = {
            'physical_appearence' : 'test_appearance',
            'back_story' : 'test_back_story',
            'race' : 2,
            'hometown' : 4,
            'name' : 'Test  Name',
            'Submit' : True
        }
        response = self.client.post(reverse('characters:application-form'), 
                                    post_data)
        self.assertEqual(response.status_code, 200)
        
        character_one = Character.objects.get(pk=5)
        character_two = Character.objects.get(pk=6)
        character_three = Character.objects.get(pk=7)

        self.assertEquals(character_one.slug, 'test-name')
        self.assertEquals(character_two.slug, 'test-name_')
        self.assertEquals(character_three.slug, 'test-name__')
        
    def testGmEmails(self):
        """
        Tests that the correct GMs are sent emails, with a valid link, to 
        approve new characters.
        """
        pass
    
    def testCharacterAdmin(self):
        """
        Ensures the character admin is installed and loads
        """
        self.client.login(username="test_admin", password='test')
        response = self.client.get('/admin/characters/')
        self.assertEquals(response.status_code, 200)

    def testCharacterApproval(self):
        """
        Tests that a character application can be approved
        """
        self.client.login(username="test_admin", password='test')
        response = self.client.get(reverse(
                'characters:approve-application-form',
                args=[5]))
        self.assertEquals(response.status_code, 404)
        
        self.submit_application_form(submit=True,
                                     url=reverse('characters:application-form'))
        
        response = self.client.get(reverse(
                'characters:approve-application-form',
                args=[5]))
        self.assertEquals(response.status_code, 302)
        
        character = Character.objects.get(pk=5)
        self.assertEquals(character.status, 'approved')
    
    def testCharacterRejection(self):
        """
        Tests that a character application can be rejected
        """
        self.client.login(username="test_admin", password='test')
        response = self.client.get(reverse(
                'characters:reject-application-form',
                args=[5]))
        self.assertEquals(response.status_code, 404)
        
        self.submit_application_form(submit=True,
                                     url=reverse('characters:application-form'))
        
        response = self.client.get(reverse(
                'characters:reject-application-form',
                args=[5]))
        self.assertEquals(response.status_code, 200)
        
        response = self.client.post(reverse(
                'characters:reject-application-form',
                args=[5]), { 'gm_notes' : 'do not like' })
        self.assertEquals(response.status_code, 302)
        
        character = Character.objects.get(pk=5)
        
        self.assertEquals(character.status, 'unsuccessful')
        
    def testCanLoadCharactersByUser(self):
        """
        Ensures the static method correctly gets all characters for a user
        """
        self.assertEqual(len(Character.approved_characters_by_user(self.test_member)), 2)