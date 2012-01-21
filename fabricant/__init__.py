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
