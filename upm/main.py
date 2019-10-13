import os
import json

from .user import gen_packs, load_plugins
from .build import build_makefile


def main(prefix, plugins, kof):
    if plugins:
        load_plugins(plugins, kof)

    node = {
        'node': {
            'name': 'all',
            'from': __file__,
	    'build': [],
        },
        'deps': list(gen_packs())
    }

    data = build_makefile(node, prefix=prefix)

    if 0:
        for l in data.split('\n'):
            if '$(' in l:
                raise Exception('shit happen ' + l)

    return data
