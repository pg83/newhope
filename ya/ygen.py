def subst_some_values(v):
    def gen_some_subst(k, v):
        yield k, v
        yield '_' + k + '_', v.replace('.', '_').replace('-', '_')

    if 'code' in v and '{' in v['code']:
        v = y.dc(v)

        for x in ('version', 'name', 'num'):
            if x in v:
                for p1, p2 in gen_some_subst(x, v[x]): 
                    v['code'] = v['code'].replace('{' + p1 + '}', p2)

    return v


def exec_plugin_code(iface):
    yield y.EOP(y.ACCEPT('mf:plugin'), y.PROVIDES('mf:original'))

    for data in iface.iter_data():
        code = data.data

        if not code:
            yield y.FIN()

            return

        name = code['name']
        name = name.replace('/', '.')

        if name.endswith('.py'):
            name = name[:-3]

        mod = __yexec__(code['data'], module_name=name)

        try:
            for x in mod.event:
                yield x
        except AttributeError:
            pass

    yield y.EOP()


def ygenerator(where=None):
    def functor(func):
        base_name = func.__name__[:-1]
        new_f = y.singleton(y.compose_simple(func, y.dc, subst_some_values))

        descr = {
            'gen': 'human',
            'base': base_name.replace('_', '-'),
            'kind': new_f()['meta']['kind'],
            'code': new_f,
        }

        assert 'codec' not in new_f()

        ev = y.ELEM({'func': descr})

        if where is not None:
            where.append(ev)
        else:
            fg = func.__globals__
            fg['event'] = fg.get('event', []) + [ev]

        return func

    return functor
