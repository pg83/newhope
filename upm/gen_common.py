def calc_name(x):
    for l in x['template'].split('\n'):
        if 'return ' in l:
            l = l.split('(')[0]
            l = l.split( )[-1]

            return l.strip()[:-1]

    raise Exception('shit ' + x)


def fix_user_data(iter):
    for f in iter:
        f = y.deep_copy(f)

        ss = f.get('support', [])

        if ss and 'darwin' not in ss:
            continue

        if 'name' not in f:
            f['name'] = calc_name(f)

        yield f


@y.singleton
def iter_all_user_templates():
    res = []

    @y.read_callback('new functions templates', 'iter_all')
    def cb(data):
        res.extend(fix_user_data([data]))

    return res
