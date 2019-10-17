from .user import gen_packs, load_plugins
from .build import build_makefile
from .db import store_node


def main(plugins, verbose):
    load_plugins(plugins)

    node = {
        'node': {
            'name': 'all',
            'from': __file__,
	    'build': [],
            'codec': 'tr',
        },
        'deps': list(gen_packs())
    }

    return build_makefile(store_node(node), verbose)
