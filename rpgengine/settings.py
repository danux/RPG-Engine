import os


SITE_ID = 1
DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_ROOT = os.path.dirname(__file__)
STATIC_ROOT = os.path.join(PROJECT_ROOT, "../static/")
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "../media")
TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, "../templates"),)

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

SECRET_KEY = "^brmcy8*+lt!i8fwjceco67&1+d3tn2*@xv4_b1%)9!u+9pj6("

CACHE_MIDDLEWARE_KEY_PREFIX = "rpgengine"

EMAIL_SUBJECT_PREFIX = "[RPGEngine]"

INSTALLED_APPS = ("django.contrib.auth",
                  "django.contrib.contenttypes",
                  "django.contrib.sessions",
                  "django.contrib.sites",
                  "django.contrib.admin",
                  "django.contrib.admindocs",
                  "django.contrib.redirects",
                  "django.contrib.sitemaps",
                  "django.contrib.messages",
                  "django.contrib.staticfiles",
                  "reversion",
                  "debug_toolbar",
                  "south",
                  "sorl.thumbnail",
                  "registration",
                  "django_coverage",
                  "rpgengine.utils",
                  "rpgengine.world",
                  "rpgengine.accounts",
                  "rpgengine.characters",
                  "rpgengine.game")

TEMPLATE_CONTEXT_PROCESSORS = ("django.core.context_processors.i18n",
                               "django.core.context_processors.request",
                               "django.core.context_processors.media",
                               "django.core.context_processors.static",
                               "django.contrib.auth.context_processors.auth",
                               "django.contrib.messages.context_processors.messages",)

MIDDLEWARE_CLASSES = ("django.middleware.transaction.TransactionMiddleware",
                      "django.middleware.common.CommonMiddleware",
                      "django.contrib.sessions.middleware.SessionMiddleware",
                      "django.contrib.auth.middleware.AuthenticationMiddleware",
                      "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
                      "django.middleware.csrf.CsrfViewMiddleware",
                      "django.contrib.messages.middleware.MessageMiddleware",
                      "debug_toolbar.middleware.DebugToolbarMiddleware",)

ROOT_URLCONF = "rpgengine.urls"
LOGIN_REDIRECT_URL = '/accounts/'

ACCOUNT_ACTIVATION_DAYS = 7
AUTH_PROFILE_MODULE = 'accounts.UserProfile'

TIME_ZONE = 'UTC'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '%s/rpgengine.sqlite' % PROJECT_ROOT,
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}