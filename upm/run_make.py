import itertools


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

                if y.os.path.isfile(path):
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
                y.xprint_r(ls, line_no, e)

                raise

            prev['deps1'] = list(iter_deps(a))
            prev['deps2'] = list(iter_deps(b))
        else:
            prev['cmd'].append(l[1:].rstrip())

    if prev:
        lst.append(prev)
        
    return lst


def cheet(lst):
    @y.singleton
    def placeholder():
        bsp = lst[0]['deps1'][0]
            
        def build_scripts_path():
            return bsp

        def build_scripts_dir():
            return y.os.path.dirname(bsp)

        l = locals()
        
        @y.lookup
        def look(name):
            return l[name]

    try:
        y.build_scripts_dir()
    except AttributeError:
        placeholder()
        y.build_scripts_dir()


def run_makefile(data, shell_vars, shell_out, targets, threads, parsed, pre_run=[], bypass_streams=False):
    lst = data

    if not parsed:
        lst = parse_makefile(lst)

    cheet(lst)

    if pre_run:
        run_seq_build(lst, shell_vars, False, pre_run)
    
    if threads > 1:
        return y.run_parallel_build(lst, shell_vars, targets, threads, bypass_streams)

    return run_seq_build(lst, shell_vars, shell_out, targets)


def build_run_sh(n):
    def iter_run_sh():
        yield '{r}running {w}[cname]'
        yield '{y} run.sh:'

        for l in n['cmd']:
            yield '  ' + l

    return '\n'.join(iter_run_sh())


def run_seq_build(lst, shell_vars, shell_out, targets):
    build_results = y.build_results_channel()    
    sp = y.subprocess
    by_dep = {}

    for x in lst:
        for d in x['deps1']:
            by_dep[d] = x

    done = set()
    do_compile = sp.Popen

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
        elif y.os.path.exists(c):
            done.add(c)

            return

        n = by_dep[c]

        for d in n['deps2']:
            run_cmd(d)

        my_name = ', '.join(n['deps1'])

        if n.get('cmd'):
            shell = find_file(n['cmd'], 'dash') or '/bin/sh'
            env = dict(y.fix_shell_vars(shell_vars))

            def iter_cmd():
                yield 'set -e'
                yield 'set +x'
                
                for k in sorted(env, key=lambda x: -len(x)):
                    yield 'export {k}={v}'.format(k=k, v=env[k])
                    
                yield 'export PATH="{runtime}:$PATH"'.format(runtime=y.build_scripts_dir())
                yield 'mainfun() {'
                
                for l in n['cmd']:
                    yield l
                    
                yield '}'
                yield 'mainfun ' + ' '.join(itertools.chain(n['deps1'], n['deps2']))
                
            input = '\n'.join(iter_cmd()) + '\n'
            input = input.replace('$(SHELL)', '$YSHELL')

            p = do_compile([shell, '-s'], stdout=sp.PIPE, stderr=sp.STDOUT, stdin=sp.PIPE, shell=False, env=env)
            res, _ = p.communicate(input=input.encode('utf-8'))
            fail = p.wait()

            if not res.strip():
                res = build_run_sh(n)
            
            build_results({
                'text': res,
                'command': input,
                'target': my_name,
            })

            if fail:
                build_results({
                    'message': 'target {g}' + my_name + '{} failed, with retcode ' + str(fail),
                    'retcode': fail,
                    'target': my_name,
                    'status': 'faulure'
                })
                
                raise y.StopNow()
            else:
                build_results({
                    'message': 'target {g}' + my_name + '{} complete',
                    'target': my_name,
                })
        else:
            build_results({
                'message': 'target {g}' + my_name + '{} complete',
                'target': my_name,
            })

        for d in n['deps1']:
            done.add(d)

    try:
        for t in targets:
            run_cmd(t)
            
        build_results({'message': 'all ok', 'status': 'ok'})
    except y.StopNow:
        build_results({'message': 'build not finished', 'status': 'failure'})
