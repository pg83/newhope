import inspect

from .db import restore_node


def outer_locals(depth=0):
    return inspect.getouterframes(inspect.currentframe())[depth + 1][0].f_locals


def run_xpath(val, path, log=[]):
    funcs = [lambda x: x, int, float]

    def f1(cur, p):
        try:
            return cur()
        except Exception as e:
            log.append((cur, p, e, '()'))

        return f2(cur, p)

    def f2(cur, p):
        for f in funcs:
            try:
                return cur(f(p))
            except Exception as e:
                log.append((cur, p, e, '(...)', f))

        return f3(cur, p)

    def f3(cur, p):
        for f in funcs:
            try:
                return cur[f(p)]
            except Exception as e:
                log.append((cur, p, e, '[...]', f))

        return f4(cur, p)

    def f4(cur, p):
        try:
            return eval('cur' + p)
        except Exception as e:
            log.append((cur, p, e, cur + p))

            raise e

    x = val

    for p in path.split('/'):
        def f(x):
            for t in ('x()', 'restore_node(x)'):
                try:
                    return eval(t)
                except:
                    log.append((run_xpath, x, p, t, 'warn'))

            return x

        x = f(f2(f(x), p))

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

        for i in range(1, 5):
            ol = outer_locals(i)

            if name in ol:
                return run_xpath_simple(ol[name], path)

    raise Exception('shit happen')
