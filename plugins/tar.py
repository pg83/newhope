def tar0(info, deps, codec):
    return {
        'code': 'FORCE_UNSAFE_CONFIGURE=1 ./configure --prefix=$(INSTALL_DIR) && make && make install',
        'prepare': '$(ADD_PATH)',
        'src': 'https://ftp.gnu.org/gnu/tar/tar-1.32.tar.gz',
        'deps': deps,
        'codec': codec,
    }


@helper
def tar2(info):
    return tar0(info, [bestbox2(info), make2(info)], 'gz')


@helper
def tar1(info):
    return tar0(info, [bestbox2(info), tar2(info), xz2(info), make2(info), curl2(info), musl2(info)], 'xz')


@helper
def tar(info):
    return tar0(info, [bestbox1(info), tar1(info), xz1(info), make1(info), curl1(info), musl1(info)], 'xz')


@splitter(folders=['/bin'])
def tar_runtime(info):
    return tar(info)


@splitter(folders=['/share'])
def tar_docs(info):
    return tar(info)
