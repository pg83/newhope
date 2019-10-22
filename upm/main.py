import os
import sys
import subprocess

from upm_iface import y
from upm_build import build_makefile
from upm_ft import singleton


@singleton
def docker_binary():
   return subprocess.check_output(['/bin/sh -c "which docker"'], shell=True).strip()


def main(verbose):
   return build_makefile(list(y.gen_packs()), verbose)
