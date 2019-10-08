import os
import sys

from all import RES
from build import build_package
from user import USER_PACKAGES, prune_repo, install_xz


if __name__ == '__main__':
    install_xz()

    if 'prune' in sys.argv:
        pass
        #prune_repo()
    else:
        for bb in USER_PACKAGES:
            print build_package(bb)
