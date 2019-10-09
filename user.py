import os
import sys
import subprocess
import json

def fp(f, v, *args, **kwargs):
    def wrap(*args, **kwargs):
        return f(v, *args, **kwargs)

    return wrap

from all import find_compiler, RES
from gen_id import gen_id
from bb import find_busybox
from build import build_package as build_package_xx


def cons_to_name(c):
    return '-'.join([c['host'], c['libc'], c['target']])


def to_visible_name_0(pkg):
    return (gen_id(pkg)[:8] + '-' + cons_to_name(pkg['constraint']) + '-' + os.path.basename(pkg['url']).replace('_', '-').replace('.', '-')).replace('--', '-')


def to_visible_name_1(pkg):
    def remove_compressor_name(x):
        for i in ('_tar_', '_tgz', '_tbz', '_txz'):
            p = x.find(i)

            if p > 0:
                x = x[:p]

        return x

    return remove_compressor_name(to_visible_name_0(pkg))


FUNCS = [
    to_visible_name_0,
    to_visible_name_1,
]


def cur_build_system_version():
    return len(FUNCS) - 1


def to_visible_name(pkg, version):
    return FUNCS[version](pkg)


def cur_visible_name(pkg):
    return to_visible_name(pkg, cur_build_system_version())


def build_package(pkg):
    return build_package_xx(pkg, cur_visible_name)


def singleton(f):
    def wrapper():
        try:
            f.__res
        except AttributeError:
            f.__res = f()

        return f.__res

    return wrapper


@singleton
def current_host_platform():
    data = subprocess.check_output(['/bin/uname', '-a'], shell=False).strip();

    for x in ('aarch64', 'x86_64'):
        if x in data:
            return x

    return data.split()[-1]


def find_compiler_id(info):
    for x in find_compiler(**info):
        return x

    raise Exception('shit happen')


def fix_fetch_url(src):
    fetch_url = 'which tar; which xz; wget -O - $(URL) | tar --strip-components 1 -x#f - ;'.replace('$(URL)', src)

    if '.bz2' in src:
        fetch_url = fetch_url.replace('#', 'j')
    elif '.xz' in src:
        fetch_url = fetch_url.replace('#', 'J')
    else:
        fetch_url = fetch_url.replace('#', 'z')

    return fetch_url


def subst_pkg(pkg, info, tools=[]):
    def iter_deps():
        for d in pkg['deps']:
            yield d

        for t in tools:
            yield USER_PACKAGES_1[t](info)

    pkg[deps] = list(iter_deps())


def install_dir(pkg):
    return '/managed/' + to_visible_name(pkg)


def bin_dir(pkg):
    return install_dir(pkg) + '/bin'


def bin_dir(lib):
    return install_dir(pkg) + '/lib'


def include_dir(pkg):
    return install_dir(pkg) + '/include'


def is_cross(info):
    return info['target'] != info['host']


def subst_info(info):
    info = json.loads(json.dumps(info))

    if 'host' not in info:
        info['host'] = current_host_platform()

    if 'target' not in info:
        info['target'] = 'aarch64'

    if 'libc' not in info:
        info['libc'] = 'musl'

    if 'build_system_version' not in info:
        info['build_system_version'] = cur_build_system_version()

    return info


def helper(func):
    def wrapper(src, info):
        info = subst_info(info)

        data = """
            export PATH=$(TAR_BIN_DIR):$PATH
            export PATH=$(XZ_BIN_DIR):$PATH
        """ + func()

        def iter_compilers():
            if '$(CC)' not in data:
                return

            if is_cross(info):
                cinfo = json.loads(json.dumps(info))
                cinfo['target'] = cinfo['host']

                yield find_compiler_id(cinfo)

            yield find_compiler_id(info)

        res = {
            'deps': list(iter_compilers()) + [x(info) for x in TOOLS.values()],
            'build': ['cd $(BUILD_DIR)'] + [x.strip() for x in fix_fetch_url(data).split('\n')],
            "url": src,
            "constraint": info,
            "from": __file__,
        }

        return res

    return wrapper


