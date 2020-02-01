async def gen_mk_data(cc):
    funcs = []

    for c in cc:
        loop = y.PubSubLoop()

        await loop.run(init=[y.mk_funcs_gen(c, funcs.append)])

    return funcs


async def main_makefile(iter_cc, kind='text'):
    cc = list(iter_cc())
    portion = await gen_mk_data(cc)

    return await y.build_makefile([x['code']() for x in portion], kind=kind)
