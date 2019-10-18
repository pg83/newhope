def make0(do_make, deps, codec='gz'):
    return {
        'code': """
            ./configure --prefix=$(INSTALL_DIR) || exit 1
            $(M)
            mkdir $(INSTALL_DIR)/bin && cp make $(INSTALL_DIR)/bin/ && chmod +x $(INSTALL_DIR)/bin/make
        """.replace('$(M)', do_make),
        'src': 'http://mirror.lihnidos.org/GNU/ftp/gnu/make/make-4.2.tar.gz',
        'prepare': '$(ADD_PATH)',
        'codec': codec,
        'deps': deps,
    }


@helper
def make2(info):
    return make0('sh ./build.sh', [bestbox2(info)])


@helper
def make1(info):
    return make0('make', [make2(info), bestbox2(info)])


@helper
def make(info):
    return make0('make', [make1(info), bestbox1(info), tar1(info), xz1(info), curl1(info), musl1(info)], codec='xz')
