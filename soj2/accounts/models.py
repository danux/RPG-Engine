from django.db import models
from django.db.models.signals import pre_save
from django.contrib.auth.models import User, Group

from mcnulty.dashboard.fields import HtmlField

from soj2.accounts.choice_lists import COUNTRIES, TIMEZONES, PERMISSION_TYPES
from soj2.utils.slug_generator import slug_generator


class UserProfile(models.Model):
    '''
    Class providing additional meta-information about users, such as their
    date of birth and a public profile about the player.
    '''
    user = models.OneToOneField(User, unique=True)
    name = models.CharField('Pen name', max_length=100, unique=True, 
                            db_index=True)
    slug = models.SlugField()
    avatar = models.ImageField(
            blank=True, null=True,
            upload_to="dynamic/accounts/user-profile/avatars")
    date_of_birth = models.DateField()
    timezone = models.CharField(max_length=50, default="Europe/London",
                                choices=TIMEZONES)
    country = models.CharField(max_length=150, default="GB", choices=COUNTRIES)
    english_first_language = models.NullBooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "author"
        ordering = ['name']
        
    def __unicode__(self):
        return self.name

pre_save.connect(slug_generator, sender=UserProfile)