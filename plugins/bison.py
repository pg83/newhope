def bison0(info, deps):
    version = '3.4.2'
    url = 'https://ftp.gnu.org/gnu/bison/bison-' + version + '.tar.xz'

    return to_v2({
        'code': """
             ./configure --prefix=$(INSTALL_DIR) --disable-shared --enable-static || exit 1
             make
             make install
             $(MOVE_LOG) config.log
        """,
        'url': url,
        'deps': dep_list(info, deps),
        'version': version,
        'prepare': '$(ADD_PATH)',
    }, info)


@y.options()
def bison2(info):
    return bison0(info, [bestbox2_run, tar2_run, xz2_run, make2_run, m4])


@y.options()
def bison1(info):
    return bison0(info, [bestbox1_run, coreutils2_run, tar1_run, xz1_run, make1_run, curl1_run, m4])


@y.options()
def bison(info):
    return bison0(info, [bestbox_run, coreutils1_run, tar_run, xz_run, make_run, curl_run, m4])
