def coreutils0(info, deps):
    version = '8.31'

    return to_v2({
        'code': """
             ./configure --prefix=$(INSTALL_DIR) --disable-shared --enable-static || exit 1
             make
             make install -j 2
        """,
        'url': 'https://ftp.gnu.org/gnu/coreutils/coreutils-' + version + '.tar.xz',
        'deps': dep_list(info, deps),
        'version': version,
        'prepare': '$(ADD_PATH)',
    }, info)


@y.options()
def coreutils2(info):
    return coreutils0(info, [bestbox2_run, tar2_run, xz2_run, make2_run])


@y.options()
def coreutils1(info):
    return coreutils0(info, [bestbox1_run, tar1_run, xz1_run, make1_run, bison1_run, curl1_run])


@y.options()
def coreutils(info):
    return coreutils0(info, [bestbox_run, tar_run, xz_run, make_run, bison_run, curl_run, m4_run])
