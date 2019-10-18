from .xpath import xp


def m4_0(info, deps, codec):
    if xp('/info/compilers/cross') is True:
        def val(n):
            return xp('/info/compilers/deps/%s/node/prefix/1/[:-1]' % n)

        cross = '--host=' + val(1) + ' --target=' + val(0)
    else:
        cross = ''

    return {
        'code': './configure $(CROSS) --prefix=$(INSTALL_DIR) && make && make install'.replace('$(CROSS)', cross),
        'prepare': '$(ADD_PATH)',
        'src': 'https://ftp.gnu.org/gnu/m4/m4-1.4.18.tar.gz',
        'deps': deps,
        'codec': codec,
    }


@helper
def m4(info):
    return m4_0(info, [bestbox(info), make(info), tar_runtime(info), xz(info), curl(info), musl(info)], 'xz')
