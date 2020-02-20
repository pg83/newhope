def gen_some_subst(k, v):
    yield k, v
    yield '_' + k + '_', v.replace('.', '_').replace('-', '_')


def subst_some_values(v, base_name):
    if 'code' in v and '{' in v['code']:
        v = y.dc(v)

        if 'version' not in v:
            s = y.package_versions()

            if base_name in s:
                v['version'] = s[base_name]

        for x in ('version', 'name', 'num'):
            if x in v:
                for p1, p2 in gen_some_subst(x, v[x]):
                    v['code'] = v['code'].replace('{' + p1 + '}', p2)

        assert '{version}' not in v['code']

    return v


plugin_code = {}


def exec_plugin_code(el):
    code = el['el']
    cc = el['cc']
    name = code['name']
    name = name.replace('/', '.')

    if name.endswith('.py'):
        name = name[:-3]

    args = {
        '{arch}': cc['arch'],
        '{os}': cc['os']
    }

    mod_name = y.small_repr(cc) + '.' + name
    y.plugin_code[mod_name] = []
    mod = __yexec__(code['data'], module_name=mod_name, args=args)
    events = y.plugin_code.pop(mod_name)

    yield from events

    if not events:
        y.error('{by}no package in', name, '{}')


def package(func):
    base_name = func.__name__[:-1]
    fix_bn = base_name.replace('_', '-')
    new_f = y.singleton(y.compose_simple(func, y.dc, lambda x: subst_some_values(x, fix_bn)))
    parts = func.__module__.split('.')

    descr = {
        'gen': 'human',
        'base': fix_bn,
        'kind': new_f()['meta']['kind'],
        'code': new_f,
        'cc': y.to_full_target(parts[1])
    }

    y.plugin_code['.'.join(parts[1:])].append(descr)

    return func
