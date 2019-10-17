def bestbox0(info, deps, codec):
    if xp('/info/info/host/os') == 'darwin':
        return system0(info)

    return {
        'code': """
            mkdir -p $(INSTALL_DIR)/bin

            ln $($(TB)_DIR)/bin/toybox $(INSTALL_DIR)/bin
            ln $($(BB)_DIR)/bin/busybox $(INSTALL_DIR)/bin
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
        'version': join_versions(deps[:2]),
        'codec': codec,
        'subst': [
            ('$(TB)', xp('/deps/0/node/name').upper()),
            ('$(BB)', xp('/deps/1/node/name').upper()),
        ],
    }


@helper
def bestbox2(info):
    return bestbox0(info, [toybox2(info), busybox2(info)], 'gz')


@helper
def bestbox1(info):
    return bestbox0(info, [toybox1(info), busybox1(info)], 'gz')


@helper
def bestbox(info):
    return bestbox0(info, [toybox(info), busybox(info), tar1(info), xz1(info)], 'xz')
