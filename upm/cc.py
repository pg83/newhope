def small_repr(c):
    return c['os'] + '-' + c['arch']


def small_repr_cons(c):
    return small_repr(c['host']) + '$' + small_repr(c['target'])


def is_cross(cc):
    if not cc:
        return False

    return small_repr(cc['host']) != small_repr(cc['target'])


@y.singleton
def iter_system_compilers():
    for t in ('gcc', 'clang'):
        tp = y.find_tool(t)

        yield {
            'kind': ['c', 'c++', 'linker'],
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

        c['node']['kind'] = ['c']
        c['node']['type'] = 'clang'

        l['node']['kind'] = ['linker']
        l['node']['type'] = 'binutils'

        for x in (l, c):
            xn = x['node']

            xn.pop('url', None)
            xn.pop('data', None)
            xn.pop('build')
            xn.pop('prepare', None)

            xn['name'] = 'system-' + '-'.join(xn['kind']) + '-' + xn['type']

            yield y.deep_copy(x)
