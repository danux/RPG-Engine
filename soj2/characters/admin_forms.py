from django import forms

from mcnulty.dashboard.fields import HtmlWidget

from soj2.characters.models import Character


class RejectCharacterApplicationForm(forms.ModelForm):
    """
    This form allows a GM to leave information for a user as to why they have
    not had their character approved.
    """
    gm_notes = forms.CharField(widget=HtmlWidget())
    
    class Meta:
        model = Character
        fields =['gm_notes']