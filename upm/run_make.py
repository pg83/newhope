import os
import sys
import subprocess
import random
import traceback

from upm_iface import y


def new_cmd():
    return {
        'cmd': [],
    }


BASH_RUNTIME = """
set -e
set -x

rmmkcd() {
    (rm -rf "$1" || true) && (mkdir -p "$1") && cd "$1"
}

mkcd() {
    mkdir -p "$1" && cd "$1"
}
"""


def run_makefile(data, shell_out, targets):
    lst = []
    prev = None
    shell = '/bin/bash'
    flags = ['--noprofile', '--norc', '-e']
    cprint = y.xprint_white

    for line_no, l in enumerate(data.split('\n')):
        p = l.find('##')

        if p > 5:
            l = l[:p]

        ls = l.strip()

        if not ls:
            continue

        if l[0] == '.':
            if l.startswith('.SHELLFLAGS'):
                a, b = l.split('=')
                flags = [x.strip() for x in b.strip().split(' ')]

            continue

        if ls.startswith('SHELL'):
            shell = ls[6:]

            continue

        if ls.startswith('#'):
            continue

        if l[0] != '\t':
            if prev:
                lst.append(prev)

            prev = new_cmd()

            def iter_deps(ll):
                for l in ll.strip().split(' '):
                    l = l.strip()

                    if l:
                        yield l

            a, b = ls.split(':')

            prev['deps1'] = list(iter_deps(a))
            prev['deps2'] = list(iter_deps(b))
        else:
            prev['cmd'].append(l[1:].rstrip())

    if prev:
        lst.append(prev)

    by_dep = {}

    for x in lst:
        for d in x['deps1']:
            by_dep[d] = x

    done = set()
    do_compile = subprocess.check_output

    if shell_out:
        def do_compile_1(*args, **kwargs):
            shell_out.append(y.deep_copy({'args': args, 'kwargs': kwargs}))

            return ''

        do_compile = do_compile_1

    def run_cmd(c):
        if c in done:
            return y.xprint_blue('already done ' + c)

        if shell_out:
            pass
        elif os.path.exists(c):
            done.add(c)
            return y.xprint_blue('already made it ' + c)

        n = by_dep[c]

        for d in n['deps2']:
            run_cmd(d)


        y.xprint_white('-------------------------------------------------------------------------------')
        my_name = ', '.join(n['deps1'])

        if n.get('cmd'):
            y.xprint_red('will run ' + my_name)

            cmd = '\n'.join(n['cmd']) + '\n'
            input = 'set -e; set -x; ' + cmd
            input = input.replace('$(SHELL)', shell).replace('$(SHELL_FLAGS)', ' '.join(flags[:2]))
            args = ['/usr/bin/env', '-i', '/bin/bash'] + flags

            p = subprocess.Popen(args, stdout=sys.stdout, stderr=sys.stderr, stdin=subprocess.PIPE, shell=False)
            p.communicate(input=input)

            if p.wait():
                raise Exception('shit')
        else:
            y.xprint_blue('symlink target ' + my_name + ' ready')

        for d in n['deps1']:
            done.add(d)

    for t in targets:
        run_cmd(t)
