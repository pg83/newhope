def bestbox0(info, deps, codec):
    return {
        'code': """
            mkdir -p $(INSTALL_DIR)/bin

            ln $(MNGR_$(TB)_DIR)/bin/toybox $(INSTALL_DIR)/bin
            ln $(MNGR_$(BB)_DIR)/bin/busybox $(INSTALL_DIR)/bin
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


@y.options(folders=[])
def bestbox2_run(info):
    if y.xp('/info/info/host/os') == 'darwin':
        return system0(info)

    return bestbox0(info, [toybox2_run(info), busybox2_run(info)], 'gz')


@y.options(folders=[])
def bestbox1_run(info):
    if y.xp('/info/info/host/os') == 'darwin':
        return coreutils2_run(info)

    return bestbox0(info, [toybox1_run(info), busybox1_run(info)], 'gz')


@y.options(folders=[])
def bestbox_run(info):
    if y.xp('/info/info/host/os') == 'darwin':
        return coreutils2_run(info)

    return bestbox0(info, [toybox_run(info), busybox_run(info), tar1_run(info), xz1_run(info)], 'xz')
