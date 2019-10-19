from .ft import singleton
from .db import store_node, restore_node


def iter_targets():
    for a in ('x86_64', 'aarch64'):
        for o in ('linux', 'darwin'):
            yield {
                'arch': a,
                'os': o,
            }


@singleton
def iter_android_ndk_20():
    return list(iter_android_ndk_20_x())


def iter_android_ndk_20_x():
    host = {'arch': 'x86_64', 'os': 'darwin'}

    by_arch = {
        'aarch64': 'toolchains/aarch64-linux-android-4.9/prebuilt/darwin-x86_64',
        'x86_64': 'toolchains/x86_64-4.9/prebuilt/darwin-x86_64',
    }

    for t in iter_targets():
        res = {
            'node': {
                'build': [
                    'mkdir $(INSTALL_DIR)/tmp && cd $(INSTALL_DIR)/tmp',
                    'unzip $(BUILD_DIR)/fetched_urls/android-ndk-r20-darwin-x86_64.zip -d .',
                    'mv android-ndk-r20/' + by_arch[t['arch']] + ' $(INSTALL_DIR)/',
                    'cd $(INSTALL_DIR) && rm -rf ./tmp',
                ],
                'prepare': [
                    'export PATH=$(CUR_DIR)/darwin-x86_64/' + t['arch'] + '-linux-android/bin:$PATH'
                ],
                'url': 'https://dl.google.com/android/repository/android-ndk-r20-darwin-x86_64.zip',
                'pkg_full_name': 'android-ndk-r20-darwin-x86_64.zip',
                'kind': 'spizdili',
                'name': 'android-cross-linkers',
                'version': 'r20',
                'constraint': {'host': host, 'target': t},
                'codec': 'xz',
            },
            'deps': []
        }

        yield store_node(res)


def find_android_linker_by_cc(cc, cmp):
    for n in iter_android_ndk_20():
        ncc = restore_node(n)['node']()['constraint']

        if cmp(ncc) == cmp(cc):
            yield n
