import os

from all import RES
from build import build_package
from user import USER_PACKAGES


if __name__ == '__main__':
    for bb in [USER_PACKAGES[3]]:
        print build_package(bb)
