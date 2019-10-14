import os
import json

from .user import gen_packs, load_plugins, store_node
from .build import build_makefile


def main(prefix, plugins, kof, rm_tmp, install_dir):
    assert plugins

    load_plugins(plugins.replace('$(PREFIX)', prefix), kof)

    node = {
        'node': {
            'name': 'all',
            'from': __file__,
	    'build': [],
        },
        'deps': list(gen_packs())
    }

    return build_makefile(store_node(node), prefix=prefix, rm_tmp=rm_tmp, install_dir=install_dir)
