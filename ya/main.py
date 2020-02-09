async def gen_mk_data(cc, distr):
    funcs = []

    for c in cc:
        y.generate_data(c, funcs.append, distr)

    return funcs


async def main_makefile(iter_cc, distr, kind='text'):
    cc = list(iter_cc())
    portion = await gen_mk_data(cc, distr)

    return await y.build_makefile([x['code']() for x in portion], kind=kind)
