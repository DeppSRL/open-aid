from fabric.api import run, env, cd, task
from fabric.contrib.files import sed, contains
from fabric.colors import green
from fabvenv import virtualenv

env.hosts = ['staging', ] + env.hosts
env.user = 'root'
env.directory = '/home/open-aid'
env.venv = '/home/virtualenvs/open-aid'


def manage(cmd):
    run('python project/manage.py %s' % cmd)

def welcome():
    print(green("Executing on %(host)s as %(user)s" % env))

def reload():
    run('touch config/uwsgi.ini')

@task
def update_release():
    welcome()
    with virtualenv(env.venv):
        with cd(env.directory):
            run('git pull')
            manage('compilemessages')
            manage('collectstatic --noinput')
            reload()
@task
def open_release():
    welcome()
    with cd(env.directory):
        if contains('config/.env', 'EARLYBIRD_ENABLE=0'):
            print 'Already Opened'
        else:
            sed('config/.env', 'EARLYBIRD_ENABLE=1', 'EARLYBIRD_ENABLE=0')
            reload()
@task
def close_release():
    welcome()
    with cd(env.directory):

        if contains('config/.env', 'EARLYBIRD_ENABLE=1'):
            print 'Already Closed'
        else:
            sed('config/.env', 'EARLYBIRD_ENABLE=0', 'EARLYBIRD_ENABLE=1')
            reload()
