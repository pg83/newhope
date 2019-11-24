def subst_some_values(v):
    def gen_some_subst(k, v):
        yield k, v
        yield '_' + k + '_', v.replace('.', '_').replace('-', '_')
        
    if 'code' in v and '{' in v['code']:
        v = y.deep_copy(v)
        
        for x in ('version', 'name', 'num'):
            if x in v:
                for p1, p2 in gen_some_subst(x, v[x]): 
                    v['code'] = v['code'].replace('{' + p1 + '}', p2)

    return v


def ygenerator(tier=None, include=[], exclude=[], version=1):
    func_channel = y.GEN_DATA_LOOP.write_channel('orig functions', 'yg')

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
