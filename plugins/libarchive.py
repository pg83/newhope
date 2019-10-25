def libarchive0(info, deps):
    version = '3.4.0'
    name = 'libarchive'

    return to_v2({
        'url': 'https://libarchive.org/downloads/' + name + '-' + version + '.tar.gz',
        'code': """
            ./configure --prefix=$(INSTALL_DIR) --enable-static --disable-shared
        """,
        'name': name,
        'version': version,
        'deps': dep_list(info, deps),
    }, info)


@y.options()
def libarchive1(info):
    return libarchive0(info, [bestbox1_run, coreutils1_run, tar1_run, xz1_run, curl1_run, make1_run])


@y.options()
def libarchive(info):
    return libarchive0(info, [bestbox_run, coreutils_run, tar_run, xz_run, curl_run, make_run])
