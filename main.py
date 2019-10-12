import os
import sys
import json

from user import gen_packs, USER_PACKAGES, TOOLS
from build import build_makefile


if __name__ == '__main__':
    if 'prune' in sys.argv:
        if 0:
            prune_repo()
    else:
        val, param = sys.argv[1].split('=')

        if val == 'prefix':
            prefix = param
        else:
            prefix = ''

        node = {
            'node': {
                'name': 'all',
                'from': __file__,
		'build': [],
            },
            'deps': list(gen_packs())
        }

        data = build_makefile(node, prefix=prefix)

        print >>sys.stderr, data
        print data
