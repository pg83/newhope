import os
import subprocess

from .colors import RED, GREEN, RESET, YELLOW, WHITE, BLUE
from .subst import subst_kv_base


def new_cmd():
    return {
        'cmd': [],
    }


def run_makefile(data, *targets):
    lst = []
    prev = None
    shell = '/bin/bash'

    for l in data.split('\n'):
        ls = l.strip()

        if not ls:
            continue

        if l[0] == '.':
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

    def run_cmd(c):
        if c in done:
            print BLUE + 'already done ' + c + RESET
            return

        if os.path.exists(c):
            done.add(c)
            print BLUE + 'already done ' + c + RESET
            return

        n = by_dep[c]

        for d in n['deps1']:
            done.add(d)

        for d in n['deps2']:
            run_cmd(d)

        errors = []
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

                try:
                    (res, errr) = (subprocess.check_output([shell, '-xce', cmd], stderr=subprocess.STDOUT, shell=False), None)
                except subprocess.CalledProcessError as err:
                    (res, errr) = (err.output, err)

                    errors.append('can not build ' + c)

                yield GREEN + ' log:' + RESET

                for l in res.strip().split('\n'):
                    l = l.rstrip()

                    if l:
                        l = l.decode('utf-8')

                        if RED in l:
                            errors.append(l)
                        else:
                            yield '  ' + GREEN + l + RESET

                if errors:
                    yield white_line
            else:
                yield BLUE + 'done fake ' + c + RESET

        print '\n'.join(iter_lines(errors))

        if errors:
            raise Exception(', '.join(errors))

    for t in targets:
        run_cmd(t)
