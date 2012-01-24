import os

from fabric.api import *
from fabric.operations import _shell_escape

from cuisine import *
from cuisine import run as _cuisine_run


def make_symlinks(configs_dir='configs'):
    """Makes symlinks from configs directory
    """
    require('environment')
    require('project_dir')

    if os.path.exists(configs_dir):
        environment = '.' + env.environment

        for root, dirs, files in os.walk('configs'):
            for filename in files:
                if filename.endswith(environment):
                    local_file = os.path.join(env.project_dir, root, filename)
                    symlink = os.path.join(
                        root.lstrip(configs_dir),
                        filename[0:-len(environment)]
                    )
                    if not file_exists(symlink):
                        sudo('ln -s "{0}" "{1}"'.format(local_file, symlink))


def use_ssh_config(env):
    import ssh
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


def _run_with_agent(command, shell=True, pty=True, ssh_options='-A'):
    """
    Helper function.
    Runs a command with SSH agent forwarding enabled.

    Note:: Fabric (and paramiko) can't forward your SSH agent.~
    This helper uses your system's ssh to do so.
    """
    env = fabric.api.env
    real_command = command
    if shell:
        cwd = env.get('cwd', '')
        if cwd:
            cwd = 'cd %s && ' % _shell_escape(cwd)
        real_command = '%s "%s"' % (env.shell,
            _shell_escape(cwd + real_command))

    if fabric.api.output.debug:
        print("[%s] run: %s" % (env.host_string, real_command))
    elif fabric.api.output.running:
        print("[%s] run: %s" % (env.host_string, command))

    return fabric.api.local("ssh {options} -p {env.port} {env.host} '{command}'".format(
            env=env,
            command=real_command,
            options=ssh_options,
        )
    )


def run(*args, **kwargs):
    if kwargs.get('forward_agent', False):
        new_kwargs = dict(item for item in kwargs.items() if item[0] in ('shell', 'pty'))
        return _run_with_agent(*args, **new_kwargs)
    return _cuisine_run(*args, **kwargs)

run.__doc__ = _cuisine_run.__doc__ + """

If there is 'forward_agent=True in the kwargs, then this command
will run true 'ssh' client locally. This is because pythonic 'ssh'
library still lack this feature.
"""

