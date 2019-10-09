import os
import sys

from user import build_package, gen_packs, prune_repo


if __name__ == '__main__':
    if 'prune' in sys.argv:
        if 0:
            prune_repo()
    else:
        for bb in gen_packs():
            print build_package(bb)
