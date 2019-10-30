@ygenerator(tier=1, kind=['core', 'dev', 'tool'], cached=['deps', 'codec'])
def m40(deps, codec):
    cross = ''

    return {
        'code': './configure $(CROSS) --prefix=$(INSTALL_DIR) && make -j2 && make install'.replace('$(CROSS)', cross),
        'prepare': '$(ADD_PATH)',
        'src': 'https://ftp.gnu.org/gnu/m4/m4-1.4.18.tar.gz',
        'deps': deps,
        'codec': codec,
        'version': '1.4.18',
    }
