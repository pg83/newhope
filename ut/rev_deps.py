def make_engine(data, ntn=lambda x: x['name'], dep_list=None, random=False, seed=''):
    data = [{'x': x, 'i': i} for i, x in enumerate(data)]
    name_to_num = dict((ntn(x['x']), x['i']) for x in data)

    def build_deps():
        for el in data:
            for v in (name_to_num.get(name, None) for name in dep_list(el['x'])):
                if v is not None:
                    yield el['i'], v

    r, w = simple_engine(build_deps(), random=random, seed=seed)

    def nw(el):
        try:
            el = el['i']
        except Exception:
            pass

        w(el)

    def nr():
        for i in r():
            yield data[i]

    return nr, nw


def simple_engine(it, random=False, seed=''):
    if random:
        seed = y.random.random()

    by_dep = y.collections.defaultdict(set)
    by_rdep = y.collections.defaultdict(set)

    for k, v in it:
        by_dep[k].add(v)
        by_rdep[v].add(k)

    deps = set(by_dep.keys())
    rdeps = set(by_rdep.keys())
    ready = rdeps - deps

    def iter_ready():
        while ready:
            tmp = list(sorted(ready, key=lambda x: y.burn([x, seed])))
            ready.clear()
            yield from tmp

    def cb(item):
        for k in by_rdep[item]:
            el = by_dep[k]

            el.remove(item)

            if not el:
                by_dep.pop(k)
                ready.add(k)

    return iter_ready, cb


def execution_sequence(it, random=False, seed=''):
    r, w = simple_engine(it, random=random, seed=seed)
    done = False

    while not done:
        done = True

        for i in r():
            done = False
            yield i
            w(i)
