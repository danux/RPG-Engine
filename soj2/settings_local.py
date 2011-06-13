from soj2.settings import *

SHOW_UNPUBLISHED_PAGES = False

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEBUG = True
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG

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