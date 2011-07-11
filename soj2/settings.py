import os

PROJECT_ROOT = os.path.dirname(__file__)
STATIC_ROOT = os.path.join(PROJECT_ROOT, "../static-files")
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "../media")
TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, "../templates"),)
STATIC_URL = '/static-files/'
STATIC_URL = '/media/'
DEBUG = True
TEMPLATE_DEBUG = DEBUG
SITE_ID = 1

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
INSTALLED_APPS = ("django.contrib.auth",
                  "django.contrib.contenttypes",
                  "django.contrib.sessions",
                  "django.contrib.sites",
                  "django.contrib.admin",
                  "django.contrib.admindocs",
                  "django.contrib.redirects",
                  "django.contrib.sitemaps",
                  "django.contrib.syndication",
                  "django.contrib.messages",
                  "django.contrib.staticfiles",
                  "reversion",
                  "debug_toolbar",
                  "south",
                  "sorl.thumbnail",
                  "registration",
                  "django_coverage",
                  "soj2.utils",
                  "soj2.world",
                  "soj2.accounts",
                  "soj2.characters",
                  "soj2.game")

TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
                               "django.contrib.messages.context_processors.messages",
                               "django.core.context_processors.i18n",
                               "django.core.context_processors.request",
                               "django.core.context_processors.media",
                               "django.core.context_processors.static")

MIDDLEWARE_CLASSES = ("django.middleware.transaction.TransactionMiddleware",
                      "django.middleware.common.CommonMiddleware",
                      "django.contrib.sessions.middleware.SessionMiddleware",
                      "django.contrib.auth.middleware.AuthenticationMiddleware",
                      "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
                      "django.middleware.csrf.CsrfViewMiddleware",
                      "django.contrib.messages.middleware.MessageMiddleware",
                      "debug_toolbar.middleware.DebugToolbarMiddleware",)

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
