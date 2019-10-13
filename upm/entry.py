import sys
import os

from build import prepare_pkg, get_pkg_link


if __name__ == '__main__':
    args = sys.argv[sys.argv.index('--') + 1:]

    globals()[args[0]](*args[1:])
