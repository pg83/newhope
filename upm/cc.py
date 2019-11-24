V = {
    'common': {
        'kind': ['c', 'c++', 'linker'],
        'type': 'gcc',
        'name': 'gcc',
        'version': '9.2',
        'build': [
            '#pragma manual deps',
            '$(FETCH_URL_2)',
            'rm -rf $(BUILD_DIR)/fetched_urls',
            'mv $(BUILD_DIR)/* $(INSTALL_DIR)/'
        ],
        'prepare': [
            'export PATH=$(GCC_BIN_DIR):$PATH',
            'export LDFLAGS="--static $LDFLAGS"',
            'export CFLAGS="-O2 -I$(GCC_INC_DIR) $CFLAGS"',
        ],
        'codec': 'gz',
    },
    "barebone": [
        {
            'prefix': ['tool_native_prefix', 'x86_64-linux-musl-'],
            "url": "https://musl.cc/x86_64-linux-musl-native.tgz",
            "constraint": {
                'host': {
                    'os': 'linux',
                    'arch': 'x86_64',
                },
            },
        },
        {
            'prefix': ['tool_native_prefix', 'aarch64-linux-musl-'],
            "url": "https://musl.cc/aarch64-linux-musl-native.tgz",
            "constraint": {
                'host': {
                    'os': 'linux',
                    'arch': 'aarch64',
                },
            },
        },
        {
            'prefix': ['tool_cross_prefix', 'aarch64-linux-musl-'],
            "url": "https://musl.cc/aarch64-linux-musl-cross.tgz",
            "constraint": {
                'host': {
                    'os': 'linux',
                    'arch': 'x86_64',
                },
                'target': {
                    'arch': 'aarch64',
                },
            },
        },
    ],
}


def fix_constraints(h, t):
    for k, v in h.items():
        if k not in t:
            t[k] = v


def fix_constraints_cc(cc):
    cc = y.deep_copy(cc)

    if 'target' not in cc:
        cc['target'] = {}

    fix_constraints(cc['host'], cc['target'])

    cc['is_cross'] = is_cross(cc)

    return y.deep_copy(cc)


def small_repr(c):
    return c['os'] + '-' + c['arch']


def small_repr_cons(c):
    return small_repr(c['host']) + '$' + small_repr(c['target'])


def is_cross(cc):
    if not cc:
        return False

    return small_repr(cc['host']) != small_repr(cc['target'])


def _iter_comp():
    for v in V['barebone']:
        v = y.deep_copy(v)
        v.update(y.deep_copy(V['common']))

        v['constraint'] = fix_constraints_cc(v['constraint'])

        yield y.fix_v2({
            'node': v,
            'deps': [],
        })


def iter_musl_cc_tools():
    for n in _iter_comp():
        nd = y.store_node(n)

        c = y.deep_copy(n)
        l = y.deep_copy(n)

        c['node']['kind'] = 'c'
        c['node']['type'] = 'gcc'

        l['node']['kind'] = 'linker'
        l['node']['type'] = 'binutils'

        for x in (c, l):
            x['deps'] = [nd]
            xn = x['node']

            xn.pop('url', None)
            xn.pop('build')
            xn.pop('prepare', None)

            xn['name'] = 'muslcc-' + xn['kind'] + '-' + xn['type']

            yield y.deep_copy(x)


@y.singleton
def iter_system_compilers():
    for t in ('gcc', 'clang'):
        tp = y.find_tool(t)

        yield {
            'kind': 'c/c++/linker',
            'type': 'clang',
            'name': y.os.path.basename(tp),
            'path': tp,
            'data': y.subprocess.check_output([tp, '--version'], stderr=y.subprocess.STDOUT, shell=False),
        }


def iter_targets(*extra):
    for x in extra:
        yield x

    for a in ('x86_64', 'aarch64'):
        for o in ('linux', 'darwin'):
            yield {
                'arch': a,
                'os': o,
            }


def iter_system_impl():
    def iter_c():
        for c in iter_system_compilers():
            if c['type'] == 'clang':
                yield c

    for c in iter_c():
        data = c.pop('data')

        for l in data.decode('utf-8').strip().split('\n'):
            l = l.strip()

            if not l:
                continue

            if not l.startswith('Target'):
                continue

            k, v = l.split(':')

            if k != 'Target':
                continue

            a, b, _ = v.strip().split('-')

            host = {
                'arch': a,
                'os': {'apple': 'darwin'}.get(b, y.platform.system().lower()),
            }

            for t in iter_targets(host):
                c = y.deep_copy(c)

                cc = {
                    'host': host,
                    'target': t,
                }

                cc['is_cross'] = is_cross(cc)

                c['constraint'] = cc
                c['version'] = '9.0.0'
                c['build'] = []
                c['codec'] = 'gz'

                if cc['is_cross']:
                    c['prefix'] = ['tool_cross_prefix', '']
                    c['prepare'] = ['export CFLAGS="-O2 --target=%s-%s -fno-short-wchar"' % (t['os'], t['arch'])]
                else:
                    c['prefix'] = ['tool_native_prefix', '']
                    c['prepare'] = ['export CFLAGS="-O2"']

                yield {
                    'node': c,
                    'deps': [],
                }


def iter_system_tools():
    for n in iter_system_impl():
        c = y.deep_copy(n)
        l = y.deep_copy(n)

        c['node']['kind'] = 'c'
        c['node']['type'] = 'clang'

        l['node']['kind'] = 'linker'
        l['node']['type'] = 'binutils'

        for x in (l, c):
            xn = x['node']

            xn.pop('url', None)
            xn.pop('data', None)
            xn.pop('build')
            xn.pop('prepare', None)

            xn['name'] = 'system-' + xn['kind'] + '-' + xn['type']

            yield y.deep_copy(x)


def _iter_all_nodes():
    for node in _iter_comp():
        yield node

    for node in iter_system_impl():
        yield node
