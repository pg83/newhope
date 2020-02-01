async def gen_mk_data(cc, distr):
    funcs = []

    for c in cc:
        loop = y.PubSubLoop()

        await loop.run(init=[y.mk_funcs_gen(c, funcs.append, distr)])

    return funcs


async def main_makefile(iter_cc, distr, kind='text'):
    cc = list(iter_cc())
    portion = await gen_mk_data(cc, distr)

    return await y.build_makefile([x['code']() for x in portion], kind=kind)
