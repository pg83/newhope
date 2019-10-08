import os
import sys

from all import RES
from build import build_package
from user import USER_PACKAGES, prune_repo


if __name__ == '__main__':
    if 'prune' in sys.argv:
        prune_repo()
    else:
        for bb in [USER_PACKAGES[x] for x in [9, 10]]:
            print build_package(bb)
