@y.singleton
def layers_channel():
    return y.write_channel("new functions", "layers")


@y.singleton
def layers_channel_2():
    return y.write_channel("new plugin", "layers")


def gen_all_texts(only_print_layers=False, channel=layers_channel_2()):
    by_tier = {}
    by_name = {}
    all = []
    channel = layers_channel()

    for j in y.iter_all_user_generators():
        f = y.deep_copy(j)
        f['name'] = 'lay_' + f['name']
        
        t = f['tier']
        by_name[f['name']] = f

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
            yield i, [x['name'] for x in calc_level(i)]

    by_level = dict(calc_levels())

    def iter_layers():
        for i in levels:
            yield i

        yield levels[-1]

    to_build = list(iter_layers())

    def iter():
        for i, l in enumerate(to_build):
            yield i + 1, [{'name': x, 'num': i + 1} for x in by_level[l]]

    descr = dict(iter())

    def gen_name(x):
        return x['name'] + str(x['num'])
    
    all_funcs = []

    @y.cached()
    def deps(l):
        @y.singleton
        def cached_types():
            if l == 0:
                return []

            return y.join_funcs('devtools', l, [all_funcs[x['i']] for x in descr[l]])

        return cached_types

    def gen_func(x):
        n = x['num']
        nn = n - 1

        if n >= 4:
            codec = 'xz'
        else:
            codec = 'gz'

        ygf = y.gen_func
        name = x['name']
        fname = name + str(n)
        generator = by_name[name]['generator']
        f1 = generator(lambda: deps(nn)(), n, fname, codec)
        f1.__name__ = 'f1_' + fname
        f2 = lambda info: ygf(f1, info)
        f2.__name__ = 'f2_' + fname
        f3 = y.cached()(f2)
        f3.__name__ = fname

        channel({'func': f3, 'kind': ['layers']})

        return f3

    by_id = {}
    by_num = {}
    
    def iter_allx_funcs():
        for i in sorted(descr.keys()):
            for x in descr[i]:
                xn = x['num']
                xnn = x['name']

                if xn not in by_num:
                    by_num[xn] = [xnn]
                else:
                    by_num[xn].append(xnn)

                id = xnn + '_' + str(xn)

                if id not in by_id:
                    res = gen_func(x)
                    by_id[id] = res
                    all_funcs.append(res)
                    x['i'] = len(all_funcs) - 1

                    yield res, xnn

    list(iter_allx_funcs())

    if only_print_layers:
        for i in sorted(by_num.keys()):
            print >>y.sys.stderr,  i, by_num[i]


@y.defer_constructor
def init():
    @y.read_callback('build env', 'layers')
    def solver(arg):
        def func(name, info):
            send_all_plugins_to_queue()

            return eval(name)(info)

        arg['back_channel']({'func': lambda info: func('y.cached_deps4', info), 'descr': ['system', 'coreutils', 'gnu']})
        arg['back_channel']({'func': lambda info: func('y.cached_deps5', info), 'descr': ['system', 'coreutils', 'gnu']})
