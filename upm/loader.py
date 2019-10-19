import os
import imp
import sys
import itertools

from .user import helper
from .ft import cached
from .db import store_node
from .xpath import xp


def load_plugins_code(where):
    def iter_plugins():
        for x in os.listdir(where):
            if '~' not in x and '#' not in x:
                path = where + '/' + x

                with open(path, 'r') as f:
                    yield path, f.read()

    return dict(iter_plugins())


def load_plugins_base(plugins):
    exec '\n'.join(sorted((v for v in plugins.values()), key=lambda x: -len(x))) in globals()


def load_plugins(where):
    builtin_plugins = {}
    ## builtin_plugins
    load_plugins_base(builtin_plugins)

    for x in itertools.chain(where):
        load_plugins_base(load_plugins_code(os.path.abspath(x)))
