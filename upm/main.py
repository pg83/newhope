async def gen_full_dump(iter_cc):
    await y.prepare_makefile()
    data, portion = await main_makefile(iter_cc)
    lst = [y.restore_node_node(d) for d in sorted(portion)]

    y.stdout.write(y.json.dumps(sorted(lst, key=lambda x: x['name']), indent=4, sort_keys=True))
    
        
async def main_makefile(iter_cc, internal=False):    
    data = ''
    prev = set()
    cnt = 0
    
    while True:
        portion = set(await y.gen_packs(iter_cc))

        if not portion:
            cnt += 1
        
        len_b = len(prev)
        prev = prev | portion
        len_a = len(prev)

        if (len_b == len_a and prev) or cnt > 2:
            return data, prev
        
        data = await y.build_makefile(sorted(prev), internal=internal)
