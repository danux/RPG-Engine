from django import forms

from rpgengine.characters.models import Character


class RejectCharacterApplicationForm(forms.ModelForm):
    """
    This form allows a GM to leave information for a user as to why they have
    not had their character approved.
    """
    class Meta:
        model = Character
        fields =['gm_notes']