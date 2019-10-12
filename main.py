import os
import sys
import json

from user import gen_packs, load_plugins
from build import build_makefile


if __name__ == '__main__':
    if 'prune' in sys.argv:
        if 0:
            prune_repo()
    else:
        prefix = ''

        for arg in sys.argv[1:]:
            val, param = arg.split('=')

            if val == 'prefix':
                prefix = param

            if val == 'plugins':
                load_plugins(param)

        node = {
            'node': {
                'name': 'all',
                'from': __file__,
		'build': [],
            },
            'deps': list(gen_packs())
        }

        data = build_makefile(node, prefix=prefix)

        print data
