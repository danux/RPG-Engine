from django.db import models
from django.db.models.signals import pre_save
from django.contrib.auth.models import User, Group

from mcnulty.dashboard.fields import HtmlField

from soj2.world.models import Town
from soj2.utils.slug_generator import slug_generator


class Quest(models.Model):
    
    name = models.CharField(max_length=150)
    slug = models.SlugField()
    is_open = models.BooleanField()
    town = models.ForeignKey(Town)

pre_save.connect(slug_generator, sender=Quest)