import sys
import base64

from .main import tool_binary, main as main_makefile
from .run_make import run_makefile
from .subst import subst_kv_base
from .helpers import xprint


def subst(v):
    def iter_subst():
        yield ('$(WDM)', '$(PREFIX)/m')
        yield ('$(WDR)', '$(PREFIX)/r')
        yield ('$(WDW)', '$(PREFIX)/w')
        yield ('$(WDP)', '$(PREFIX)/p')
        yield ('$(UPM)', tool_binary())
        yield ('$(RM_TMP)', '## ')
        yield ('$(PREFIX)', '$PREFIX')
        yield ('$$', '$')

    return subst_kv_base(v, iter_subst())


def build_sh_script(targets, verbose):
    res = [1]
    run_makefile(main_makefile(verbose), res, targets)
    res = res[1:]

    def iter_cmd():
        yield '#!/bin/sh'

        for cmd in res:
            try:
                cmd = list(*cmd['args'])[6]

                yield '(echo "' + base64.b64encode(subst(cmd)) + '" | base64 -D -i - -o - | /usr/bin/env -i PREFIX=$1 /bin/sh -s) || exit 1'
            except Exception as e:
                xprint('------------------------------------------\n', cmd, e)

    return '\n\n'.join(iter_cmd()) + '\n'
