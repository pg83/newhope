import os
import sys
import subprocess
import random


from upm_iface import y
from upm_bad import BAD_SUBSTRINGS
from upm_colors import RED, GREEN, RESET, YELLOW, WHITE, BLUE


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
    shell = '/bin/sh'
    flags = ['--noprofile', '--norc', '-e']

    for l in data.split('\n'):
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
            return y.xprint(BLUE + 'already done ' + c + RESET)

        if shell_out:
            pass
        elif os.path.exists(c):
            done.add(c)

            return y.xprint(BLUE + 'already done ' + c + RESET)

        cleanups = []

        try:
            for c in run_cmd_1(c):
                cleanups.append(c)
        except Exception:
            for c in cleanups:
                c()

            raise

    def run_cmd_1(c):
        errors = []
        n = by_dep[c]

        def cleanup():
            for d in n['deps1']:
                if d[0] == '/':
                    errors.append('will remove trash ' + d)

                    try:
                        os.unlink(d)
                    except Exception as e:
                        errors.append(str(e))

        yield cleanup

        for d in n['deps1']:
            done.add(d)

        for d in n['deps2']:
            run_cmd(d)

        white_line = WHITE + '--------------------------------------------------------------------------------------------' + RESET

        def iter_lines(errors):
            yield white_line

            if n['cmd']:
                cmd = '\n'.join(n['cmd']) + '\n'

                yield RED + 'run ' + c + ':' + RESET
                yield YELLOW + ' command:' + RESET

                for l in cmd.strip().split('\n'):
                    l = l.rstrip()

                    if l:
                        yield '  ' + YELLOW + l + RESET

                yield ''

                all_res = []

                try:
                    args = ['/usr/bin/env', '-i', shell] + flags
                    input = BASH_RUNTIME + '\n' + cmd
                    input = input.replace('$(SHELL)', shell).replace('$(SHELL_FLAGS)', ' '.join(flags[:2]))

                    p = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
                    res, _ = p.communicate(input=input)

                    if res:
                        all_res.append(str(res))

                    check_data = ''.join(all_res)

                    for t in BAD_SUBSTRINGS:
                        if t in check_data:
                            raise Exception("error detected: %s" % t)
                except subprocess.CalledProcessError as err:
                    all_res.append(err.output)
                    errors.append('can not build ' + c)
                except Exception as err:
                    errors.append(str(err))

                if errors:
                    color = RED
                else:
                    color = GREEN

                yield color + ' log:' + RESET

                for l in ('\n'.join(all_res)).strip().split('\n'):
                    l = l.rstrip()

                    if l:
                        l = l.decode('utf-8')

                        if 'last log:' in l:
                            color = BLUE

                            yield ''

                            l = ' ' + color + l.strip() + RESET

                            yield l
                        else:
                            if RED in l:
                                errors.append(l)
                            else:
                                yield '  ' + color + l + RESET

                if errors:
                    yield white_line
            else:
                yield BLUE + 'done fake ' + c + RESET

        y.xprint('\n'.join(iter_lines(errors)))

        if errors:
            data = ', '.join(errors)

            raise Exception('%s' % data)

    for t in targets:
        run_cmd(t)
