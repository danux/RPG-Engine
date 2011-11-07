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

class QuestForm(forms.ModelForm):
    """
    Base form for allowing selection of character for quests
    """
    class Meta:
        model = QuestMembership
        fields = ['character',]

    def __init__(self, *args, **kwargs):
        queryset = kwargs['queryset']
        del kwargs['queryset']
        super(QuestForm, self).__init__(*args, **kwargs)
        self.fields['character'] = forms.ModelChoiceField(queryset=queryset)