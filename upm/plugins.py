import sys

from upm_iface import y


def register_plugin_func(func):
    globals()[func.__name__] = func


def dep_name(dep):
    return y.restore_node(dep)['node']()['name']


def dep_list(info, iter):
    return [x(info) for x in iter]
