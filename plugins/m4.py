def m4_0(info, deps, codec):
    cross = ''

    return to_v2({
        'code': './configure $(CROSS) --prefix=$(INSTALL_DIR) && make -j2 && make install'.replace('$(CROSS)', cross),
        'prepare': '$(ADD_PATH)',
        'src': 'https://ftp.gnu.org/gnu/m4/m4-1.4.18.tar.gz',
        'deps': deps,
        'codec': codec,
    }, info)


@y.options()
def m4(info):
    return m4_0(info, [bestbox_run(info), make_run(info), tar_run(info), xz_run(info), curl_run(info)], 'xz')
