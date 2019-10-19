import os
import sys
import subprocess

from .user import gen_packs
from .build import build_makefile
from .ft import singleton


@singleton
def docker_binary():
   return subprocess.check_output(['/bin/sh -c "which docker"'], shell=True).strip()


@singleton
def tool_binary():
   if sys.argv[0].endswith('upm'):
      return os.path.abspath(sys.argv[0])

   res = os.path.abspath(__file__)

   if 'main.py' in res:
      res = os.path.dirname(os.path.dirname(res)) + '/cli'

   return res


def main(verbose):
    return build_makefile(list(gen_packs()), verbose)
