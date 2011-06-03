from django.db import models

from mcnulty.dashboard.fields import HtmlField

class WorldNode(models.Model):
    """
    All things in the world are essentially "nodes", sharing some common
    attributes. This class can be extended by everything in the world module.
    """
    name = models.CharField(max_length=150, unique=True)
    description = HtmlField()
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='dynamic/world/world-node', blank=True,
                              null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.name
    
class Language(WorldNode):
    """
    Model representing a langugage in the game.
    """
    pass
    
class Nation(WorldNode):
    """
    Model representing a nation in the game.
    """
    pass
    
class Town(WorldNode):
    """
    Model representing a town in the game.
    """
    nation = models.ForeignKey(Nation)
    is_newbie_friendly = models.NullBooleanField()
    
class Race(WorldNode):
    """
    Model representing a race in the game.
    """
    traditions = HtmlField()
    characteristics = HtmlField()
    physical_appearence = HtmlField()
    home_town = models.ForeignKey(Town)
    language = models.ForeignKey(Langugage)