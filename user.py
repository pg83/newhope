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
from gen_id import to_visible_name, cur_build_system_version
from bb import find_busybox


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


def tools(info):
    return [x(info) for x in TOOLS.values()]


def helper(func):
    def wrapper(src, info):
        name = func.__name__
        wrapper.__name__ = name
        
        info = subst_info(info)
        data = 'cd $(BUILD_DIR)\n' + func()

        def iter_compilers():
            if '#pragma cc' not in data:
                return

            if is_cross(info):
                cinfo = json.loads(json.dumps(info))
                cinfo['target'] = cinfo['host']

                yield find_compiler_id(cinfo)

            yield find_compiler_id(info)

        return {
            'node': {
                'name': func.__name__,
                "url": src,
                "constraint": info,
                "from": __file__,
                'build': [x.strip() for x in data.split('\n')],
            },
            'deps': list(iter_compilers()),
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

        $(FETCH_URL) ./configure --prefix=$(INSTALL_DIR) && make && make install
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


USER_PACKAGES = {
    'busybox': fp(bb, 'https://www.busybox.net/downloads/busybox-1.30.1.tar.bz2'),
    'musl': fp(musl, 'https://www.musl-libc.org/releases/musl-1.1.23.tar.gz'),
    'm4': fp(m4, 'https://ftp.gnu.org/gnu/m4/m4-1.4.18.tar.gz'),
    'pkg-config': fp(pkg_config, 'https://pkg-config.freedesktop.org/releases/pkg-config-0.29.2.tar.gz'),
    #fp(ncurses, 'https://ftp.gnu.org/pub/gnu/ncurses/ncurses-6.1.tar.gz'),
    #fp(tb, 'http://landley.net/toybox/downloads/toybox-0.8.1.tar.gz'),
}


def find_busybox_ex(info):
    return find_busybox(info['host'], info['target'])


TOOLS = {
    'xz': fp(xz, 'https://tukaani.org/xz/xz-5.2.4.tar.gz'),
    'tar': fp(tar, 'https://ftp.gnu.org/gnu/tar/tar-1.32.tar.gz'),
    'xz1': fp(xz, 'https://tukaani.org/xz/xz-5.2.4.tar.gz'),
    'tar1': fp(tar, 'https://ftp.gnu.org/gnu/tar/tar-1.32.tar.gz'),
    'busybox1': find_busybox_ex,
}


def add_tool_deps(pkg, data):
    def iter_tools():
        for k, v in TOOLS.items():
            kk = '$(' + k.upper() + '_'
            
            if kk in data:
                yield v(pkg['constraint'])

    return list(iter_tools())


def gen_packs(host=current_host_platform(), targets=['x86_64', 'aarch64']):
    for x in USER_PACKAGES.values():
        for target in targets:
            yield x({'target': target, 'host': host})

    for x in TOOLS.values():
            for target in targets:
                yield x({'target': target, 'host': host})
