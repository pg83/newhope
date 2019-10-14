def bestbox0(deps):
    return {
        'code': """
            mkdir -p $(INSTALL_DIR)/bin

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
        'deps': deps,
        'version': join_versions(deps),
    }


@helper
def bestbox2(info):
    return bestbox0([toybox2(info), busybox2(info)])


@helper
def bestbox1(info):
    return bestbox0([toybox1(info), busybox1(info)])


@helper
def bestbox(info):
    return bestbox0([toybox(info), busybox(info)])
