import os

from mcnulty.settings import *

PROJECT_ROOT = os.path.dirname(__file__)

MEDIA_ROOT = os.path.join(PROJECT_ROOT, "media")

TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, "templates"),) + TEMPLATE_DIRS

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

# Database settings.  Leave these as they are to use the default built-in
# SQLite database.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'soj2.sqlite',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Email settings.
SERVER_EMAIL = "daniel@amarus.co.uk"
DEFAULT_FROM_EMAIL = "daniel@amarus.co.uk"

# This setting installs the base set of Vertex applications.  Add your own
# custom applications to enable additional functionality for your site.

INSTALLED_APPS += ("django.contrib.staticfiles",
                   "sorl.thumbnail",
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

ACCOUNT_ACTIVATION_DAYS = 7

ROOT_URLCONF = "soj2.urls"

ADMIN_MEDIA_PREFIX = "/media/lib/admin/"

STATIC_DOC_ROOT = '/srv/sites/soj2/soj2/media'

LOGIN_REDIRECT_URL = '/'

AUTH_PROFILE_MODULE = 'accounts.UserProfile'

ADMINS = (
     ('Amarus Support', 'support@amarus.co.uk'),
)

MANAGERS = ADMINS

TIME_ZONE = 'UTC'

LATEST_NEWS_SLUG = 'blah'
MIDDLEWARE_CLASSES += ("django.middleware.csrf.CsrfViewMiddleware",)
TEMPLATE_CONTEXT_PROCESSORS += ("django.core.context_processors.static",)