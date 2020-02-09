def gen_package_name(x):
    res = x['gen']

    if res:
        res += '-'

    res += x['base']

    if 'num' in x:
        res += str(x['num'])

    return res


def fix_pkg_name(res, descr):
    res = y.dc(res)

    res['node']['name'] = gen_package_name(descr)
    res['node']['gen'] = descr['gen']

    return res
