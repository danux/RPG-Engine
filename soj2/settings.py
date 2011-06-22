import os

from mcnulty.settings import *


PROJECT_ROOT = os.path.dirname(__file__)
STATIC_ROOT = os.path.join(PROJECT_ROOT, "../static-files")
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "../media")
TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, "../templates"),) + TEMPLATE_DIRS
STATIC_URL = '/static-files/'
STATIC_URL = '/media/'
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Set this to a unique, random phrase and keep it secret.
SECRET_KEY = "^brmcy8*+lt!i8fwjceco67&1+d3tn2*@xv4_b1%)9!u+9pj6("

# If you are running multiple Vertex sites on this server, set this to a unique
# phrase.
CACHE_MIDDLEWARE_KEY_PREFIX = "soj2"

# Vertex will send you notifications of broken links found on your website.
# Change this to provide a helpful prefix for all of these emails to help keep
# your inbox well-sorted.
EMAIL_SUBJECT_PREFIX = "[SOJ2]"

# This setting installs the base set of Vertex applications.  Add your own
# custom applications to enable additional functionality for your site.
INSTALLED_APPS += ("sorl.thumbnail",
                   "registration",
                   "django_coverage",
                   "mcnulty.contentpages",
                   "mcnulty.links",
                   "mcnulty.contact",
                   "soj2.utils",
                   "soj2.world",
                   "soj2.accounts",
                   "soj2.characters",
                   "soj2.game")

# Accounts Settings
ACCOUNT_ACTIVATION_DAYS = 7
ROOT_URLCONF = "soj2.urls"
LOGIN_REDIRECT_URL = '/accounts/login/'

# Misc settings
AUTH_PROFILE_MODULE = 'accounts.UserProfile'

TIME_ZONE = 'UTC'

#  Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '%s/soj2.sqlite' % PROJECT_ROOT,
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
