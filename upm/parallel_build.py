import os
import sys
import Queue
import threading
import subprocess as sp
import itertools
import base64
import time


def is_in(lst, s):
    for l in lst:
        if l not in s:
            return False

    return True


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


def remove_d(k):
    if k[0] == '$':
        return k[1:]
                
    return k


def subst_vars(d, shell_vars):
    while '$' in d:
        for k, v in shell_vars.iteritems():
            d = d.replace(k, v)
            
    return d


def fix_shell_vars(shell_vars):
    return [(remove_d(k), v) for k, v in shell_vars.iteritems()]


def run_parallel_build(lst, shell_vars, targets, thrs, bypass_streams):
    t_begin = y.time.time()
    verbose = y.verbose

    for i, l in enumerate(lst):
        l['n'] = i
    
    lst = get_only_our_targets(lst, targets)
    left = len(lst)

    rq, wq = y.make_engine(lst, lambda x: x['deps1'][0], dep_list=lambda x: x['deps2'])

    @y.cached()
    def resolve_path(d):
        return subst_vars(d, shell_vars)

    methods = {
        'get_el': get_el,
        'popen': sp.Popen,
    }

    def get_method_get_el():
        return methods['get_el']
    
    for i, l in enumerate(lst):
        l['n'] = i

    q = Queue.Queue()
    w = Queue.Queue()

    build_results = y.build_results_channel()
    status_bar = y.status_bar()
    terminal_channel = y.terminal_channel()
    console_channel = y.write_channel('yic', 'parallel build')
    
    @y.run_by_timer(0.5)
    def ff():
        def f():
            status_bar({'message': ' '})
            terminal_channel({'command': 'redraw'})

        w.put(f)

    def kill_all_running(*args):
        os.system('pkill -KILL -g {pgid}'.format(pgid=os.getpgid(os.getpid())))

    def find_complete():
        for x in rq():
            yield x

    def gen_working_func(ll):
        def set_result(a):
            raise SetResult(a)

        def process():
            l = ll['x']
            c = l.get('cmd')
            tg = l['deps1'][0]
            output = l['deps1'][0]

            if not c:
                return lambda: build_results({'message': 'target {task} complete'.format(task='{g}' + tg + '{}'), 'target': tg})

            if os.path.exists(resolve_path(output)):
                return lambda: build_results({'message': 'target {task} complete'.format(task='{g}' + tg + '{}'), 'target': tg})

            def iter_deps():
                for d in l['deps2']:
                    yield os.path.join(os.path.dirname(resolve_path(d)), 'bin')

            srch_lst = list(iter_deps())

            def find_tool(tool):
                if tool[0] == '/':
                    return tool

                return y.find_tool_uncached(tool, srch_lst)

            if '$YSHELL' in shell_vars:
                shell = find_tool(shell_vars['$YSHELL'])

                if not shell:
                    raise Exception('can not find ' + shell_vars['$YSHELL'])
            else:
                shell = find_tool('dash') or find_tool('yash') or find_tool('sh') or find_tool('bash')

            input = '\n'.join(c)
            cmd = [shell, '-s']
            env = dict(itertools.chain({'OUTER_SHELL': shell}.iteritems(), fix_shell_vars(shell_vars)))
            out = []
            retcode = None

            def iter_parts():
                if '/-x' in verbose:
                    yield 'set -x'
                else:
                    yield 'set +x'
                    
                if '/-v' in verbose:
                    yield 'set -v'
                else:
                    yield 'set +v'

                yield 'set -e'

                for k in sorted(env.keys(), key=lambda x: -len(x)):
                    yield 'export ' + k + '=' + env[k]

                yield 'export BIGI="' + base64.b64encode(input) + '"'
                yield 'export PATH={runtime}:$PATH'.format(runtime=y.build_scripts_dir())
                yield 'mainfun() {'
                yield input
                yield '}'
                yield 'mainfun ' + ' '.join(itertools.chain(l['deps1'], l['deps2']))

            input = '\n'.join(iter_parts()) + '\n'
            
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

                try:
                    res, _ = p.communicate(input=input)

                    if not res.strip():
                        res = y.build_run_sh(l)
                        
                    out.append(res)
                    retcode = p.wait()
                except sp.CalledProcessError as e:
                    out.append(e.output)
                    retcode = e.returncode
                except Exception:
                    out.append(y.format_tbx())
                    retcode = -1

            def func():
                data = '\n'.join(o.strip() for o in out)

                if data:
                    build_results({
                        'text': data,
                        'target': tg,
                        'command': input,
                    })

                if retcode and retcode != -9:
                    build_results({
                        'message': 'target {g}' + tg + '{} failed, with retcode ' + str(retcode),
                        'status': 'failure',
                        'target': tg,
                        'retcode': retcode,
                    })
                    
                    raise StopIteration()

            return func

        def wrapper():
            try:
                set_result(process())
            except SetResult as e:
                def func():
                    e.func()

                    return ll

                w.put(func)

        return wrapper

    def func():
        while True:
            try:
                get_method_get_el()(q)()
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
            methods[k] = stop_iter

    def print_status():
        if left:
            build_results({'message': 'build not finished', 'status': 'failure'})
            build_results({'key': 'Build', 'value': 'Failed'})
        else:
            build_results({'message': 'all ok', 'status': 'ok'})
            build_results({'key': 'Build', 'value': 'Successful'})
        
    @y.signal_channel.read_callback()
    def on_sig_int(arg):
        if arg['signal'] == 'INT':
            build_results({'message': 'SIGINT happens', 'status': 'failure'})
        
    for t in threads:
        t.start()
        
    with y.defer_context() as reg_defer:
        reg_defer(prepare_finish)
        reg_defer(kill_all_running)
        reg_defer(wait_all_threads)
        reg_defer(print_status)
                
        while left:
            status_bar({'key': 'Left', 'value': str(left)})
            status_bar({'key': 'All', 'value': str(len(lst))})
            status_bar({'key': 'Complete', 'value': str(len(lst) - left)})
            status_bar({'key': 'Wall Clock', 'value': str(y.time.time())})
            status_bar({'key': 'Duration', 'value': str(y.time.time() - t_begin)})
        
            for ll in find_complete():
                q.put(gen_working_func(ll))

            try:
                ll = get_method_get_el()(w)()
            except StopIteration:
                break
            
            if ll:
                wq(ll['i'])
                left -= 1
