import os
import sys
import subprocess

from .colors import RED, GREEN, RESET, YELLOW, WHITE, BLUE
from .subst import subst_kv_base


def new_cmd():
    return {
        'cmd': [],
    }


def xprint(*args):
    print >>sys.stderr, ' '.join(args)


def run_makefile(data, *targets):
    lst = []
    prev = None
    shell = '/bin/bash'
    flags = ['-c']

    for l in data.split('\n'):
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

    def run_cmd(c):
        errors = []

        if c in done:
            return xprint(BLUE + 'already done ' + c + RESET)

        if os.path.exists(c):
            done.add(c)
            return xprint(BLUE + 'already done ' + c + RESET)

        n = by_dep[c]

        def cleanup():
            for d in n['deps1']:
                if d[0] == '/':
                    errors.append('will remove trash ' + d)

                    try:
                        os.unlink(d)
                    except Exception as e:
                        errors.append(str(e))

        for d in n['deps1']:
            done.add(d)

        for d in n['deps2']:
            run_cmd(d)

        white_line = WHITE + '--------------------------------------------------------------------------------------------' + RESET

        def iter_lines(errors):
            yield white_line

            if n['cmd']:
                cmd = 'set -e; set -x; ' + '\n'.join(n['cmd']) + '\n'

                yield RED + 'run ' + c + ':' + RESET
                yield YELLOW + ' command:' + RESET

                for l in cmd.strip().split('\n'):
                    l = l.rstrip()

                    if l:
                        yield '  ' + YELLOW + l + RESET

                yield ''

                all_res = []

                try:
                    res = subprocess.check_output([shell] + flags + [cmd], stderr=subprocess.STDOUT, shell=False)
                    all_res.append(res)

                    if 'C compiler cannot create executables' in res:
                        raise Exception('C compiler cannot create executables')
                except subprocess.CalledProcessError as err:
                    all_res.append(err.output)
                    errors.append('can not build ' + c)
                except Exception as err:
                    errors.append(str(err))

                yield GREEN + ' log:' + RESET

                for l in ('\n'.join(all_res)).strip().split('\n'):
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

        xprint('\n'.join(iter_lines(errors)))

        if errors:
            cleanup()

            raise Exception('%s' % (', '.join(errors)))

    for t in targets:
        run_cmd(t)
