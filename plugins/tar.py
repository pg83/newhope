def tar0(info, deps, codec):
    return to_v2({
        'code': 'FORCE_UNSAFE_CONFIGURE=1 ./configure --prefix=$(INSTALL_DIR) && make && make install',
        'prepare': '$(ADD_PATH)',
        'src': 'https://ftp.gnu.org/gnu/tar/tar-1.32.tar.gz',
        'deps': deps,
        'codec': codec,
    }, info)


@y.options()
def tar2(info):
    return tar0(info, [bestbox2_run(info), make2_run(info)], 'gz')


@y.options()
def tar1(info):
    return tar0(info, [bestbox2_run(info), tar2_run(info), xz2_run(info), make2_run(info), curl2_run(info)], 'xz')


@y.options()
def tar(info):
    return tar0(info, [bestbox1_run(info), tar1_run(info), xz1_run(info), make1_run(info), curl1_run(info)], 'xz')

