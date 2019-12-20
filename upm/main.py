async def gen_full_dump(iter_cc):
    data, portion = await main_makefile(iter_cc)
    lst = [y.restore_node_node(d) for d in sorted(portion)]

    y.stdout.write(y.json.dumps(sorted(lst, key=lambda x: x['name']), indent=4, sort_keys=True))
    
        
async def main_makefile(iter_cc, internal=False):    
    cc = list(iter_cc())
    funcs = []
        
    await y.pubsub.run(init=[y.mf_function_holder_gen(cc, funcs.append)])

    portion = [x() for x in funcs]

    return await y.build_makefile(portion, internal=internal), portion
