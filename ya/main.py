def gen_mk_data(cc, distr):
    funcs = []

    for c in cc:
        y.generate_data(c, funcs.append, distr)

    return funcs


def main_makefile(iter_cc, distr, kind='text'):
    cc = list(iter_cc())
    portion = gen_mk_data(cc, distr)

    return y.build_makefile([x['code']() for x in portion], kind=kind)
