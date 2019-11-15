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
    sp = y.subprocess
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


def run_makefile(data, shell_vars, shell_out, targets, threads, parsed):
    lst = data

    if not parsed:
        lst = parse_makefile(lst)

    cheet(lst)

    if threads > 1:
        for i, val in enumerate(lst):
            val['n'] = i

        return y.run_parallel_build(lst, shell_vars, targets, threads)

    by_dep = {}

    for x in lst:
        for d in x['deps1']:
            by_dep[d] = x

    done = set()
    do_compile = sp.check_output

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
            p = do_compile(args, stdout=sp.PIPE, stderr=sp.STDOUT, stdin=sp.PIPE, shell=False)
            res, _ = p.communicate(input=input)
            fail = p.wait()

            y.xxprint(res)

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

