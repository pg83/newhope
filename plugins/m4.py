def m4_0(info, deps, codec):
    if 0:
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


@y.options()
def m4(info):
    return m4_0(info, [bestbox_run(info), make_run(info), tar_run(info), xz_run(info), curl_run(info)], 'xz')
