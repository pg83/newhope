@helper
def bestbox1(info):
    cc = info['info']
    gen_func = info['generator_func']
    toybox1 = gen_func('toybox1')(cc)
    busybox1 = gen_func('busybox1')(cc)

    return {
        'code': """
            mkdir -p $(INSTALL_DIR)/original

            mv $(TOYBOX1_DIR)/original/toybox $(INSTALL_DIR)/original/
            mv $(BUSYBOX1_DIR)/original/busybox $(INSTALL_DIR)/original/
        """,
        'deps': [toybox1, busybox1],
    }
