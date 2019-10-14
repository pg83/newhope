@helper
def bestbox0(info):
    return {
        'code': """
            mkdir -p $(INSTALL_DIR)/bin/

            ln $(TOYBOX1_DIR)/bin/toybox $(INSTALL_DIR)/bin
            ln $(BUSYBOX1_DIR)/bin/busybox $(INSTALL_DIR)/bin
        """,
        'prepare': """
            mkdir $(BUILD_DIR)/bin

            $(CUR_DIR)/bin/busybox --install -s $(BUILD_DIR)/bin/

            for i in `$(CUR_DIR)/bin/toolbox`
            do
               ln -fs $(CUR_DIR)/bin/toolbox $(BUILD_DIR)/bin/$i
            done

            export PATH=$(BUILD_DIR)/bin:$PATH
        """,
    }


@helper
def bestbox1(info):
    cc = info['info']
    gen_func = info['generator_func']
    res = gen_func('orig_bestbox0')(info)
    deps = [gen_func('toybox1')(cc), gen_func('busybox1')(cc)]
    res['deps'] = deps
    res['version'] = deps[1]['node']['version'] + '-' + deps[0]['node']['version']

    return res


@helper
def bestbox(info):
    cc = info['info']
    gen_func = info['generator_func']
    res = gen_func('orig_bestbox0')(info)
    deps = [gen_func('toybox')(cc), gen_func('busybox')(cc)]
    res['deps'] = deps
    res['version'] = deps[1]['node']['version'] + '-' + deps[0]['node']['version']

    return res
