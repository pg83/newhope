def dep_name(dep):
    return y.restore_node_node(dep)['name']


def dep_list(info, iter):
    return [x(info) for x in iter]


@y.read_callback('new plugin', 'plugins')
def exec_plugin_code(code):
    try:
        name = code['name']
    except:
        print code
        raise

    name = name.replace('/', '.')

    if name.endswith('.py'):
        name = name[:-3]

    __yexec__(code['data'], module_name=name)


@y.cached()
def find_build_func(name, num='', split=''):
    if num:
        name = name + str(num)

    if split:
        name = name + '_' + split

    return eval('y.' + name)


def identity(x):
    return x


def parse_line(l):
    if l.startswith('source fetch '):
        return l.split('"')[1]

    return False


def set_name(v, n):
    v = y.deep_copy(v)
    v['name'] = n

    return v


def join_n(p):
    return '\n'.join(p) + '\n'


def better_tov2(x, info, kw):
    if 'deps' not in x:
        x['deps'] = x.pop('extra_deps', []) + eval('y.' + kw['deps'])

    if 'prepare' not in x:
        p = []
        kind = kw['kind']

        if 'tool' in kind:
            p.append('$(ADD_PATH)')

        if 'library' in kind:
            p.append('$(ADD_CFLAGS)')
            p.append('$(ADD_LDFLAGS)')
            p.append('$(ADD_LIBS)')
            p.append('$(ADD_PKG_CONFIG)')
          
        x['prepare'] = join_n(p)

    return y.to_v2(x, info)


def ygenerator(tier=None, kind=[], include=[], exclude=[], version=1):
    func_channel = y.write_channel('orig functions', 'yg')
    tmpl_channel = y.write_channel('new functions templates', 'yg')

    def functor(func):
        assert tier is not None

        func_channel({'func': func, 'kind': kind, 'original': True, 'mod': func.__module__})

        rfn = func.__name__
        fn = rfn[:-1]
        func.__name__ = rfn

        template = """
@y.options({options})
def {name}{num}(info):
    def my_tov2(x):
        return y.better_tov2(x, info, {kw})

    return {tov2}(y.set_name(y.{func_name}(), "{name}{num}"))
"""
        fname = 'y.identity'

        if version == 1:
            fname = 'my_tov2'

        data = {
            'tier': tier,
            'name': fn,
            'kind': kind,
            'include': include,
            'exclude': exclude,
            'template': template,
            'extra_arg': {
                'func_name': func.__name__,
                'tov2': fname,
            }
        }

        if fn.startswith('lib'):
            kind.append('library')

        tmpl_channel(data)

        return func

    return functor
