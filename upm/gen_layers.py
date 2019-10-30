import sys


def calc_name(x):
    for l in x['template'].split('\n'):
        if 'return ' in l:
            l = l.split('(')[0]
            l = l.split( )[-1]

            return l.strip()[:-1]

    raise Exception('shit ' + x)


def gen_all_texts():
    by_tier = {}
    by_name = {}
    all = []

    for f in y.all_my_funcs():
        f = y.deep_copy(f)

        ss = f.get('support', [])

        if ss and 'darwin' not in ss:
            continue

        if 'name' not in f:
            f['name'] = calc_name(f)

        t = f['tier']
        by_name[f['name']] = f

        if t in by_tier:
            by_tier[t].append(f)
        else:
            by_tier[t] = [f]

        all.append(f)

    levels = list(sorted(by_tier.keys()))

    #import json
    #print >>sys.stderr, json.dumps(by_name, indent=4, sort_keys=True)

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

        res = [gen_name(x) for x in descr[l]]

        by_val = '[' + ', '.join([x + '(info)' for x in res]) + ']'
        by_typ = '[' + ', '.join(res) + ']'

        return {
            'deps': by_val,
            'deps_funcs': by_typ,
        }

    @y.cached()
    def gen_func(x):
        d = deps(x['num'] - 1)

        if x['num'] >= 4:
            codec = 'xz'
        else:
            codec = 'gz'

        n = x['num'] - 1

        args = dict(
            name=x['name'],
            num=x['num'],
            deps='cached_deps%s(info)' % n,
            deps_funcs='cached_types%s()' % n,
            options='cached=True',
            codec=codec,
        )

        for k, v in by_name[x['name']].get('extra_arg', {}).items():
            args[k] = v

        tmpl = by_name[x['name']]['template']

        return tmpl.format(**args)

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

    if 0:
        for i in sorted(by_num.keys()):
            print >>sys.stderr,  i, by_num[i]


    stmpl = """
@y.singleton
def cached_types{num}():
    return {deps_funcs}


@y.cached()
def cached_deps{num}(info):
    return [x(info) for x in cached_types{num}()]
"""
    for i in sorted(descr.keys()):
        d = deps(i - 1)

        texts.append(stmpl.format(num=i - 1, deps_funcs=d['deps_funcs']))

    return '\n\n'.join(reversed(texts))
