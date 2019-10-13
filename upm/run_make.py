import os
import subprocess


def new_cmd():
    return {
        'cmd': [],
    }


def run_makefile(data, *targets):
    lst = []
    prev = None

    for l in data.split('\n'):
        ls = l.strip()

        if not ls:
            continue

        if ls[0] == '.':
            continue

        if ls.startswith('SHELL'):
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
            prev['cmd'].append(ls)

    lst.append(prev)
    by_dep = {}

    for x in lst:
        for d in x['deps1']:
            by_dep[d] = x

    done = set()

    def run_cmd(c):
        if c in done:
            return

        if os.path.exists(c):
            print 'already done ' + c
            done.add(c)
            return

        n = by_dep[c]

        for d in n['deps1']:
            done.add(d)

        for d in n['deps2']:
            run_cmd(d)

        if n['cmd']:
            cmd = '\n'.join(n['cmd']) + '\n'

            print 'run ' + c
            print subprocess.check_output(['/bin/bash', '-xce', cmd], shell=False)
            print 'done ' + c
        else:
            print 'done fake ' + c

    for t in targets:
        run_cmd(t)
