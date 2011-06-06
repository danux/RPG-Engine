from django.db import models
from django.contrib.auth.models import User, Group

from soj2.accounts.choice_lists import COUNTRIES, TIMEZONES


class SocialNetwork(models.Model):
    '''
    Class representing a social network, i.e. Facebook, Twitter, Myspace
    '''
    title = models.CharField(max_length=255, unique=True)
    icon = models.ImageField(upload_to="dynamic/accounts/social-network/icons")
    link_to_expression = models.CharField(max_length=255)
    help_text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


class InstantMessenger(models.Model):
    '''
    Class representing an instant messenger program
    '''
    title = models.CharField(max_length=255, unique=True)
    icon = models.ImageField(upload_to=
                             "dynamic/accounts/instant-messenger/icons")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


class UserProfile(models.Model):
    '''
    Class providing additional meta-information about users, such as their
    date of birth and a public profile about the player.
    '''
    user = models.OneToOneField(User, unique=True)
    pen_name = models.CharField(max_length=100, unique=True, db_index=True)
    avatar = models.ImageField(
            blank=True, null=True,
            upload_to="dynamic/accounts/user-profile/avatars")
    date_of_birth = models.DateField()
    social_networks = models.ManyToManyField(
            SocialNetwork, blank=True,
            null=True, through="SocialNetworkMembership")
    instant_messengers = models.ManyToManyField(
            InstantMessenger, blank=True, null=True,
            through="InstantMessengerMembership")
    timezone = models.CharField(max_length=50, default="Europe/London",
                                choices=TIMEZONES)
    country = models.CharField(max_length=150, default="GB", choices=COUNTRIES)
    english_first_language = models.NullBooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "author"
        ordering = ['pen_name']
        
    def __unicode__(self):
        return self.pen_name


class SocialNetworkMembership(models.Model):
    '''
    Class representing a user's identity on a social network. Users may select
    a supported social network and share their id on their public profile.
    Other users are then provided a link to the user's page on said social
    network.
    '''
    user_profile = models.ForeignKey(UserProfile)
    social_network = models.ForeignKey(SocialNetwork)
    link_to_identifier = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        order_with_respect_to = 'social_network'


class InstantMessengerMembership(models.Model):
    '''
    Class representing a user's identity on a social network. Users may select
    a supported social network and share their id on their public profile.
    Other users are then provided a link to the user's page on said social
    network.
    '''
    user_profile = models.ForeignKey(UserProfile)
    instant_messenger = models.ForeignKey(InstantMessenger)
    username = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        order_with_respect_to = 'instant_messenger'


class FollowedUserProfile(models.Model):
    '''
    Class representing a relationship between 2 UserProfiles. A UserProfile
    may follow another and receive updates in their feed.
    '''
    follower = models.ForeignKey(UserProfile, related_name='following')
    following = models.ForeignKey(UserProfile, related_name='followers')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-date_created"]

    
class BlockedUserProfile(models.Model):
    '''
    Class representing a user's desire to block another user from contacting
    them.
    '''
    user = models.ForeignKey(UserProfile, related_name='block_list')
    blocked = models.ForeignKey(UserProfile, related_name='blocked_by')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-date_created"]