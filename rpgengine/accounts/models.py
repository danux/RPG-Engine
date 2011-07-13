from django.db import models
from django.db.models.signals import pre_save
from django.contrib.auth.models import User, Group

from rpgengine.accounts.choice_lists import COUNTRIES, TIMEZONES, PERMISSION_TYPES
from rpgengine.accounts.choice_lists import PERMISSION_VALUES
from rpgengine.utils.slug_generator import slug_generator


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
        
    def add_permission(self, game_permission, value):
        if self.has_permission(game_permission, value):
            raise GamePermission.DuplicatePermissionValue()
        
        if not any(value in x for x in PERMISSION_VALUES):
            raise GamePermission.BadPermissionValue()
        
        set_permission = UserProfilePermission()
        set_permission.game_permission = game_permission
        set_permission.value = value
        set_permission.user_profile = self
        set_permission.save()
        
    def has_permission(self, game_permission, value):
        try:
            set_permission = UserProfilePermission.objects.get(user_profile=self,
                                                               game_permission=game_permission,
                                                               value=value)
        except UserProfilePermission.DoesNotExist:
            return False
        else:
            return True
    
    def add_permission_by_key(self, key, value):
        try:
            game_permission = GamePermission.objects.get(key=key)
        except GamePermission.DoesNotExist, e:
            raise e

        self.add_permission(game_permission, value)

    def has_permission_by_key(self, key, value):
        """
        Determines whether or not an account has the value of permission
        key set
        """
        try:
            game_permission = GamePermission.objects.get(key=key)
        except GamePermission.DoesNotExist, e:
            raise e
        
        return self.has_permission(game_permission, value)
    
    def clear_permissions(self):
        self.userprofilepermission_set.all().delete()


class GamePermission(models.Model):
    """
    Class defining various user permissions
    """
    type = models.CharField(max_length=100, choices=PERMISSION_TYPES)
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=100)

    class BadPermissionValue(Exception):
        pass

    class DuplicatePermissionValue(Exception):
        pass

    
class UserProfilePermission(models.Model):
    """
    Class defining the link between a userprofile and a permission, with a 
    value
    """
    user_profile = models.ForeignKey(UserProfile)
    game_permission = models.ForeignKey(GamePermission)
    value = models.CharField(max_length=100, choices=PERMISSION_VALUES)

pre_save.connect(slug_generator, sender=UserProfile)