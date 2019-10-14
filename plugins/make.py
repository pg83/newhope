@helper
def make2(info):
    cc = info['info']
    gen_func = info['generator_func']
    bestbox1 = gen_func('bestbox1')(cc)

    return {
        'code': """
            #pragma cc
            LDFLAGS=--static ./configure && sh ./build.sh
            mkdir $(INSTALL_DIR)/bin
            cp make $(INSTALL_DIR)/bin/
            chmod +x $(INSTALL_DIR)/bin/make
        """,
        'src': 'http://mirror.lihnidos.org/GNU/ftp/gnu/make/make-4.2.tar.gz',
        'deps': [bestbox1],
        'prepare': 'export PATH=$(CUR_DIR)/bin:$PATH',
        'codec': 'gz',
    }


@helper
def make1(info):
    cc = info['info']
    gen_func = info['generator_func']
    bestbox = gen_func('bestbox')(cc)
    make2 = gen_func('make2')(cc)

    return {
        'code': """
            #pragma cc
            LDFLAGS=--static ./configure --prefix=$(INSTALL_DIR) && make
            mkdir $(INSTALL_DIR)/bin
            cp make $(INSTALL_DIR)/bin/
            chmod +x $(INSTALL_DIR)/bin/make
        """,
        'src': make2['node']['url'],
        'deps': [bestbox, make2],
        'prepare': 'export PATH=$(CUR_DIR)/bin:$PATH',
        'codec': 'gz',
    }
