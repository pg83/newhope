import os
import sys
import signal
import threading
import traceback


def set_profile(g):
    if 'profile=pg' not in ''.join(sys.argv):
        return

    g.trace_function = lambda *args: None
    
    def trace(*args):
        g.trace_function(*args)

    sys.settrace(trace)
    threading.settrace(trace)


def set_sigint(g):
    g.sigint_handler = lambda *args: os._exit(8)

    def sig_handler(*args):
        g.sigint_handler(*args)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGPIPE, signal.SIG_IGN)


def set_abort(g):
    g.abort_function = os.abort
    g.abort_handler = traceback.print_exc

    def new_abort():
        try:
            g.abort_handler()
        finally:
            g.abort_function()

    os.abort = new_abort


def set_env(g):
    sys.argv[0] = g.script_path
    sys.dont_write_bytecode = True
    os.environ['PATH'] = '/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin'
    set_sigint(g)
    set_abort(g)
    set_profile(g)
    

def preprocess_data(data):
    p1 = data.find('/*')
    p2 = data.find('*/')

    if p1 > 0 and p2 > 0:
        d1 = data[:p1]
        d2 = data[p2 + 2:]

        return preprocess_data(d1 + ' ' * (p2 + 2 - p1) + d2)

    return data


def fix_print(data):
    def iter_lines():
        for l in data.split('\n'):
            ll = l.strip()

            if '>>' in ll:
                yield l
            elif ll.startswith('print '):
                l = l.replace('print ', 'print(') + ', file=y.stderr)'

                yield l
            else:
                yield l

    return '\n'.join(iter_lines())


def bad_name(x):
    if '~' in x:
        return True

    if '#' in x:
        return True
   
    if x[0] == '.':
        return True

    return False


def load_folders(folders, exts, where):
    replace = {
        'upm': 'ya',
        'plugins': 'pl',
        'plugins/lib': 'data',
        'scripts': 'sc',
        'util': 'ut',
    }

    yield {'name': os.path.basename(where), 'path': where, 'data': open(where).read()}

    for f in folders:
        fp = os.path.join(os.path.dirname(where), f)
      
        for x in os.listdir(fp):
            if bad_name(x):
                continue
            
            parts = x.split('.')
            name = os.path.join(replace[f], x)
            path = os.path.join(fp, x)

            if not os.path.isfile(path):
                continue
            
            with open(path) as fff:
                data = preprocess_data(fff.read())

                if parts[-1] == 'py':
                    data = fix_print(data)

            yield {'name': name, 'path': path, 'data': data}


def load_system(where):
    return list(load_folders(['plugins', 'plugins/lib', 'scripts', 'upm', 'util'], ['py', ''], where))


def thr_func(g):
    try:
        g.file_data = g.file_data or load_system(g.script_path)
        g.by_name = dict((x['name'], x) for x in g.file_data)
        
        ctx = {'_globals': g}
        exec(compile((g.by_name['ut/stage0.py']['data'] + '\nrun_stage0(_globals)\n'), 'ut/stage0.py', 'exec'), ctx)
        ctx.clear()
    except Exception:
        try:
            sys.stderr.write('can not initialize runtime\n')
        finally:
            os.abort()


def main(g):
    set_env(g)
    t = threading.Thread(target=lambda: thr_func(g))
    t.start()
    t.join()
