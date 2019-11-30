import os
import sys
import threading
import traceback


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
                l = l.replace('print ', 'print(') + ')'

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
        'scripts': 'sc',
        'util': 'ut',
    }

    yield {'name': 'cli', 'path': 'cli', 'data': open(where).read()}

    for f in folders:
        fp = os.path.join(os.path.dirname(where), f)
      
        for x in os.listdir(fp):
            if bad_name(x):
                continue

            parts = x.split('.')
            
            if parts[-1] in exts or len(parts) == 1:
                pass
            else:
                continue

            name = os.path.join(replace[f], x)
            path = os.path.join(fp, x)
         
            with open(path) as fff:
                data = preprocess_data(fff.read())

                if parts[-1] == 'py':
                    data = fix_print(data)

            yield {'name': name, 'path': path, 'data': data}


def thr_func(args, data, where, **kwrgs):
    try:
        data = data or list(load_folders(['plugins', 'scripts', 'upm', 'util'], ['py', ''], where))
        by_name = dict((x['name'], x) for x in data)
        stage0 = by_name['ut/stage0.py']
      
        args.update({'data': data, 'by_name': by_name})
   
        ctx = {'args': args}
        exec(compile((stage0['data'] + '\nrun_stage0(args, **args)\n'), 'ut/stage0.py', 'exec'), ctx)
        ctx.clear()
    except Exception:
        try:
            sys.stderr.write('can not initialize runtime\n')
            traceback.print_exc()
        finally:
            os.abort()


def main(args, data, where, **kwargs):
    t = threading.Thread(target=lambda: thr_func(args, **args))
    t.start()
    t.join()
