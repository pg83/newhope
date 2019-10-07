import os

from all import RES
from build import build_package


if __name__ == '__main__':
    for pkg in RES:
        if 'id' in pkg:
            where = build_package(pkg)
            to = '/repo/' + pkg['id']

            os.rename(where, to)
