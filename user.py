import os
import sys
import subprocess
import json
import gen_id

def fp(f, v, *args, **kwargs):
    def wrap(*args, **kwargs):
        return f(v, *args, **kwargs)

    return wrap


from cc import find_compiler
from gen_id import to_visible_name, cur_build_system_version, deep_copy
from bb import find_busybox


def singleton(f):
    def wrapper():
        try:
            f.__res
        except AttributeError:
            f.__res = f()

        return f.__res

    return wrapper


def cached(f):
    v = {}

    def wrapper(*args, **kwargs):
        k = gen_id.struct_dump([args, kwargs])

        if f not in v:
            v[k] = f(*args, **kwargs)

        return deep_copy(v[k])

    return wrapper


@singleton
def current_host_platform():
    data = subprocess.check_output(['/bin/uname', '-a'], shell=False).strip();

    for x in ('aarch64', 'x86_64'):
        if x in data:
            return x

    return data.split()[-1]


@cached
def find_compiler_id(info):
    info = gen_id.deep_copy(info)

    info.pop('build_system_version')

    for x in find_compiler(info):
        return x

    raise Exception('shit happen')


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


@cached
def tools(info):
    return [x(info) for x in TOOLS.values()]


def helper(func):
    def wrapper(src, info):
        name = func.__name__
        wrapper.__name__ = name

        info = subst_info(info)
        data = func()

        def iter_compilers():
            if '#pragma cc' not in data:
                return

            if is_cross(info):
                cinfo = json.loads(json.dumps(info))
                cinfo['target'] = cinfo['host']

                yield find_compiler_id(cinfo)

            yield find_compiler_id(info)

        deps = list(iter_compilers())
        cross_cc = deps[-1]

        return {
            'node': {
                'name': func.__name__,
                "url": src,
                "constraint": info,
                "from": __file__,
                'build': ['ln -sf `which ' + cross_cc['node']['prefix'][1] + 'gcc` /bin/cc'] + [x.strip() for x in data.split('\n')],
            },
            'deps': deps,
        }

    return wrapper


@helper
def tb():
    return """
        #pragma cc

        $(FETCH_URL)
        LDFLAGS=--static CFLAGS=-O2 CC=gcc CROSS_COMPILE=$TOOL_CROSS_PREFIX make defconfig toybox
        mv toybox $(INSTALL_DIR)
    """


@helper
def m4():
    return """
        #pragma cc

        export PATH=$(CURL1_BIN_DIR):$PATH
        $(FETCH_URL) ./configure --prefix=$(INSTALL_DIR) && make && make install
    """


@helper
def curl1():
    return """
        #pragma cc

        $(FETCH_URL) ./configure --prefix=$(INSTALL_DIR) --with-mbedtls=$(MBEDTLS1_LIB_DIR) --enable-static --disable-shared && make && make install
    """


@helper
def xz():
    return """
        export PATH=$(BUSYBOX1_BIN_DIR):$PATH

        $(FETCH_URL) ./configure --prefix=$(INSTALL_DIR) --disable-shared --enable-static && make && make install

        #pragma cc
        #pragma manual deps
    """


@helper
def bb():
    return """
        #pragma cc

        $(FETCH_URL)
        make CROSS_COMPILE=$TOOL_CROSS_PREFIX defconfig
        make CROSS_COMPILE=$TOOL_CROSS_PREFIX
        ./busybox mv ./busybox $(INSTALL_DIR)/
    """


@helper
def musl():
    return """
        #pragma cc

        $(FETCH_URL)
        LDFLAGS=--static CFLAGS=-O2 CROSS_COMPILE=$TOOL_CROSS_PREFIX ./configure --prefix=$(INSTALL_DIR) --enable-static --disable-shared && make && make install
    """


@helper
def ncurses():
    return """
        #pragma cc

        $(FETCH_URL)
        sed -i s/mawk// configure
        ./configure --prefix=$(INSTALL_DIR) --without-shared --without-debug --without-ada --enable-widec --enable-overwrite && make && make install
    """


@helper
def pkg_config():
    return """
        #pragma cc

        $(FETCH_URL)
        LDFLAGS=--static ./configure --prefix=$(INSTALL_DIR) --with-internal-glib --enable-static --disable-shared && make && make install
    """


@helper
def tar():
    return """
        export PATH=$(BUSYBOX1_BIN_DIR):$(XZ_BIN_DIR):$PATH

        $(FETCH_URL) FORCE_UNSAFE_CONFIGURE=1 ./configure --prefix=$(INSTALL_DIR) && make && make install

        #pragma cc
        #pragma manual deps
    """


@helper
def mbedtls1():
    return """
        rm -rf /usr/local
        $(FETCH_URL) make programs lib && make install
        cd /usr/local && mv * $(INSTALL_DIR)/

        #pragma cc
    """


USER_PACKAGES = {
    'busybox': fp(bb, 'https://www.busybox.net/downloads/busybox-1.30.1.tar.bz2'),
    'musl': fp(musl, 'https://www.musl-libc.org/releases/musl-1.1.23.tar.gz'),
    'm4': fp(m4, 'https://ftp.gnu.org/gnu/m4/m4-1.4.18.tar.gz'),
    'pkg-config': fp(pkg_config, 'https://pkg-config.freedesktop.org/releases/pkg-config-0.29.2.tar.gz'),
    'mbedtls': fp(mbedtls1, 'https://tls.mbed.org/download/mbedtls-2.16.3-apache.tgz'),
    #fp(ncurses, 'https://ftp.gnu.org/pub/gnu/ncurses/ncurses-6.1.tar.gz'),
    #fp(tb, 'http://landley.net/toybox/downloads/toybox-0.8.1.tar.gz'),
}


def find_busybox_ex(info):
    return find_busybox(info['host'], info['target'])


def iter_tools():
    tools = [
        ('xz', fp(xz, 'https://downloads.sourceforge.net/project/lzmautils/xz-5.2.4.tar.gz')),
        ('tar', fp(tar, 'https://ftp.gnu.org/gnu/tar/tar-1.32.tar.gz')),
        ('xz1', fp(xz, 'https://downloads.sourceforge.net/project/lzmautils/xz-5.2.4.tar.gz')),
        ('tar1', fp(tar, 'https://ftp.gnu.org/gnu/tar/tar-1.32.tar.gz')),
        ('mbedtls1', fp(mbedtls1, 'https://tls.mbed.org/download/mbedtls-2.16.3-apache.tgz')),
        ('curl1', fp(curl1, 'https://curl.haxx.se/snapshots/curl-7.67.0-20191011.tar.bz2')),
        ('busybox1', find_busybox_ex),
    ]

    res = {}

    for k, func in tools:
        func.__name__ = k
        res[k] = func

    return res


TOOLS = iter_tools()


def add_tool_deps(pkg, data):
    def iter_tools():
        for k, v in TOOLS.items():
            kk = '$(' + k.upper() + '_'

            if kk in data:
                cc = json.loads(json.dumps(pkg['constraint']))
                cc['host'] = cc['target']

                yield v(cc)

    return list(iter_tools())


def gen_packs(host=current_host_platform(), targets=['x86_64', 'aarch64']):
    for x in USER_PACKAGES.values():
        for target in targets:
            yield x({'target': target, 'host': host})

    for x in TOOLS.values():
        for target in targets:
            yield x({'target': target, 'host': host})
