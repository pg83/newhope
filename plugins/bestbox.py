@helper
def bestbox1(info):
    cc = info['info']
    gen_func = info['generator_func']
    toybox1 = gen_func('toybox1')(cc)
    busybox1 = gen_func('busybox1')(cc)

    return {
        'code': """
            mkdir -p $(INSTALL_DIR)/bin/

            ln $(TOYBOX1_DIR)/bin/toybox $(INSTALL_DIR)/bin
            ln $(BUSYBOX1_DIR)/bin/busybox $(INSTALL_DIR)/bin
        """,
        'deps': [toybox1, busybox1],
        'version': busybox1['node']['version'] + '-' + toybox1['node']['version'],
    }
