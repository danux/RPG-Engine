import os

from fabric.api import *
from fabric.contrib.project import rsync_project
from fabsettings import *

from django.conf import settings
from django.core import management

os.environ['DJANGO_SETTINGS_MODULE'] = 'soj2.settings_local'

def staging():
    env.hosts = [STAGING_HOST]
    
def production():
    env.hosts = [PRODUCTION_HOST]

def pull_media_from_live():
    local(
          'rsync -pthrvz %s:%s/%s/media/dynamic/ %s/media/dynamic --stats --progress' % (
            PRODUCTION_HOST,
            REMOTE_SITE_DIR,
            PROJECT_NAME,
            PROJECT_NAME
          )
      ) 

def push_media_to_staging():
    local('rsync -pthrvz %s/media/dynamic %s:%s/%s/media/ --stats --progress' % (
            PROJECT_NAME,
            STAGING_HOST,
            REMOTE_SITE_DIR,
            PROJECT_NAME
          )
    )    

def sync():
    pull_media_from_live()
    push_media_to_staging()
    
def deploy():
    """ Runs an svn update on the remote host and touches the wsgi file """
    with cd(REMOTE_SITE_DIR):
        run('git pull')
        run('touch *.wsgi')

def test():
    """ Tests the project locally """
    print '== Testing accounts'
    management.call_command('test', 'accounts')
    
    print '== Testing characters'
    management.call_command('test', 'characters')