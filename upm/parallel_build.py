import os
import sys
import Queue
import signal
import threading
import subprocess as sp
import traceback
import functools
import itertools


def is_in(lst, s):
    for l in lst:
        if l not in s:
            return False

    return True


def cmd_name(cmd):
    assert len(cmd['deps1']) == 1
    
    v = cmd['deps1'][0]
    v = v[v.find('/v5') + 1:]

    return v


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

    return [lst[x] for x in sorted(frozenset(iter()))]


def get_el(qu):
    while True:
        try:
            return qu.get(True, 0.1)
        except Queue.Empty:
            pass


def get_white_line():
    return y.xxformat('---------------------------------------------------------------------', init='white')


@y.defer_wrapper
def run_parallel_build(reg_defer, lst, targets, thrs):
    lst = get_only_our_targets(lst, targets)
    white_line = get_white_line()

    def stop_iter(*args, **kwargs):
        raise StopIteration()

    methods = {
        'get_el': get_el,
        'popen': sp.Popen,
        'get_reason': lambda: [],
    }

    for i, l in enumerate(lst):
        l['n'] = i

    complete = set()
    unready = set([l['n'] for l in lst])
    q = Queue.Queue()
    w = Queue.Queue()
    running = set()

    def kill_all_running(*args):
        os.system('pkill -KILL -g {pgid}'.format(pgid=os.getpgid(os.getpid())))

    def find_complete():
        for n in list(unready):
            l = lst[n]

            if is_in(l['deps2'], complete):
                unready.remove(n)

                yield l

    def gen_working_func(l):
        def set_result(a):
            raise SetResult(a)

        def process():
            c = l.get('cmd')
            cn = cmd_name(l)
            output = l['deps1'][0]

            if not c:
                return lambda: y.xxprint('symlink {g:task} complete', init='b', task=cn)

            if os.path.exists(output):
                return lambda: y.xxprint('target {g:task} complete', init='b', task=cn)

            def find_tool(tool):
                def iter_deps():
                    for d in l['deps2']:
                        yield os.path.join(os.path.dirname(d), 'bin')

                return y.find_tool_uncached(tool, iter_deps())

            def iter_eof():
                if 'EOF' in c[1] or 'EOF' in c[2]:
                    yield 'EOF'

                yield ''

            shell = find_tool('dash') or find_tool('bash') or find_tool('sh')
            input = '\n'.join(itertools.chain(c, iter_eof()))
            cmd = [shell, '-s']
            env = {'OUTER_SHELL': shell}
            out = []
            retcode = None

            with y.defer_context() as defer:
                args = {
                    'stdout': sp.PIPE, 
                    'stderr': sp.STDOUT,
                    'stdin': sp.PIPE,
                    'shell': False, 
                    'env': env, 
                    'close_fds': True, 
                    'cwd': '/', 
                    'bufsize': 1,
                }

                p = methods['popen'](cmd, **args)
                running.add(p)
                defer(lambda: running.remove(p))

                try:
                    res, _ = p.communicate(input=input)
                    out.append(res)
                    retcode = p.wait()
                except sp.CalledProcessError as e:
                    out.append(e.output)
                    retcode = e.returncode
                except Exception as e:
                    out.append(y.colorize(traceback.format_exc(e), 'r'))
                    retcode = -1

            def func():
                data = '\n'.join(o.strip() for o in out)

                if data:
                    data = white_line + '\n' + data
                    sys.stderr.write(y.xxformat(data, cname=cn))

                if retcode and retcode != -9:
                    oldfun = methods['get_reason']

                    def new_fun():
                        arr = oldfun()
                        arr.append('{y}' + cn + '{} finished with return code: ' + str(retcode))

                        return arr
                    
                    methods['get_reason'] = new_fun

                    raise StopIteration()

            return func

        def wrapper():
            try:
                set_result(process())
            except SetResult as e:
                def func():
                    e.func()

                    return l

                w.put(func)

        return wrapper

    def func():
        while True:
            try:
                methods['get_el'](q)()
            except StopIteration:
                return
            except Exception as e:
                exc = sys.exc_info()

                def func():
                    raise exc[0], exc[1], exc[2]

                w.put(func)

    threads = [threading.Thread(target=func) for i in range(0, thrs)]

    def wait_all_threads():
        for t in threads:
            q.put(stop_iter)

        for t in threads:
            t.join()

    def prepare_finish():
        for k in methods.keys():
            if k not in ['get_reason']:
                methods[k] = stop_iter

    def restore_sigint():
        signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    def print_status():
        def iter():
            yield white_line

            if unready:
                yield y.xxformat('build not finished - ' + ', '.join(methods['get_reason']()), init='r')
            else:
                yield y.xxformat('all ok', init='g')

        return '\n'.join(iter())

    def read_queue():
        while True:
            try:
                w.get_nowait()()
            except StopIteration:
                pass
            except Queue.Empty:
                return
            except Exception as e:
                y.xprint_red(traceback.format_exc(e))

    reg_defer(lambda: white_line)
    reg_defer(prepare_finish)
    reg_defer(kill_all_running)
    reg_defer(wait_all_threads)
    reg_defer(restore_sigint)
    reg_defer(print_status)
    
    msg = y.get_color('') + '\n'

    def sigint(*args):
        def func():
            methods['get_reason'] = lambda: ['SIGINT happens']

            raise StopIteration()

        sys.stderr.write(msg)
        w.put(func)

    signal.signal(signal.SIGINT, sigint)

    for t in threads:
        t.start()

    while unready:
        for l in find_complete():
            q.put(gen_working_func(l))

        try:
            l = methods['get_el'](w)()
        except StopIteration:
            break

        for d in l['deps1']:
            complete.add(d)
