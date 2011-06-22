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
        'rsync -pthrvz %s:%s/media/dynamic/ media/dynamic --stats --progress' % (
        PRODUCTION_HOST,
        REMOTE_SITE_DIR,)) 

def push_media_to_staging():
    """ Pushes local media to the staging server with rsync """
    local('rsync -pthrvz media/dynamic %s:%s/media/ --stats --progress' % (
            STAGING_HOST,
            REMOTE_SITE_DIR))

def sync():
    """ Download dynamic media from the live site and pushes up to staging """
    pull_media_from_live()
    push_media_to_staging()

def deploy():
    """ Runs a git update on the remote host and touches the wsgi file """
    test()
    local('git commit -m "Deploy to %s "' % env.hosts[0])
    with cd(REMOTE_SITE_DIR):
        run('git pull')
        run('workon %s' % PROJECT_NAME)
        run('pip install -r requirements.txt')
        run('touch *.wsgi')
        
def test():
    """ Tests the project locally """
    management.call_command('test_coverage',
                            'accounts',
                            'characters',
                            'game')