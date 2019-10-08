import os
import sys

from all import RES
from build import build_package
from user import USER_PACKAGES


if __name__ == '__main__':
    for bb in [USER_PACKAGES[x] for x in [4]]:
        print build_package(bb)
