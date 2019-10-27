def make0(info, do_make, deps, codec='gz'):
    return to_v2({
        'code': """
            ./configure --prefix=$(INSTALL_DIR) || exit 1
            $(M)
            mkdir $(INSTALL_DIR)/bin && cp make $(INSTALL_DIR)/bin/ && chmod +x $(INSTALL_DIR)/bin/make
        """.replace('$(M)', do_make),
        'src': 'http://mirror.lihnidos.org/GNU/ftp/gnu/make/make-4.2.tar.gz',
        'prepare': '$(ADD_PATH)',
        'codec': codec,
        'deps': deps,
    }, info)


@y.options(repacks=None)
def make2_run(info):
    return make0(info, 'sh ./build.sh', [bestbox2_run(info)])


@y.options(repacks=None)
def make1_run(info):
    return make0(info, 'make -j2', [make2_run(info), bestbox2_run(info)])


@y.options(repacks=None)
def make_run(info):
    return make0(info, 'make -j2', [make1_run(info), bestbox1_run(info), tar1_run(info), xz1_run(info), curl1_run(info)], codec='xz')
