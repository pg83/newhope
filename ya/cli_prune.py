def iter_non_trivial_clusters(data, keyf):
    dd = y.collections.defaultdict(list)

    for x in data:
        dd[keyf(x)].append(x)

    def iter_0():
        for v in dd.values():
            if len(v) > 1:
                yield v

    return list(iter_0())


def fix_absolute_symlinks(d):
    y.info('fix absolute symlinks in', d)
    
    def iter_links():
        for a, b, c in y.os.walk(d):
            for x in c:
                p = y.os.path.join(a, x)

                if y.os.path.islink(p):
                    pp = y.os.readlink(p)

                    if pp[0] == '/':
                        yield p, pp

    for p, pp in list(iter_links()):
        y.info('relink', p, pp)
        y.os.unlink(p)
        y.os.link(pp, p)


def prune_dir(d):
    y.info('prune', d)
    
    def iter_files():
        for a, b, c in y.os.walk(d):
            for x in c:
                p = y.os.path.join(a, x)

                if y.os.path.islink(p):
                    continue

                yield p

    def smart_getsize(p):
        res = y.os.path.getsize(p)

        if res < 100:
            res += y.random.random()

        return res
                
    files = list(iter_files())
    by_size = iter_non_trivial_clusters(files, smart_getsize)

    def path_md5(p):
        with open(p, 'rb') as f:
            return y.hashlib.md5(f.read()).hexdigest()

    def iter_clusters():
        for c in by_size:
            yield from iter_non_trivial_clusters(c, path_md5)

    clusters = list(iter_clusters())

    y.os.chdir(d)
    
    for c in clusters:
        c = sorted(c, key=lambda x: (len(x), x))
        fr = c[0][len(d) + 1:]

        for to in c[1:]:
            to = to[len(d) + 1:]
            
            y.info(fr, '->', to)
            
            y.os.unlink(to)
            y.os.symlink('../' * to.count('/') + fr, to)

            
@y.main_entry_point
async def cli_cmd_prune(args):
    for a in args:
        fix_absolute_symlinks(a)
        prune_dir(a)
