import os
import sys
import json

from user import gen_packs, USER_PACKAGES
from build import build_makefile


if __name__ == '__main__':
    if 'prune' in sys.argv:
        if 0:
            prune_repo()
    else:
        for bb in [USER_PACKAGES['m4']({'target': 'aarch64', 'host': 'x86_64'})]: #gen_packs():
            print >>sys.stderr, build_makefile(bb)