@helper
def tb():
    return """
        # $(CC) // TODO
        $(FETCH_URL)
        LDFLAGS=--static CFLAGS=-O2 CC=gcc CROSS_COMPILE=$TOOL_CROSS_PREFIX make defconfig toybox
        mv toybox $(INSTALL_DIR)"""


@helper
def m4():
    return '$(FETCH_URL) ./configure --prefix=$(INSTALL_DIR) && make && make install # $(CC) // TODO'


@helper
def xz_simple():
    return '$(FETCH_URL) ./configure --prefix=$(INSTALL_DIR) --disable-shared --enable-static && make && make install # $(CC) // TODO'


def dec_build_version(c):
    c = json.loads(json.dumps(c))

    c['build_system_version'] -= 1

    return c


def xz(src, info):
    if info['build_system_version'] >= 0:
        return xz_simple(src, dec_build_version(info))

    return find_busybox(info['host'], info['target'])


@helper
def bb():
    return """
        # $(CC) // TODO
        $(FETCH_URL)
        make CROSS_COMPILE=$TOOL_CROSS_PREFIX defconfig
        make CROSS_COMPILE=$TOOL_CROSS_PREFIX
        ./busybox mv ./busybox $(INSTALL_DIR)/
    """


@helper
def musl():
    return """
        # $(CC) // TODO
        $(FETCH_URL)
        LDFLAGS=--static CFLAGS=-O2 CROSS_COMPILE=$TOOL_CROSS_PREFIX ./configure --prefix=$(INSTALL_DIR) --enable-static --disable-shared && make && make install
    """


@helper
def ncurses():
    return """
        # $(CC) // TODO
        $(FETCH_URL)
        sed -i s/mawk// configure
        ./configure --prefix=$(INSTALL_DIR) --without-shared --without-debug --without-ada --enable-widec --enable-overwrite &?&? make && make        install"""


@helper
def pkg_config():
    return """
        # $(CC) // TODO
        $(FETCH_URL)
        LDFLAGS=--static ./configure --prefix=$(INSTALL_DIR) --with-internal-glib --enable-static --disable-shared && make && make install
    """


@helper
def tar_simple():
    return '$(FETCH_URL) FORCE_UNSAFE_CONFIGURE=1 ./configure --prefix=$(INSTALL_DIR) && make && make install # $(CC) // TODO'


def tar(src, info):
    if info['build_system_version'] >= 0:
        return tar_simple(src, dec_build_version(info))

    return find_busybox(info['host'], info['target'])


USER_PACKAGES = {
    'busybox': fp(bb, 'https://www.busybox.net/downloads/busybox-1.30.1.tar.bz2'),
    'musl': fp(musl, 'https://www.musl-libc.org/releases/musl-1.1.23.tar.gz'),
    'm4': fp(m4, 'https://ftp.gnu.org/gnu/m4/m4-1.4.18.tar.gz'),
    'pkg-config': fp(pkg_config, 'https://pkg-config.freedesktop.org/releases/pkg-config-0.29.2.tar.gz'),
    #fp(ncurses, 'https://ftp.gnu.org/pub/gnu/ncurses/ncurses-6.1.tar.gz'),
    #fp(tb, 'http://landley.net/toybox/downloads/toybox-0.8.1.tar.gz'),
}

TOOLS = {
    'xz': fp(xz, 'https://tukaani.org/xz/xz-5.2.4.tar.gz'),
    'tar': fp(tar, 'https://ftp.gnu.org/gnu/tar/tar-1.32.tar.gz'),
}

def gen_packs(host=current_host_platform(), targets=['x86_64', 'aarch64']):
    cur = cur_build_system_version()

    for x in USER_PACKAGES.values():
        for target in targets:
            yield x({'target': target, 'build_system_version': cur, 'host': host})

    for x in TOOLS.values():
        for i in range(-1, cur + 1):
            for target in targets:
                yield x({'target': target, 'build_system_version': i, 'host': host})


def prune_repo():
    return

    files = set()

    for x in ALL_PACKAGES:
        if 'id' in x:
            files.add(to_visible_name(x))
        else:
            print >>sys.stderr, 'unfinished', x

    for l in os.listdir('/repo/'):
        if l not in files:
            l = '/repo/' + l

            print >>sys.stderr, 'prune', l

            os.unlink(l)
