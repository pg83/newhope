async def gen_full_dump(iter_cc):
    portion = await gen_mk_data(list(iter_cc()))
    lst = [y.restore_node_node(d) for d in sorted(portion)]

    y.stdout.write(y.json.dumps(sorted(lst, key=lambda x: x['name']), indent=4, sort_keys=True))


async def gen_mk_data(cc):
    funcs = []

    for c in cc:
        loop = y.PubSubLoop()

        await loop.run(init=[y.mk_funcs_gen(c, funcs.append)])

    print funcs

    return funcs


async def main_makefile(iter_cc, internal=False):
    cc = list(iter_cc())
    portion = await gen_mk_data(cc)

    return await y.build_makefile([x['code']() for x in portion], internal=internal)


async def build_dot_script(iter_cc):
    mk = y.loads_mk(await y.main_makefile(iter_cc, internal=True))

    return y.build_dot_script_0(mk)
