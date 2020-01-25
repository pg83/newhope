@y.singleton
def main_entry_points():
    return {}


def funcs_by_func(f):
    return [k for k in main_entry_points() if f(k)]


def funcs_by_prefix(prefix):
    return funcs_by_func(lambda k: k.startswith(prefix))


def funcs_by_suffix(suffix):
    return funcs_by_func(lambda k: k.endswith(suffix))


def get_entry_point(name):
    if name.startswith('cli_'):
        name = name[4:]

    try:
        return main_entry_points()[name][1]
    except KeyError:
        l = funcs_by_suffix('_' + name)

        if len(l) == 1:
            return main_entry_points()[l[0]][1]

    raise KeyError(name)


def register_entry_point(f):
    vis, func = f
    name = func.__name__

    if name.startswith('cli_'):
        name = name[4:]

    assert '__' not in name

    mep = main_entry_points()

    assert name not in mep

    mep[name] = f

    if '_' in name:
        def it_help(prefix):
            yield '{bg}options:{}'

            for k in funcs_by_prefix(prefix + '_'):
                yield '    {bb}' + k.replace('_', ' ') + '{}'

        async def func(mn, args):
            if args:
                nn = mn + '_' + args[0]

                if nn in mep:
                    return await mep[nn][1](args[1:])
            else:
                print('\n'.join(it_help(mn)), file=y.stderr)

        def register(n, s):
            if not s:
                return

            if n:
                n = n + '_' + s.pop()
            else:
                n = s.pop()

            if n in mep:
                pass
            else:
                ff = lambda args: func(n, args)
                ff.__name__ = n

                mep[n] = ('d', ff)

            register(n, s)

        register('', list(reversed(name.split('_'))))


def main_entry_point(f):
    register_entry_point(('m', f))

    return f


def verbose_entry_point(f):
    register_entry_point(('v', f))

    return f


@y.defer_constructor
def init_1():
    if y.config.get('psy'):
        y.run_at_exit(y.print_stats)


async def run_main(args):
    with y.without_gc(True):
        return await y.get_entry_point(args[1])(args[2:])
