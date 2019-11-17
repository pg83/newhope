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


def parse_line(l):
    if l.startswith('source fetch '):
        return l.split('"')[1]

    return False


def subst_some_values(v):
    if 'code' in v and '{' in v['code']:
        v = y.deep_copy(v)
        
        for x in ('version', 'name', 'num'):
            if x in v:
                v['code'] = v['code'].replace('{' + x + '}', v[x])

    return v

    
def ygenerator(tier=None, include=[], exclude=[], version=1):
    func_channel = y.write_channel('orig functions', 'yg')

    def functor(func):
        assert tier is not None

        base_name = func.__name__[:-1]
        new_f = lambda: subst_some_values(func())

        descr = {
            'gen': 'human',
            'base': base_name,
            'kind': new_f()['meta']['kind'],
            'code': new_f,
            'include': include,
            'exclude': exclude,
            'version': 1,
        }

        func_channel({'func': descr})

        return func

    return functor
