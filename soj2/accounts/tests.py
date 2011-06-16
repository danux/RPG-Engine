import os
import string
import datetime
import re

from django.db import IntegrityError
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.conf import settings
from django.core import mail
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.test import TestCase
from django.test.client import Client

from soj2.accounts.forms import RegistrationFormWithFields
from soj2.accounts.models import UserProfile, GamePermission


class RegistrationTestCase(TestCase):
    """
    Tests various aspects of the registration system
    """
    fixtures = ['accounts_test_data.json']
    
    def setUp(self):
        self.test_admin = User.objects.get(pk=1)
        self.test_member = User.objects.get(pk=2)

    def tearDown(self):
        pass

    def testUniqueUsername(self):
        """ 
        Tests that usernames must be unique by attempting to register the same
        username twice
        """
        self.assertRaises(IntegrityError,
                          lambda: User.objects.create_user(username='test_member',
                                                           password='pass1',
                                                           email='test_member@example.com'))

    def testUniqueEmail(self):
        """
        Tests that emails are unique
        """
        post_data = {
            'email' : 'test_member@example.com',
        }
        response = self.client.post(reverse('accounts:register'), post_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
                response,
                "form", 
                'email',
                "This email address is already in use. Please select another")

    def testUniquePenName(self):
        """
        Tests that pen names are unique
        """
        post_data = {
            'name' : 'test member',
        }
        response = self.client.post(reverse('accounts:register'), post_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
                response,
                "form", 
                'name',
                "This pen name is already in use. Please select another")
        
    def testMinimumAge(self):
        """ 
        Tests that users under the required age cannot register
        """
        post_data = {
            'date_of_birth_year' : datetime.date.today().year,
            'date_of_birth_month' : 1,
            'date_of_birth_day' : 1,
        }
        response = self.client.post(reverse('accounts:register'), post_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", 
                 'date_of_birth', 'You must be at least 13 years old to play')

    def testFullProcess(self):
        """ 
        Tests the full registration process for new accounts
        """
        post_data = {
            'username' : 'testActivationCodeUser',
            'email' : 'testActivationCodeUser@amarus.co.uk',
            'password1' : 'password',
            'password2' : 'password',
            'name' : 'pen_name',
            'date_of_birth_year' : 1986,
            'date_of_birth_month' : 8,
            'date_of_birth_day' : 16,
            'timezone' : 'Europe/London',
            'country' : 'GB',
        }
        response = self.client.post(reverse('accounts:register'), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:register-done'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Welcome to SoJ2!')
        user = authenticate(username='testActivationCodeUser', 
                            password='password')
        self.assertFalse(user.is_active)
        user = User.objects.get(username="testActivationCodeUser")
        response = self.client.get(reverse('accounts:activate', args=[
                      user.registrationprofile_set.all()[0].activation_key]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:activate-done'))
        user = authenticate(username='testActivationCodeUser', 
                            password='password')
        self.assertTrue(user.is_active)


class MemberInteractionTestCase(TestCase):
    """
    Tests how a member can interact with the site and manage their account
    """
    fixtures = ['accounts_test_data.json']

    def setUp(self):
        self.test_admin = User.objects.get(pk=1)
        self.test_member = User.objects.get(pk=2)
        self.client.login(username='test_member', password='test')
    
    def testUpdatePassword(self):
        """
        Test to ensure a user can update their password using a form
        """
        response = self.client.get(reverse('accounts:change-password'))
        self.assertEqual(response.status_code, 200)
        post_data = {'old_password' : 'test',
                     'new_password1' : 'password1',
                     'new_password2' : 'password1'}
        response = self.client.post(reverse('accounts:change-password'),
                                    post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:change-password-done'))
        
        user = authenticate(username='test_member', password='password1')
        self.assertEqual(user, self.test_member)
    
    def testUpdateProfile(self):
        """
        Test to ensure a user can update their profile and preferences
        using a form
        """
        response = self.client.get(reverse('accounts:update-profile'))
        self.assertEqual(response.status_code, 200)
        post_data = {'email' : 'test_member_new@example.com',
                     'timezone' : 'UTC',
                     'country' : 'GB',
                     'english_first_language' : 'On',}
        response = self.client.post(reverse('accounts:update-profile'),
                                    post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:my-account'))
        
        # Check the new values are saved
        updated_user = User.objects.get(pk=2)
        self.assertEqual(updated_user.email, 'test_member_new@example.com')
        self.assertEqual(updated_user.userprofile.country, 'GB')
        self.assertEqual(updated_user.userprofile.english_first_language, True)
        
    def testUniqueEmail(self):
        """
        Tests that emails are unique
        """
        post_data = {'email' : 'test_admin@example.com',
                     'timezone' : 'UTC',
                     'country' : 'GB',
                     'english_first_language' : 'On',}
        response = self.client.post(reverse('accounts:register'), post_data)
        self.assertFormError(response,
                             "form", 
                             "email",
                             "This email address is already in use. Please select another")
    
    def testForgottenPassword(self):
        """
        Test to ensure a user can reset their password using their email
        address
        """
        response = self.client.get(reverse('accounts:password-reset'))
        self.assertEqual(response.status_code, 200)
        post_data = {'email' : 'test_member@example.com',}
        response = self.client.post(reverse('accounts:password-reset'),
                                    post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:password-reset-done'))

        response = self.client.get(reverse('accounts:password-reset-done'))
        self.assertEqual(response.status_code, 200)
            
        site = Site.objects.get(id=settings.SITE_ID)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject,
                         'Password reset on %s' % site.domain)
        
        expression = r'^http://(?P<url>.*)/accounts/password-reset-confirm/(?P<uid>[0-9A-Za-z]+)-(?P<token>.+)/$'
        expression = re.compile(expression)
        matches = None
        for line in mail.outbox[0].body.split('\n'):
            matches = expression.match(line)
            if matches is not None:
                break
            
        response = self.client.get(reverse('accounts:password-reset-confirm',
                                           args=[matches.group('uid'),
                                                   matches.group('token')]))
        self.assertEqual(response.status_code, 200)  
        
        post_data = {'new_password1' : 'password1',
                     'new_password2' : 'password1'}
        response = self.client.post(reverse('accounts:password-reset-confirm',
                                     args=[matches.group('uid'),
                                           matches.group('token')]),
                                     post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             reverse('accounts:password-reset-complete'))
        
        user = authenticate(username='test_member', password='password1')
        self.assertEqual(user, self.test_member)
        pass
    
class UserPrivacyTestCase(TestCase):
    """
    Tests how a member can interact with the site and manage their account
    privacy options
    """
    fixtures = ['accounts_test_data.json']

    def setUp(self):
        self.test_admin = User.objects.get(pk=1)
        self.test_member = User.objects.get(pk=2)
        self.client.login(username='test_member', password='test')
        
        self.game_permission = GamePermission()
        self.game_permission.type = 'profile'
        self.game_permission.key = 'profile_email'
        self.game_permission.name = 'View email address'
        self.game_permission.save()

    def testAddingPermissionByKey(self):
        """
        Simply test that a permission can be added by key value
        """
        self.test_member.userprofile.add_permission_by_key('profile_email', 'friend')
        self.test_member.userprofile.add_permission_by_key('profile_email', 'guild')

        self.assertTrue(
                self.test_member.userprofile.has_permission_by_key('profile_email', 
                                                                   'guild'))

        self.assertTrue(
                self.test_member.userprofile.has_permission_by_key('profile_email', 
                                                                   'friend'))

        self.assertFalse(
                self.test_member.userprofile.has_permission_by_key('profile_email', 
                                                                   'member'))

    def testInvalidPermissionByKey(self):
        """
        Tests permission key error handling
        """
        self.assertRaises(GamePermission.DoesNotExist,
                          lambda: self.test_member.userprofile.add_permission_by_key(
                                  'profile_fake', 'friend'))
                          
        self.assertRaises(GamePermission.BadPermissionValue,
                          lambda: self.test_member.userprofile.add_permission_by_key(
                                  'profile_email', 'bad_choice'))
        
        self.test_member.userprofile.add_permission_by_key('profile_email', 'friend')
        self.assertRaises(GamePermission.DuplicatePermissionValue,
                          lambda: self.test_member.userprofile.add_permission_by_key(
                                  'profile_email', 'friend'))

    def testClearPermissions(self):
        """
        Tests the permission reset button performs as expected
        """
        self.test_member.userprofile.add_permission_by_key('profile_email', 'friend')
        self.test_member.userprofile.clear_permissions()
        self.assertFalse(
                self.test_member.userprofile.has_permission_by_key('profile_email', 
                                                                   'friend'))                          