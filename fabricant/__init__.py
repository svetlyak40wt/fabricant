import os

from fabric.api import *
from cuisine import *


def make_symlinks(configs_dir='configs'):
    """Makes symlinks from configs directory
    """
    require('environment')

    if os.path.exists(configs_dir):
        environment = '.' + env.environment

        for root, dirs, files in os.walk('configs'):
            for filename in files:
                if filename.endswith(environment):
                    local_file = os.path.abspath(
                        os.path.join(root, filename)
                    )
                    symlink = os.path.join(
                        root.lstrip(configs_dir),
                        filename[0:-len(environment)]
                    )
                    if not os.path.lexists(symlink):
                        sudo('ln -s "{0}" "{1}"'.format(local_file, symlink))


def use_ssh_config(env):
    import ssh
    import pdb;pdb.set_trace()
    def hostinfo(host, config):
        hive = config.lookup(host)
        if 'hostname' in hive:
            host = hive['hostname']
        if 'user' in hive:
            host = '%s@%s' % (hive['user'], host)
        if 'port' in hive:
            host = '%s:%s' % (host, hive['port'])
        return host

    try:
        config_file = file(os.path.expanduser('~/.ssh/config'))
    except IOError:
        pass
    else:
        config = ssh.config.SSHConfig()
        config.parse(config_file)
        keys = [config.lookup(host).get('identityfile', None)
            for host in env.hosts]
        env.key_filename = [os.path.expanduser(key) for key in keys if key is not None]
        env.hosts = [hostinfo(host, config) for host in env.hosts]

