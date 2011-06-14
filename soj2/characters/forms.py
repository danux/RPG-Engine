from django import forms

from soj2.characters.models import Character


class ApplicationForm(forms.ModelForm):
    """
    A model form for creating characters. Users are able to save the form and
    return to it later or submit it. Upon submitting the form an email must
    be sent to the GMs responsible for authorising characters.
    """
    class Meta:
        model = Character
        fields =['name',
                  'race',
                  'hometown',
                  'languages', 
                  'back_story',
                  'physical_appearence',
                  'avatar']