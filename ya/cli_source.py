@y.main_entry_point
async def cli_pkg_source(arg):
    lst = await y.main_makefile(y.iter_all_cc, y.all_distro_packs(), kind='data')
    nodes = []
    by_rdep = y.collections.defaultdict(set)

    for i, node in enumerate(lst):
        node['i'] = i

    for node in lst:
        for rd in node['deps2']:
            by_rdep[rd].add(node['i'])

        for d in node['deps1']:
            for a in arg:
                if a in d:
                    nodes.append(node)

    vs = set()

    def visit(n):
        if n['i'] not in vs:
            yield n

            vs.add(n['i'])

            for d in n['deps2']:
                for y in by_rdep[d]:
                    for x in visit(lst[y]):
                        yield x

    urls = []

    for n in nodes:
        for v in visit(n):
            d = v['deps1'][0]

            if d.startswith('$SD'):
                url = v['cmd'][0].split('"')[1]

                urls.append((d, url))

    for d, u in urls:
        y.info('{bg}fetch', d, u, '{}')
        y.fetch_http('data', u, name=d[4:])
