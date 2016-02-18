from fabric.operations import local, put, sudo, run
from fabric.context_managers import lcd, cd


def _package():
    with lcd('/home/taar/git/speakers_corner/'):
        local('/home/taar/.virtualenvs/speakers_corner/bin/python2.7 '
              'setup.py sdist')
        put('dist/SpeakersCorner-0.0-py2.7.egg')
        put('dist/SpeakersCorner-0.0.tar.gz')


def restart_process():
    # sudo('mv speakers_corner.conf /etc/supervisor/conf.d/speakers_corner.conf')
    # sudo('chown root:root /etc/supervisor/conf.d/speakers_corner.conf')
    sudo('mv init.d/speakers_corner /etc/init.d/speakers_corner')
    sudo('chown root:root /etc/init.d/speakers_corner')
    sudo('chmod u+x /etc/init.d/speakers_corner')
    sudo('service speakers_corner stop', warn_only=True)
    sudo('service speakers_corner start &')


def deploy_to_rpi():
    _package()

    # run('mkdir speakers-corner')
    with cd('speakers_corner'):
        run('mv ../SpeakersCorner-0.0-py2.7.egg ./')
        run('mv ../SpeakersCorner-0.0.tar.gz ./')
        run('tar -zxvpf SpeakersCorner-0.0.tar.gz')
        with cd('SpeakersCorner-0.0'):
            sudo('python setup.py install')
            run('mv run.py /home/pi/run.py')
            #restart_process()
