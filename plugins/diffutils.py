def diffutils0(info, deps):
    version = '3.7'
    url = 'https://ftp.gnu.org/gnu/diffutils/diffutils-' + version + '.tar.xz'

    return {
        'code': """
             ./configure --prefix=$(INSTALL_DIR) --disable-shared --enable-static || exit 1
             make
             make install
        """,
        'url': url,
        'deps': dep_list(info, deps),
        'version': version,
        'prepare': '$(ADD_PATH)',
    }


@y.options()
def diffutils2(info):
    return diffutils0(info, [bestbox2_run, tar2_run, xz2_run, make2_run])


@y.options()
def diffutils1(info):
    return diffutils0(info, [bestbox1_run, coreutils1_run, tar1_run, xz1_run, make1_run, curl1_run])


@y.options()
def diffutils(info):
    return diffutils0(info, [bestbox_run, coreutils_run, tar_run, xz_run, make_run, curl_run])
