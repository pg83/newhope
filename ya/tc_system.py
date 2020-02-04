@y.singleton
def iter_darwin():
    def iter_nodes():
        for k in ('c', 'c++', 'linker'):
            meta = {'kind': [k, 'tool']}
            path = '/usr/bin/clang'

            if k == 'c':
                meta['provides'] = [
                    {'env': 'CC', 'value': '"' + path + '"'},
                    {'env': 'CFLAGS', 'value': '"$CFLAGS"'},
                    {'env': 'AR', 'value': '"ar"'},
                    {'env': 'RANLIB', 'value': '"ranlib"'},
                    {'env': 'STRIP', 'value': '"strip"'},
                    {'env': 'NM', 'value': '"nm"'},
                ]
            elif k == 'c++':
                meta['provides'] = [
                    {'env': 'CXX', 'value': '"' + path + '++"'},
                ]
            elif k == 'linker':
                meta['provides'] = [
                    {'env': 'LD', 'value': '"' + path + '"'},
                ]

            yield meta

    def do_iter():
        for meta in iter_nodes():
            m = y.dc(meta)

            n = {
                'name': '-'.join(['clang'] + meta['kind'] + [y.burn(t)]),
                'version': y.burn(meta),
                'meta': m,
                'host': {'os': 'darwin', 'arch': 'x86_64'},
                'target': {'os': 'darwin', 'arch': 'x86_64'},
            }

            yield y.dc({
                'node': n,
                'deps': [],
            })

    return list(do_iter())


@y.singleton
def iter_linux():
    def iter_nodes():
        for k in ('c', 'c++', 'linker'):
            meta = {'kind': [k, 'tool']}
            path = '/usr/bin/clang'

            if k == 'c':
                meta['provides'] = [
                    {'env': 'CC', 'value': '"' + path + '"'},
                    {'env': 'CFLAGS', 'value': '"-nostdinc $CFLAGS"'},
                    {'env': 'AR', 'value': '"/usr/bin/llvm-ar"'},
                    {'env': 'RANLIB', 'value': '"/usr/bin/llvm-ranlib"'},
                    {'env': 'STRIP', 'value': '"/usr/bin/llvm-strip"'},
                    {'env': 'NM', 'value': '"/usr/bin/llvm-nm"'},
                ]
            elif k == 'c++':
                meta['provides'] = [
                    {'env': 'CXX', 'value': '"' + path + '++"'},
                    {'env': 'CXXFLAGS', 'value': '"-nostdinc++ $CXXFLAGS"'},
                ]
            elif k == 'linker':
                meta['provides'] = [
                    {'env': 'LD', 'value': '"' + path + '"'},
                    {'env': 'LDFLAGS', 'value': '"-static -all-static -nostdlib -fuse-ld=/usr/bin/ld.lld $LDFLAGS"'},
                ]

            yield meta

    def do_iter():
        for meta in iter_nodes():
            for t in y.iter_all_targets():
                m = y.dc(meta)

                for libc in ('uclibc', 'musl', 'glibc'):
                    n = {
                        'name': '-'.join(['clang'] + meta['kind'] + [y.burn(t)]),
                        'version': y.burn(meta),
                        'meta': m,
                        'host': {'os': 'linux', 'arch': 'x86_64', 'libc': libc},
                        'target': t,
                    }

                    yield y.dc({
                        'node': n,
                        'deps': [],
                    })

    return list(do_iter())


def iter_system_tools():
    return iter_darwin() + iter_linux()
