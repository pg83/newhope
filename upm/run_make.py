import os
import sys
import subprocess
import random
import traceback


def new_cmd():
    return {
        'cmd': [],
    }


def find_file(cmd, f):
    for l in cmd:
        if 'export PATH=' in l:
            l = l[l.find('/'):]

            for d in l.split(':'):
                path = d + '/' + f

                if os.path.isfile(path):
                    return path


def parse_makefile(data):
    lst = []
    prev = None
    cprint = y.xprint_white

    for line_no, l in enumerate(data.split('\n')):
        p = l.find('##')

        if p > 5:
            l = l[:p]

        ls = l.strip()

        if not ls:
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

            try:
                a, b = ls.split(':')
            except Exception as e:
                print ls, line_no, e

                raise

            prev['deps1'] = list(iter_deps(a))
            prev['deps2'] = list(iter_deps(b))
        else:
            prev['cmd'].append(l[1:].rstrip())

    if prev:
        lst.append(prev)
        
    return lst


def run_makefile(data, shell_vars, shell_out, targets, threads, parsed, verbose):
    lst = data

    if not parsed:
        lst = parse_makefile(lst)

    if threads > 1:
        for i, val in enumerate(lst):
            val['n'] = i

        return y.run_parallel_build(lst, shell_vars, targets, threads, verbose)

    by_dep = {}

    for x in lst:
        for d in x['deps1']:
            by_dep[d] = x

    done = set()
    do_compile = subprocess.check_output

    if shell_out:
        def do_compile_1(*args, **kwargs):
            class A(object):
                def __init__(self):
                    pass

                def communicate(self, input=None):
                    shell_out.append(y.deep_copy({'args': args, 'kwargs': kwargs, 'input': input}))
            
                    return '', ''

                def wait(self):
                    return 0

            return A()

        do_compile = do_compile_1

    def run_cmd(c):
        if c in done:
            return

        if shell_out:
            pass
        elif os.path.exists(c):
            done.add(c)

            return

        n = by_dep[c]

        for d in n['deps2']:
            run_cmd(d)

        def prn_delim():
            y.xprint_white('-------------------------------------------------------------------------------')

        prn_delim()

        my_name = ', '.join(n['deps1'])

        if n.get('cmd'):
            shell = find_file(n['cmd'], 'dash') or '/bin/sh'
            cmd = '\n'.join(n['cmd']) + '\n'
            input = 'set -e; set +x; ' + cmd
            input = input.replace('$(SHELL)', '$YSHELL')
            args = ['/usr/bin/env', '-i', shell, '--noprofile', '--norc', '-s']
            p = do_compile(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, shell=False)
            res, _ = p.communicate(input=input)
            fail = p.wait()

            def it():
                for l in res.strip().split('\n'):
                    if l and l[0] == '+':
                        continue

                    yield l

                if fail:
                    yield y.get_color('red')

                    for l in traceback.format_stack():
                        if 'File' in l:
                            yield l[:-1]
                        else:
                            yield '  ' + l[:-1]

                    yield y.get_color('rst')

            print >>sys.stderr, ('\n'.join(it())).strip()

            if fail:
                prn_delim()
                raise StopIteration()
        else:
            y.xprint_blue('symlink target ' + my_name + ' ready')

        for d in n['deps1']:
            done.add(d)

    try:
        for t in targets:
            run_cmd(t)
    except StopIteration:
        raise Exception('can not build desired targets, some node broken')

