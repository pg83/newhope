def iter_targets_x():
    for a in ('x86_64', 'aarch64', 'llvm'):
        for o in ('linux',):
            yield {
                'arch': a,
                'os': o,
            }


def iter_rare_targets():
    for a in ('x86_64', 'aarch64', 'arm', 'armv7a', 'i686', 'x86_64'):
        for o in ('linux',):
            yield {
                'arch': a,
                'os': o,
            }


@y.singleton
def _iter_android_ndk_20():
    host = {'arch': 'x86_64', 'os': 'darwin'}

    by_arch = {
        'aarch64': 'toolchains/aarch64-linux-android-4.9/prebuilt/darwin-x86_64',
        'x86_64': 'toolchains/x86_64-4.9/prebuilt/darwin-x86_64',
        'llvm': 'toolchains/llvm/prebuilt/darwin-x86_64',
    }

    rm_for = {
        'llvm': './include ./lib ./lib64 ./libexec ./share ./sysroot',
    }

    need = []

    for t in iter_targets_x():
        res = {
            'node': {
                'build': [
                    'mkdir $IDIR/tmp && cd $IDIR/tmp',
                    'source fetch "https://dl.google.com/android/repository/android-ndk-r20-darwin-x86_64.zip" 0',
                    'mv android-ndk-r20/' + by_arch[t['arch']] + '/* $IDIR/',
                    'cd $IDIR && rm -rf ./tmp ' + rm_for.get(t['arch'], ''),
                ],
                'prepare': [
                    'export PATH=$(CUR_DIR)/darwin-x86_64/' + t['arch'] + '-linux-android/bin:$PATH'
                ],
                'kind': ['c-linker'],
                'name': 'google',
                'version': 'r20',
                'constraint': {'host': host, 'target': t},
            },
            'deps': [],
        }

        need.append(y.store_node(y.fix_v2(res)))

    by_arch = {}

    for t in need:
        res = y.restore_node(t)
        node = res['node']
        arch = node['constraint']['target']['arch']
        by_arch[arch] = [res, t]

    big_one = by_arch['llvm']

    llvm = [
        "bin/bisect_driver.py",
        "bin/clang",
        "bin/clang++",
        "bin/clang-check",
        "bin/clang-format",
        "bin/clang-tidy",
        "bin/clang-tidy.real",
        "bin/git-clang-format",
        "bin/ld.lld",
        "bin/llvm-ar",
        "bin/llvm-as",
        "bin/llvm-config",
        "bin/llvm-cov",
        "bin/llvm-dis",
        "bin/llvm-link",
        "bin/llvm-modextract",
        "bin/llvm-nm",
        "bin/llvm-objcopy",
        "bin/llvm-profdata",
        "bin/llvm-readobj",
        "bin/llvm-strip",
        "bin/llvm-symbolizer",
        "bin/sancov",
        "bin/sanstats",
        "bin/scan-build",
        "bin/scan-view",
        "bin/yasm",
    ]

    for t in iter_rare_targets():
        res = {
            'node': {
                'build': [
                    'cd $2',
                    'cp -R ' + t['arch'] + '* $IDIR/',
                    'mkdir $IDIR/bin',
                    'cp -R bin/' + t['arch'] + '* $IDIR/bin/',
                ] + [('cp -R ' + x + ' $IDIR/bin/')  for x in llvm],
                'kind': ['c-linker'],
                'name': 'google-llvm',
                'version': 'r20',
                'constraint': {'host': host, 'target': t},
            },
            'deps': [big_one[1]],
        }

        need.append(y.store_node(y.fix_v2(res)))

    return need


def iter_ndk_tools():
    for nd in _iter_android_ndk_20():
        n = y.restore_node(nd)

        if n['node']['constraint']['target']['arch'] == 'llvm':
            continue

        c = y.deep_copy(n)
        l = y.deep_copy(n)

        c['node']['kind'] = ['c']
        l['node']['kind'] = ['linker']

        if n['node']['name'] == 'google':
            c['node']['type'] = 'gcc'
            l['node']['type'] = 'binutils'

            all = [c, l]
        else:
            c['node']['type'] = 'clang'

            lb = y.deep_copy(l)
            lb['node']['type'] = 'binutils'

            ll = y.deep_copy(l)
            ll['node']['type'] = 'llvm'

            all = [c, lb, ll]

        for x in all:
            x['deps'] = [nd]
            xn = x['node']

            xn.pop('url', None)
            xn.pop('build')
            xn.pop('prepare', None)

            xn['name'] = 'ndk-' + '-'.join(xn['kind']) + '-' + xn['type']

            yield y.deep_copy(x)

