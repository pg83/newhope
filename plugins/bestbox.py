def bestbox0(info, deps, codec):
    if 0:
        if y.xp('/info/info/host/os') == 'darwin':
            return system00(info)

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
        'version': y.join_versions(deps[:2]),
        'codec': codec,
        'extra': [
            {'kind': 'subst', 'from': '$(TB)', 'to': y.xp('/deps/0/node/name').upper()},
            {'kind': 'subst', 'from': '$(BB)', 'to': y.xp('/deps/1/node/name').upper()},
        ],
    }


@y.helper
def bestbox2(info):
    return bestbox0(info, [toybox2(info), busybox2(info)], 'gz')


@y.helper
def bestbox1(info):
    return bestbox0(info, [toybox1(info), busybox1(info)], 'gz')


@y.helper
def bestbox(info):
    return bestbox0(info, [toybox(info), busybox(info), tar1(info), xz1(info)], 'xz')
