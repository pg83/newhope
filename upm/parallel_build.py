import os
import sys
import Queue
import threading
import subprocess as sp


def is_in(lst, s):
    for l in lst:
        if l not in s:
            return False

    return True


def cmd_name(cmd):
    assert len(cmd['deps1']) == 1
    return str(cmd['n']) + ":" + cmd['deps1'][0]


class SetResult(Exception):
    def __init__(self, func):
        self.func = func


def get_only_our_targets(lst, targets):
    by_link = {}

    for l in lst:
        for d in l['deps1']:
            by_link[d] = l['n']

    v = set()

    def visit(n):
        if n in v:
            return

        yield n

        v.add(n)

        for l in [by_link[d] for d in lst[n]['deps2']]:
            for x in visit(l):
                yield x

    def iter():
        for t in targets:
            for x in visit(by_link[t]):
                yield x

    nn = frozenset(iter())

    return [lst[x] for x in sorted(nn)]


def run_parallel_build(lst, targets, thrs):
    lst = get_only_our_targets(lst, targets)

    for i, l in enumerate(lst):
        l['n'] = i

    ll = threading.Lock()
    complete = set()
    unready = set([l['n'] for l in lst])

    def find_complete():
        for n in list(unready):
            l = lst[n]

            if is_in(l['deps2'], complete):
                unready.remove(n)

                yield l

    q = Queue.Queue()
    w = Queue.Queue()

    def gen_working_func(l):
        def set_result(a):
            raise SetResult(a)

        def process():
            c = l.get('cmd')
            cn = cmd_name(l)
            output = l['deps1'][0]

            if not c:
                def func():
                    with ll:
                        y.xprint_blue('symlink task complete', cn)

                set_result(func)

            if os.path.exists(output):
                def func():
                    with ll:
                        y.xprint_blue('task complete', cn)

                set_result(func)

            data = 'set -e; set +x; ' + '\n'.join(c) + '\n'
            data = data.replace('$(SHELL)', '$YSHELL')
            p = sp.Popen(['/bin/bash', '--noprofile', '--norc', '-s'], stdout=sp.PIPE, stderr=sp.STDOUT, stdin=sp.PIPE, shell=False, env={})
            res, _ = p.communicate(input=data)
            err = p.wait()

            def func():
                data = y.colorize('---------------------------------------------------------------------', 'white') + '\n' + res

                with ll:
                    sys.stderr.write(data.strip() + '\n')

                if err:
                    raise Exception(str(c))

            set_result(func)

        def wrapper():
            try:
                process()
            except SetResult as e:
                def func():
                    e.func()

                    return l

                w.put(func)

        return wrapper

    def func():
        while True:
            try:
                q.get()()
            except StopIteration:
                return
            except Exception as e:
                def func():
                    raise e

                w.put(func)

    def iter_thrs():
        for i in range(0, thrs):
            yield threading.Thread(target=func)

    threads = list(iter_thrs())

    for t in threads:
        t.start()

    try:
        while True:
            for l in find_complete():
                q.put(gen_working_func(l))

            l = w.get()()

            for d in l['deps1']:
                complete.add(d)
    finally:
        with ll:
            y.xprint_white('will wait others')

        def func():
            raise StopIteration()

        for t in threads:
            q.put(func)

        for t in threads:
            t.join()
