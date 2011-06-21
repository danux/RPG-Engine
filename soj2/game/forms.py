from django import forms

from soj2.game.models import Quest


class CreateQuestForm(forms.ModelForm):
    """
    The form used to create a quest
    """
    class Meta:
        model = Quest
        
    def set_character_queryset(self, character_queryset):
        self.fields["characters"].queryset = character_queryset