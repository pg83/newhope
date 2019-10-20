import os
import imp
import sys
import itertools


def load_plugins_code(where):
    def iter_plugins():
        for x in os.listdir(where):
            if '~' not in x and '#' not in x:
                path = where + '/' + x

                with open(path, 'r') as f:
                    yield path, f.read()

    return list(iter_plugins())


def load_plugins_base(plugins, into=globals()):
    data = '\n'.join(sorted((v[1] for v in plugins), key=lambda x: -len(x)))

    exec data in into


def get_builtin_plugins():
    builtin_plugins = {}
    ## builtin_plugins
    return builtin_plugins


def load_plugins(where, into):
    def iter_plugins():
        for p in where:
            if p == 'builtin':
                for x in get_builtin_plugins():
                    yield x
            else:
                for x in load_plugins_code(os.path.abspath(p)):
                    yield x

    load_plugins_base(iter_plugins(), into)
