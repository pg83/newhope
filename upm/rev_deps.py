def make_engine(data, ntn=lambda x: x['name'], dep_list=None, random=False, seed=''):
    data = [{'x': x, 'i': i} for i, x in enumerate(data)]
    name_to_num = dict((ntn(x['x']), x['i']) for x in data)

    def build_deps():
        for el in data:
            yield el['i'], set(name_to_num[name] for name in dep_list(el['x']))

    tbl = dict(build_deps())

    def collect_ready():
        for k in range(0, len(data)):
            if k not in tbl:
                yield k
            elif not tbl[k]:
                tbl.pop(k)
                yield k

    def remove_one(one):
        try:
            one = one['i']
        except:
            pass

        for k, v in list(tbl.iteritems()):
            if one in v:
                v.remove(one)

    md5 = y.hashlib.md5
    in_use = set()
        
    def build_tbl():
        seed_c = seed

        while len(in_use) < len(data):
            if random:
                seed_c = str(y.random.random())

            ready = sorted(list(set(collect_ready()) - in_use), key=lambda x: md5(str(x) + seed_c).hexdigest())

            if not ready:
                break

            for one in ready:                       
                in_use.add(one)
                yield data[one]

    return build_tbl, remove_one
