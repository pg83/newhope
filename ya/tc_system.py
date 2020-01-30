@y.singleton
def iter_darwin():
    def iter_nodes():
        for k in ('c', 'c++', 'linker'):
            meta = {'kind': [k, 'tool']}
            path = '/usr/bin/clang'

            if k == 'c':
                meta['provides'] = [
                    {'env': 'CC', 'value': '"' + path + '"'},
                    {'env': 'CFLAGS', 'value': '"$TARGET $CFLAGS"'},
                    {'env': 'AR', 'value': '"ar"'},
                    {'env': 'RANLIB', 'value': '"ranlib"'},
                    {'env': 'STRIP', 'value': '"strip"'},
                    {'env': 'NM', 'value': '"nm"'},
                ]
            elif k == 'c++':
                meta['provides'] = [
                    {'env': 'CXX', 'value': '"' + path + '"'},
                ]
            elif k == 'linker':
                meta['provides'] = [
                    {'env': 'LD', 'value': '"' + path + '"'},
                ]

            yield meta

    def do_iter():
        for meta in iter_nodes():
            for t in y.iter_all_targets():
                m = y.dc(meta)
                m['provides'] = [
                    {
                        'env': 'TARGET',
                        'value': '"--target=' + t['os'] + '-' + t['arch'] + '"',
                    }
                ] + m['provides']

                n = {
                    'name': '-'.join(['clang'] + meta['kind'] + [y.burn(t)]),
                    'version': y.burn(meta),
                    'meta': m,
                    'host': t,
                }

                yield y.dc({
                    'node': n,
                    'deps': [],
                })

    return list(do_iter())


def iter_system_tools():
    return iter_darwin()
