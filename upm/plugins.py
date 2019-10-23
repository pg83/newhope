import sys

from upm_iface import y
import upm_decor as decor


GENERATED = {}


def dep_name(dep):
    return y.restore_node(dep)['node']()['name']


def dep_list(info, iter):
    return [x(info) for x in iter]

