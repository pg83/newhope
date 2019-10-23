import inspect

from upm_iface import y


def apply_base(funcs, log):
    for f in funcs:
        try:
            yield f()
        except Exception as e:
            log.append((f, e))


def apply_any_0(funcs, log):
    for r in apply_base(funcs, log):
        return r

    raise Exception('shit happen')


def fv(f, v):
    return lambda: f(v)


def iter_lst(v, lst):
    for f in lst:
        yield fv(f, v)


def apply_any(v, lst, log):
    return apply_any_0(iter_lst(v, lst), log)


def apply_all(v, lst, log):
    return list(apply_base(iter_lst(v, lst), log))


def run_xpath(val, path, log=[]):
    def try_call(x):
        return apply_any(x, (y.restore_node, lambda x: x(), lambda x: x), log)

    def param_lst(p):
        return apply_all(p, (str, int, float), log)

    def f1(a):
        x, p = a

        return x[p]

    def f2(a):
        x, p = a

        return x(p)

    def iter_funcs(pp, x):
        for f in (f1, f2):
            for p in pp:
                yield fv(f, (x, p))

        yield lambda: eval('x' + pp[0], {'x': x, 'pp': pp})
        yield lambda: eval('x.' + pp[0], {'x': x, 'pp': pp})

    x = val

    for p in path.split('/'):
        log.append(('before', x, p))
        x = try_call(apply_any_0(iter_funcs(param_lst(p), try_call(x)), log))
        log.append(('after', x, p))

    return x


def run_xpath_simple(val, path):
    log = []

    try:
        return run_xpath(val, path, log=log)
    except Exception as e:
        log.append(('at end', str(e)))

        def iter_recs():
            for l in log:
                yield '[' + ', '.join([str(x) for x in l]) + ']'

        raise Exception('shit happen %s' % '\n'.join(iter_recs()))


def xp(path):
    if path.startswith('//'):
        return run_xpath_simple(globals(), path[2:])

    if path.startswith('/'):
        name, path = path[1:].split('/', 1)
        frame = inspect.currentframe()

        while True:
            frame = frame.f_back
            ol = frame.f_locals

            if name in ol:
                return run_xpath_simple(ol[name], path)

    raise Exception('shit happen')
