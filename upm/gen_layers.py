@y.singleton
def layers_channel():
    return y.write_channel("new functions", "layers")


def gen_all_texts(only_print_layers=False):
    by_tier = {}
    by_name = {}
    all = []
    channel = layers_channel()

    for j in y.iter_all_user_generators():
        f = y.deep_copy(j)
        f['gen'] = 'lay'
        
        t = f['tier']
        by_name[f['base']] = f

        if t in by_tier:
            by_tier[t].append(f)
        else:
            by_tier[t] = [f]

        all.append(f)

    levels = list(sorted(by_tier.keys()))

    @y.cached()
    def calc_level(n):
        res = by_tier[n]

        if n == levels[0]:
            return res

        return sorted(res + calc_level(n - 1))

    def calc_levels():
        for i in levels:
            yield i, [x['base'] for x in calc_level(i)]

    by_level = dict(calc_levels())

    def iter_layers():
        for i in levels:
            yield i

        yield levels[-1]

    to_build = list(iter_layers())

    def iter():
        for i, l in enumerate(to_build):
            yield i + 1, [{'base': x, 'num': i + 1} for x in by_level[l]]

    descr = dict(iter())    
    all_funcs = []

    @y.cached()
    def deps(l):
        @y.singleton
        def cached_types():
            if l == 0:
                return []

            return y.join_funcs([all_funcs[x['i']] for x in descr[l]])

        return cached_types

    def gen_func(x):
        n = x['num']
        nn = n - 1

        if n >= 4:
            codec = 'xz'
        else:
            codec = 'gz'

        ygf = y.gen_func
        name = x['base']
        generator = by_name[name]['generator']

        f1 = lambda info: generator(info, lambda: deps(nn)(), n, codec)
        f2 = lambda info: ygf(f1, info)
        f3 = y.cached()(f2)

        descr = {
            'gen': 'lay',
            'base': x['base'],
            'layer': num,
            'kind': ['lay'],
            'code': f3,
            'prev': x,
        }

        return descr

    by_id = {}
    
    for i in sorted(descr.keys()):
        for x in descr[i]:
            id = x['base'] + '_' + x['num']

            if id in by_id:
                continue

            res = gen_func(x)
            by_id[id] = res
            all_funcs.append(res)
            x['i'] = len(all_funcs) - 1

            channel({'func': res})


@y.defer_constructor
def init():
    @y.gd_callback('build env')
    def solver(arg):
        def func(name, info):
            send_all_plugins_to_queue()

            return eval(name)(info)

        arg['back_channel']({'func': lambda info: func('y.cached_deps4', info), 'descr': ['system', 'coreutils', 'gnu']})
        arg['back_channel']({'func': lambda info: func('y.cached_deps5', info), 'descr': ['system', 'coreutils', 'gnu']})
