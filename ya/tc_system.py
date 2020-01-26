@y.singleton
def find_system_tools():
    def iter_candidates():
        yield 'clang', {'kind': ['c'], 'type': 'clang'}
        yield 'clang++', {'kind': ['c++'], 'type': 'clang'}
        yield 'ld.lld', {'kind': ['linker'], 'type': 'lld', 'os': 'linux'}
        yield 'ld64.lld', {'kind': ['linker'], 'type': 'lld', 'os': 'darwin'}
        yield 'lld-link', {'kind': ['linker'], 'type': 'lld', 'os': 'windows'}
        yield 'wasm-ld', {'kind': ['linker'], 'type': 'lld', 'os': 'webasm'}

    def find():
        def find_cand():
            for tool, info in iter_candidates():
                for tp in y.find_tool(tool):
                    if tp:
                        y.info('find tool', tp, info)

                        yield tp, info

        for tp, info in find_cand():
            if info['type'] == 'clang':
                if not y.os.path.isfile(y.os.path.dirname(tp) + '/llvm-ar'):
                    y.info('skip', tp, 'cause not full tool chain')
                    continue

            try:
                data = y.subprocess.check_output([tp, '--version'], stderr=y.subprocess.STDOUT, shell=False)
            except Exception as e:
                data = str(e)

            info.update({'name': y.os.path.basename(tp), 'path': tp, 'data': data})

            yield info

    return list(find())


def parse_gcc(info):
    if 'clang' in info['data']:
        yield from parse_clang(info)

        return

    raise Exception('todo')


def parse_clang_info(data):
    lines = data.strip().split('\n')
    info = {}
    info['version'] = lines[0].split(' ')[3]

    for l in lines:
        l = l.strip()

        if not l:
            continue

        if not l.startswith('Target'):
            continue

        k, v = l.split(':')

        if k != 'Target':
            continue

        a, b, *_ = v.strip().split('-')

        info['target'] = {
            'arch': a,
            'os': {'apple': 'darwin'}.get(b, y.platform.system().lower()),
        }

    return info


def filter_by_os(it, info):
    if 'os' in info:
        ios = info['os']

        for x in it:
            if x['os'] == ios:
                yield x
    else:
        yield from it


def parse_clang(info):
    host = y.current_host_platform()
    extra = parse_clang_info(info['data'])
    path = info['path']

    for t in filter_by_os(y.iter_all_targets(), info):
        c = {}

        cc = {
            'host': host,
            'target': t,
        }

        is_cross_c = y.is_cross(cc)

        c['constraint'] = cc
        c['version'] = extra['version']
        c['build'] = []

        tg = t['arch'] + '-' + t['os']

        def iter_kind():
            for k in info['kind']:
                yield k

                if k in ('c', 'c++') and not is_cross_c:
                    yield 'linker'

        def iter_nodes():
            where = y.os.path.dirname(path)

            for k in iter_kind():
                meta = {'kind': [k, 'tool']}

                if k == 'c':
                    meta['provides'] = [
                        {'env': 'CC', 'value': '"' + path + '"'},
                        {'env': 'CFLAGS', 'value': '"-nostdinc $CFLAGS"'.replace('{tg}', tg)},
                        {'env': 'AR', 'value': '"' + where + '/llvm-ar' + '"'},
                        {'env': 'RANLIB', 'value': '"' + where + '/llvm-ranlib' + '"'},
                        {'env': 'STRIP', 'value': '"' + where + '/llvm-strip' + '"'},
                        {'env': 'NM', 'value': '"' + where + '/llvm-nm' + '"'},
                    ]
                elif k == 'c++':
                    meta['provides'] = [
                        {'env': 'CXX', 'value': '"' + path + '"'},
                        {'env': 'CFLAGS', 'value': '"-nostdinc $CFLAGS"'.replace('{tg}', tg)},
                        {'env': 'CXXFLAGS', 'value': '"-nostdinc++ $CXXFLAGS"'},
                    ]
                elif k == 'linker':
                    meta['provides'] = [
                        {'env': 'LD', 'value': '"' + path + '"'},
                        {'env': 'LDFLAGS', 'value': '"-nostdlib -static -all-static $LDFLAGS"'},
                    ]

                n = y.dc(c)

                n['name'] = info['name']
                n['meta'] = meta

                yield n

        for n in iter_nodes():
            yield {
                'node': n,
                'deps': [],
            }


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
                    {'env': 'CXX', 'value': '"' + path + '"'},
                ]
            elif k == 'linker':
                meta['provides'] = [
                    {'env': 'LD', 'value': '"' + path + '"'},
                ]

            yield meta

    def do_iter():
        for meta in iter_nodes():
            n = {
                'name': '-'.join(['clang'] + meta['kind']),
                'build': [],
                'version': y.burn(meta),
                'meta': meta,
                'constraint': {
                    'host': y.current_host_platform(),
                    'target': y.current_host_platform(),
                },
            }

            yield {
                'node': n,
                'deps': [],
            }

    return list(do_iter())


def parse_lld(info):
    path = info['path']
    host = y.current_host_platform()

    for t in filter_by_os(y.iter_all_targets(), info):
        c = {}

        c['constraint'] = {
            'host': host,
            'target': t,
        }

        opts = extra + [
            '-fuse-ld=lld',
            '-nostdlib',
            '-static',
            '-all-static',
            '-Wl,--no-whole-archive',
            '-Wl,--sort-section,alignment',
            '-Wl,--sort-common',
            '-Wl,--gc-sections',
            '-Wl,--hash-style=both',
            '-Wl,--exclude-libs=ALL',
            '-Wl,--no-dynamic-linker',
            '-Wl,--no-export-dynamic',
        ]

        c['build'] = []
        c['name'] = 'lld'
        c['version'] = y.burn(info)
        c['meta'] = {
            'kind': ['linker', 'tool'],
            'provides': [
                {'env': 'LD', 'value': '"' + path + '"'},
                {'env': 'LDFLAGS', 'value': '"{opts} $LDFLAGS"'.replace('{opts}', ' '.join(opts))}
            ],
        }

        yield {
            'node': c,
            'deps': [],
        }


def iter_system_tools():
    yield from iter_darwin()

    return
    
    for c in y.dc(iter_darwin()):
        try:
            c['data'] = c['data'].decode('utf-8')
        except AttributeError:
            pass

        if c['type'] == 'clang':
            yield from parse_clang(c)
        elif c['type'] == 'gcc':
            yield from parse_gcc(c)
        elif c['type'] == 'lld':
            yield from parse_lld(c)
        else:
            y.os.abort()
