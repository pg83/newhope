from .user import gen_packs
from .build import build_makefile
from .db import store_node


def main(verbose):
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
