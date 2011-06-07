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
        user = User.objects.create_user(username='user1', password='pass1', 
                                                    email='daniel@amarus.co.uk')
        
        self.assertRaises(IntegrityError, lambda: User.objects.create_user(
               username='user1', password='pass1', email='daniel@amarus.co.uk'))

    def testUniqueName(self):
        """
        Tests that pen names are unique
        """
        user1 = User.objects.create_user(username='user2', password='pass1', 
                                                    email='daniel@amarus.co.uk')
        user2 = User.objects.create_user(username='user3', password='pass1', 
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
    Tests permissions and block lists
    """
    pass