from upm_ft import singleton
from upm_db import store_node, restore_node
from upm_xpath import run_xpath_simple as xpp


def iter_targets():
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


@singleton
def iter_android_ndk_20():
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

    for t in iter_targets():
        res = {
            'node': {
                'build': [
                    'mkdir $(INSTALL_DIR)/tmp && cd $(INSTALL_DIR)/tmp',
                    'unzip $(BUILD_DIR)/fetched_urls/android-ndk-r20-darwin-x86_64.zip -d .',
                    'mv android-ndk-r20/' + by_arch[t['arch']] + '/* $(INSTALL_DIR)/',
                    'cd $(INSTALL_DIR) && rm -rf ./tmp ' + rm_for.get(t['arch'], ''),
                ],
                'prepare': [
                    'export PATH=$(CUR_DIR)/darwin-x86_64/' + t['arch'] + '-linux-android/bin:$PATH'
                ],
                'url': 'https://dl.google.com/android/repository/android-ndk-r20-darwin-x86_64.zip',
                'pkg_full_name': 'android-ndk-r20-darwin-x86_64.zip',
                'kind': 'spizdili',
                'name': 'android-darwin-' + t['arch'],
                'version': 'r20',
                'constraint': {'host': host, 'target': t},
                'codec': 'xz',
            },
            'deps': []
        }

        need.append(store_node(res))

    by_arch = {}

    for t in need:
        res = restore_node(t)
        node = res['node']()
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
        dirname = ('$(MNGR_' + big_one[0]['node']()['name'].upper() + '_DIR)').replace('-', '_')

        res = {
            'node': {
                'build': [
                    'cd ' + dirname,
                    'cp -R ' + t['arch'] + '* $(INSTALL_DIR)/',
                    'mkdir $(INSTALL_DIR)/bin',
                    'cp -R bin/' + t['arch'] + '* $(INSTALL_DIR)/bin/',
                ] + [('cp -R ' + x + ' $(INSTALL_DIR)/bin/')  for x in llvm],
                'prepare': [
                ],
                'kind': 'spizdili',
                'name': 'small-darwin',
                'version': 'r20',
                'constraint': {'host': host, 'target': t},
                'codec': 'xz',
            },
            'deps': [big_one[1]],
        }

        need.append(store_node(res))

    return need


def find_android_linker_by_cc(cc, cmp):
    for n in iter_android_ndk_20():
        if cmp(xpp(n, 'node/constraint')) == cmp(cc):
            yield n