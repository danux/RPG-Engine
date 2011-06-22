import os
from datetime import datetime

from fabric.api import *
from fabric.contrib.project import rsync_project
from fabsettings import PROJECT_NAME, PRODUCTION_HOST, REMOTE_SITE_DIR
from fabsettings import STAGING_HOST, REMOTE_VIRTUAL_ENV_DIR

from django.conf import settings
from django.core import management


os.environ['DJANGO_SETTINGS_MODULE'] = '%s.settings_local' % PROJECT_NAME

def staging():
    env.hosts = [STAGING_HOST]
    env.name = 'staging'
    
def production():
    env.hosts = [PRODUCTION_HOST]
    env.name = 'production'

def virtualenv(command):
    """ Executes a command inside the remote virtualenv """
    run('workon %s && %s' % (PROJECT_NAME, command))

def pull_live_media():
    """ Downloads the dynamic media folder from the live site """
    local(
        'rsync -pthrvz %s:%s/media/dynamic/ media/dynamic --stats --progress' % (PRODUCTION_HOST,
                                                                                 REMOTE_SITE_DIR,)) 

def push_staging_media():
    """ Pushes local media to the staging server with rsync """
    local('rsync -pthrvz media/dynamic %s:%s/media/ --stats --progress' % (STAGING_HOST,
                                                                           REMOTE_SITE_DIR))

def sync():
    """ Download dynamic media from the live site and pushes up to staging """
    pull_live_media()
    push_staging_media()

def deploy():
    """ Runs a git update on the remote host and touches the wsgi file """
    test()
    tag_name = datetime.now().strftime("deployment-%Y-%m-%d--%H-%M-%S")
    local('git tag %s' % tag_name)
    local('git push origin %s' % tag_name)
    with cd(REMOTE_SITE_DIR):
        run('git pull')
        run('pip install -E %s/bin/python -r requirements.txt' % REMOTE_VIRTUAL_ENV_DIR)
        run('touch *.wsgi')
        
    with cd('%s/%s' % (REMOTE_SITE_DIR, PROJECT_NAME)):
        virtualenv('django-admin.py syncdb --settings=%s.settings_%s' % (PROEJCT_NAME,
                                                                         env.name))
        virtualenv('django-admin.py migrate --settings=%s.settings_%s' % (PROEJCT_NAME,
                                                                          env.name))
        
def test():
    """ Tests the project locally """
    management.call_command('test_coverage',)