import sys
import base64

from upm_iface import y


def subst(v):
    def iter_subst():
        yield ('$(WDM)', '$(PREFIX)/m')
        yield ('$(WDR)', '$(PREFIX)/r')
        yield ('$(WDW)', '$(PREFIX)/w')
        yield ('$(WDP)', '$(PREFIX)/p')
        yield ('$(UPM)', y.script_path())
        yield ('$(RM_TMP)', '## ')
        yield ('$(PREFIX)', '$PREFIX')
        yield ('$$', '$')

    return y.subst_kv_base(v, iter_subst())


def build_sh_script(targets, verbose):
    res = [1]
    y.run_makefile(y.main_makefile(verbose), res, targets)
    res = res[1:]

    def iter_cmd():
        yield '#!/bin/sh'

        for cmd in res:
            try:
                cmd = list(*cmd['args'])[6]

                yield '(echo "' + base64.b64encode(subst(cmd)) + '" | base64 -D -i - -o - | /usr/bin/env -i PREFIX=$1 /bin/sh -s) || exit 1'
            except Exception as e:
                y.xprint('------------------------------------------\n', cmd, e)

    return '\n\n'.join(iter_cmd()) + '\n'
