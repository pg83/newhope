import os
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
    vvv = dict()

    def iter_modules():
        for i, x in enumerate(sorted(plugins.keys())):
            vvv[os.path.basename(x)] = i

    iter_modules()

    vvv['splitter.py'] = -1

    for x in sorted(plugins.keys(), key=lambda x: vvv[os.path.basename(x)]):
        data = plugins[x]

        exec data in globals()


def load_plugins(where):
    builtin_plugins = {}
    ## builtin_plugins
    load_plugins_base(builtin_plugins)

    for x in itertools.chain(where):
        load_plugins_base(load_plugins_code(os.path.abspath(x)))
