@y.singleton
def iter_darwin():
    def iter_nodes():
        for k in ('c', 'c++', 'linker'):
            meta = {'kind': [k, 'tool']}
            path = '/usr/bin/clang'

            if k == 'c':
                meta['provides'] = [
                    {'tool': 'CC', 'value': '"' + path + '"'},
                    {'tool': 'CFLAGS', 'value': '"$CFLAGS"'},
                    {'tool': 'AR', 'value': '"ar"'},
                    {'tool': 'RANLIB', 'value': '"ranlib"'},
                    {'tool': 'STRIP', 'value': '"strip"'},
                    {'tool': 'NM', 'value': '"nm"'},
                ]
            elif k == 'c++':
                meta['provides'] = [
                    {'tool': 'CXX', 'value': '"' + path + '++"'},
                ]
            elif k == 'linker':
                meta['provides'] = [
                    {'tool': 'LD', 'value': '"' + path + '"'},
                ]

            yield meta

    def do_iter():
        for meta in iter_nodes():
            m = y.dc(meta)

            n = {
                'name': '-'.join(['clang'] + meta['kind']),
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
            path = y.find_tool('clang')[0]
            pdir = y.os.path.dirname(path)

            if k == 'c':
                meta['provides'] = [
                    {'tool': 'CC', 'value': '"' + path + '"'},
                    {'tool': 'CFLAGS', 'value': '"-nostdinc $CFLAGS"'},
                    {'tool': 'AR', 'value': '"' + pdir + '/llvm-ar"'},
                    {'tool': 'RANLIB', 'value': '"' + pdir + '/llvm-ranlib"'},
                    {'tool': 'STRIP', 'value': '"' + pdir + '/llvm-strip"'},
                    {'tool': 'NM', 'value': '"' + pdir + '/llvm-nm"'},
                ]
            elif k == 'c++':
                meta['provides'] = [
                    {'tool': 'CXX', 'value': '"' + path + '++"'},
                    {'tool': 'CXXFLAGS', 'value': '"-nostdinc++ $CXXFLAGS"'},
                ]
            elif k == 'linker':
                meta['provides'] = [
                    {'tool': 'LD', 'value': '"' + path + '"'},
                    {'tool': 'LDFLAGS', 'value': '"-static -all-static -nostdlib -fuse-ld=' + pdir + '/ld.lld $LDFLAGS"'},
                ]

            yield meta

    def do_iter():
        for meta in iter_nodes():
            m = y.dc(meta)

            for libc in ('uclibc', 'musl', 'glibc'):
                n = {
                    'name': '-'.join(['clang'] + meta['kind'] + [libc]),
                    'version': y.burn(meta),
                    'meta': m,
                    'host': {'os': 'linux', 'arch': 'x86_64', 'libc': libc},
                    'target': {'os': 'linux', 'arch': 'x86_64', 'libc': libc},
                }

                yield y.dc({
                    'node': n,
                    'deps': [],
                })

    return list(do_iter())


def iter_system_tools():
    return iter_darwin() + iter_linux()
