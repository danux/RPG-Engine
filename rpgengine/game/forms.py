from django import forms

from rpgengine.game.models import Quest, QuestMembership


class CreateQuestForm(forms.ModelForm):
    """
    The form used to create a quest
    """
    class Meta:
        model = Quest
        fields = ['name',]
        
class QuestForm(forms.ModelForm):
    """
    Basic form for joining and leaving a quest
    """
    class Meta:
        model = QuestMembership
        fields = ['character',]
        
    def set_character_queryset(self, character_queryset):
        self.fields["character"].queryset = character_queryset

class JoinQuestForm(QuestForm):
    """
    The form used to join a quest
    """
    pass

class CharacterActionForm(forms.Form):
    character = forms.ChoiceField()

    def set_character_queryset(self, character_queryset):
        self.fields["character"].choices = character_queryset.values_list('id', 'character__name')
        
class LeaveQuestForm(CharacterActionForm):
    """
    The form used to leave a quest
    """
    pass
        
class MakeQuestLeaderForm(CharacterActionForm):
    """
    The form used to make a quest leader
    """
    pass
        
class RemoveQuestLeaderForm(CharacterActionForm):
    """
    The form used to remove a quest leader
    """
    pass