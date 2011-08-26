import datetime

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class QuestManager(models.Manager):
    """
    Extensions to the default manager to handle common queries specific
    to quests
    """
    def start_quest(self, name, town):
        """
        Method for starting a new quest. The objects should not
        be created directly
        """
        return super(QuestManager, self).create(name=name,
                                                town=town,
                                                is_open=True)

    def get_by_character(self, character):
        """
        Returns the current quest that a character is on
        """
        return self.get(questmembership__character=character,
                        questmembership__date_left__isnull=True)