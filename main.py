import os

from all import RES
from build import build_package
from user import gen_bb


if __name__ == '__main__':
    bb = gen_bb('https://www.busybox.net/downloads/busybox-1.30.1.tar.bz2')

    print build_package(bb)
