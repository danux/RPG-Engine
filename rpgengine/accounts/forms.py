from datetime import date
from dateutil.relativedelta import relativedelta

from django import forms
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget
from registration.forms import RegistrationForm

from rpgengine.accounts.choice_lists import TIMEZONES, COUNTRIES
from rpgengine.accounts.models import UserProfile

class RegistrationFormWithFields(RegistrationForm):
    """
    A sub class of the django-registration app's registration form. This form
    adds in the specific fields for RPGEngine and validates them.
    """
    name = forms.CharField(widget=forms.TextInput, label="Pen name",
                   help_text="How you will be known, as an author, in the game")
    date_of_birth = forms.DateField(widget=SelectDateWidget(years=range(1900,2011)))
    timezone = forms.ChoiceField(choices=TIMEZONES, initial="Europe/London")
    country = forms.ChoiceField(choices=COUNTRIES, initial='GB')
    english_first_language = forms.BooleanField(required=False,
             help_text=("Check this box if English is not your first language. "
             "This option does not affect play, but allows GMs and other players "
             " to be more understanding towards authors who do not speak English "
             "as a native language."))
    
    def clean_name(self):
        try:
            UserProfile.objects.get(name=self.cleaned_data['name'])
        except UserProfile.DoesNotExist:
            return self.cleaned_data['name']
        else:
            raise forms.ValidationError((
                                "This pen name is already in use. Please select"
                                " another"))
    
    def clean_email(self):
        try:
            User.objects.get(email=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']
        else:
            raise forms.ValidationError((
                                "This email address is already in use. Please select"
                                " another"))
    
    def clean_date_of_birth(self):
        max_dob = date.today() + relativedelta(years=-13)
        if max_dob < self.cleaned_data['date_of_birth']:
            raise forms.ValidationError(
                                'You must be at least 13 years old to play')
        return self.cleaned_data['date_of_birth']

class UpdateAccountForm(forms.Form):
    """
    A form used by users to update their account and author details
    """
    email = forms.EmailField()
    timezone = forms.ChoiceField(choices=TIMEZONES)
    country = forms.ChoiceField(choices=COUNTRIES)
    english_first_language = forms.BooleanField(required=False,
             help_text=("Check this box if English is not your first language. "
             "This option does not affect play, but allows GMs and other players "
             " to be more understanding towards authors who do not speak English "
             "as a native language."))
                    
    def clean_email(self):
        if self.initial['email'] != self.cleaned_data['email']:
            try:
                User.objects.get(email=self.cleaned_data['email'])
            except User.DoesNotExist:
                pass
            else:
                raise forms.ValidationError((
                                    "This email address is already in use. Please select"
                                    " another"))
        return self.cleaned_data['email']