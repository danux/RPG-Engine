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

from soj2.accounts.forms import RegistrationFormWithFields
from soj2.accounts.models import UserProfile, GamePermission


class RegistrationTestCase(TestCase):
    """
    Tests various aspects of the registration system
    """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testUniqueUsername(self):
        """ 
        Tests that usernames must be unique by attempting to register the same
        username twice
        """
        user = User.objects.create_user(username='user1',
                                        password='pass1',
                                        email='daniel@amarus.co.uk')

    def testUniqueName(self):
        """
        Tests that pen names are unique
        """
        user1 = User.objects.create_user(username='user2', 
                                         password='pass1',
                                         email='daniel@amarus.co.uk')
        user2 = User.objects.create_user(username='user3',
                                         password='pass1',
                                         email='daniel@amarus.co.uk')
        user_profile1 = UserProfile(user=user1, name='Test', 
                                        date_of_birth=datetime.date.today())
        user_profile1.save()
        
        post_data = {
            'name' : 'Test',
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
    def setUp(self):
        self.user = User.objects.create_user('test',
                                             'daniel@amarus.co.uk',
                                             'test')
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        profile = UserProfile(name='Test',
                              date_of_birth=datetime.datetime(1986, 8, 16),
                              user=self.user)
        profile.save()
        self.client.login(username='test', password='test')
    
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
        
        user = authenticate(username='test', password='password1')
        self.assertEqual(user, self.user)
    
    def testUpdateProfile(self):
        """
        Test to ensure a user can update their profile and preferences
        using a form
        """
        response = self.client.get(reverse('accounts:update-profile'))
        self.assertEqual(response.status_code, 200)
        post_data = {'email' : 'daniel@danux.co.uk',
                     'timezone' : 'UTC',
                     'country' : 'GB',
                     'english_first_language' : 'On',}
        response = self.client.post(reverse('accounts:update-profile'),
                                    post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:my-account'))
        
        # Check the new values are saved
        updated_user = User.objects.get(pk=1)
        self.assertEqual(updated_user.email, 'daniel@danux.co.uk')
        self.assertEqual(updated_user.userprofile.country, 'GB')
        self.assertEqual(updated_user.userprofile.english_first_language, True)
    
    def testForgottenPassword(self):
        """
        Test to ensure a user can reset their password using their email
        address
        """
        response = self.client.get(reverse('accounts:password-reset'))
        self.assertEqual(response.status_code, 200)
        post_data = {'email' : 'daniel@amarus.co.uk',}
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
        
        user = authenticate(username='test', password='password1')
        self.assertEqual(user, self.user)
        pass
    
class UserPrivacyTestCase(TestCase):
    """
    Tests how a member can interact with the site and manage their account
    """
    def setUp(self):
        self.user = User.objects.create_user('test',
                                             'daniel@amarus.co.uk',
                                             'test')
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        profile = UserProfile(name='Test',
                              date_of_birth=datetime.datetime(1986, 8, 16),
                              user=self.user)
        profile.save()
        self.client.login(username='test', password='test')
        
        self.game_permission = GamePermission()
        self.game_permission.type = 'profile'
        self.game_permission.key = 'profile_email'
        self.game_permission.name = 'View email address'
        self.game_permission.save()

    """
    Tests the UserPrivacy settings module
    """
    def testAddingPermissionByKey(self):
        """
        Simply test that a permission can be added by key value
        """
        self.user.userprofile.add_permission_by_key('profile_email', 'friend')
        self.user.userprofile.add_permission_by_key('profile_email', 'guild')

        self.assertTrue(
                self.user.userprofile.has_permission_by_key('profile_email', 
                                                            'guild'))

        self.assertTrue(
                self.user.userprofile.has_permission_by_key('profile_email', 
                                                            'friend'))

        self.assertFalse(
                self.user.userprofile.has_permission_by_key('profile_email', 
                                                            'member'))

    def testInvalidPermissionByKey(self):
        """
        Tests permission key error handling
        """
        self.assertRaises(GamePermission.DoesNotExist,
                          lambda: self.user.userprofile.add_permission_by_key(
                                  'profile_fake', 'friend'))
                          
        self.assertRaises(GamePermission.BadPermissionValue,
                          lambda: self.user.userprofile.add_permission_by_key(
                                  'profile_email', 'bad_choice'))
        
        self.user.userprofile.add_permission_by_key('profile_email', 'friend')
        self.assertRaises(GamePermission.DuplicatePermissionValue,
                          lambda: self.user.userprofile.add_permission_by_key(
                                  'profile_email', 'friend'))

    def testClearPermissions(self):
        """
        Tests the permission reset button performs as expected
        """
        self.user.userprofile.add_permission_by_key('profile_email', 'friend')
        self.user.userprofile.clear_permissions()
        self.assertFalse(
                self.user.userprofile.has_permission_by_key('profile_email', 
                                                            'friend'))                          