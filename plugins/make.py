def make0(do_make, deps, codec='gz'):
    return {
        'code': """
            #pragma cc
            LDFLAGS=--static ./configure --prefix=$(INSTALL_DIR) && $(M)
            mkdir $(INSTALL_DIR)/bin
            cp make $(INSTALL_DIR)/bin/
            chmod +x $(INSTALL_DIR)/bin/make
        """.replace('$(M)', do_make),
        'src': 'http://mirror.lihnidos.org/GNU/ftp/gnu/make/make-4.2.tar.gz',
        'prepare': 'export PATH=$(CUR_DIR)/bin:$PATH',
        'codec': codec,
        'deps': deps,
    }


@helper
def make2(info):
    return make0('sh ./build.sh', [system()])


@helper
def make1(info):
    return make0('make', [make2(info), bestbox2(info)])


@helper
def make(info):
    return make0('make', [make1(info), bestbox1(info), tar1(info), xz1(info), curl1(info)], codec='xz')
