import os

from all import RES
from build import build_package
from user import gen_bb, USER_PACKAGES


if __name__ == '__main__':
    for bb in [USER_PACKAGES[1]]:
        print build_package(bb)
