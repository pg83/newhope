def layers_channel():
    return y.write_channel("new functions", "layers")


def layers_channel_2():
    return y.write_channel("new plugin", "layers")


def gen_all_texts(only_print_layers=False, channel=layers_channel_2()):
    by_tier = {}
    by_name = {}
    all = []

    for f in y.iter_all_user_templates():
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

    @y.cached()
    def deps(l):
        if l == 0:
            return {'deps': '[]', 'deps_funcs': '[]'}

        res = ['y.' + gen_name(x) for x in descr[l]]

        by_val = '[' + ', '.join([x + '(info)' for x in res]) + ']'
        by_typ = '[' + ', '.join(res) + ']'

        return {
            'deps': by_val,
            'deps_funcs': by_typ,
        }

    def gen_func(x):
        d = deps(x['num'] - 1)

        if x['num'] >= 4:
            codec = 'xz'
        else:
            codec = 'gz'

        args = dict(
            name=x['name'],
            num=x['num'],
            deps='cached_deps%s(info)' % (x['num'] - 1),
            deps_funcs='cached_types%s()' % (x['num'] - 1),
            options='cached=True, codec="{codec}", channel="y.layers_channel()"',
            codec=codec,
            kind=by_name[x['name']]['kind'],
        )

        for k, v in by_name[x['name']].get('extra_arg', {}).items():
            args[k] = v

        tmpl = by_name[x['name']]['template']

        return tmpl.format(kw=args, **args)

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

                    yield res

    texts = []

    for x in iter_allx_funcs():
        texts.append(x)

    if only_print_layers:
        for i in sorted(by_num.keys()):
            print >>y.sys.stderr,  i, by_num[i]

        return

    stmpl = """
@y.singleton
def cached_types{num}():
    return y.join_funcs('devtools', {num}, {deps_funcs})


@y.cached()
def cached_deps{num}(info):
    return [x(info) for x in cached_types{num}()]
"""
    for i in [0] + sorted(descr.keys()):
        d = deps(i)
        texts.append(stmpl.format(num=i, deps_funcs=d['deps_funcs']))

    #channel('\n\n'.join(reversed(texts)))

    if 1:
        for i in reversed(texts):
            channel(i)
        
