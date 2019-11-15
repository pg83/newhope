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


def parse_line(l):
    if l.startswith('source fetch '):
        return l.split('"')[1]

    return False


def ygenerator(tier=None, kind=[], include=[], exclude=[], version=1):
    func_channel = y.write_channel('orig functions', 'yg')
    gen_channel = y.write_channel('new functions generator', 'yg')
    kind = y.deep_copy(kind)
        
    def functor(func):
        assert tier is not None
        
        orig_func = func
        base_name = orig_func.__name__[:-1]

        if base_name.startswith('lib'):
            kind.append('library')
        else:
            kind.append('tool')

        if 'box' in kind:
            kind.append('tool')

        func_channel({'func': func, 'kind': kind, 'original': True, 'mod': func.__module__})
        
        def generator(deps_types, num, fname, codec):
            def func(info):
                res = y.deep_copy(orig_func())

                res['codec'] = codec
                res['name'] = fname
                res['deps'] = res.pop('extra_deps', []) + [f(info) for f in deps_types()]

                if 'meta' not in res:
                    res['meta'] = {}

                if 'kind' not in res['meta']:
                    res['meta']['kind'] = kind

                if version == 1:
                    return y.to_v2(res, info)

                return res
            
            func.__name__ = fname

            return func

        data = {
            'tier': tier,
            'kind': kind,
            'name': base_name,
            'include': include,
            'exclude': exclude,
            'generator': generator,
        }

        gen_channel(data)

        return func

    return functor
