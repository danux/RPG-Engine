from django import forms

from rpgengine.game.models import Quest, QuestMembership


class CreateQuestForm(forms.ModelForm):
    """
    The form used to create a quest
    """
    
    def __init__(self, *args, **kwargs):
        queryset = kwargs['queryset']
        del kwargs['queryset']
        super(CreateQuestForm, self).__init__(*args, **kwargs)
        self.fields['character'] = forms.ModelChoiceField(queryset=queryset)
    
    class Meta:
        model = Quest
        fields = ['name',]


class JoinQuestForm(forms.ModelForm):
    """
    The form used to join a quest
    """
    class Meta:
        model = QuestMembership
        fields = ['character',]

    def set_character_queryset(self, query_set):
        self.fields["character"].choices = query_set.values_list('id', 'name')