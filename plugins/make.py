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


@y.options(folders=[])
def make2_run(info):
    return make0('sh ./build.sh', [bestbox2_run(info)])


@y.options(folders=[])
def make1_run(info):
    return make0('make', [make2_run(info), bestbox2_run(info)])


@y.options(folders=[])
def make_run(info):
    return make0('make', [make1_run(info), bestbox1_run(info), tar1_run(info), xz1_run(info), curl1_run(info)], codec='xz')
