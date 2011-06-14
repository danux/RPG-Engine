import os

from fabric.api import *
from fabric.contrib.project import rsync_project
from fabsettings import PROJECT_NAME, PRODUCTION_HOST, REMOTE_SITE_DIR
from fabsettings import STAGING_HOST, REMOTE_VIRTUAL_ENV_DIR

from django.conf import settings
from django.core import management

os.environ['DJANGO_SETTINGS_MODULE'] = '%s.settings_local' % PROJECT_NAME

def staging():
    env.hosts = [STAGING_HOST]
    
def production():
    env.hosts = [PRODUCTION_HOST]

def pull_media_from_live():
    """ Downloads the dynamic media folder from the live site """
    local(
        'rsync -pthrvz %s:%s/%s/media/dynamic/ %s/media/dynamic --stats --progress' % (
        PRODUCTION_HOST,
        REMOTE_SITE_DIR,
        PROJECT_NAME,
        PROJECT_NAME)) 

def push_media_to_staging():
    """ Pushes local media to the staging server with rsync """
    local('rsync -pthrvz %s/media/dynamic %s:%s/%s/media/ --stats --progress' % (
            PROJECT_NAME,
            STAGING_HOST,
            REMOTE_SITE_DIR,
            PROJECT_NAME))

def sync():
    """ Download dynamic media from the live site and pushes up to staging """
    pull_media_from_live()
    push_media_to_staging()

def deploy():
    """ Runs a git update on the remote host and touches the wsgi file """
    test()
    with cd(REMOTE_SITE_DIR):
        run('git pull')
        run('touch *.wsgi')

def test():
    """ Tests the project locally """
    management.call_command('test_coverage', 'characters', 'accounts')