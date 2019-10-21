def tool_test0(info, deps, codec):
    return {
        'code': """
           mkdir -p $(INSTALL_DIR)/bin; echo 1 > $(INSTALL_DIR)/bin/x
           which tar
           which xz1
        """,
        'deps': deps,
        'codec': codec,
    }


@y.options()
def tool_test1(info):
    return tool_test0(info, [bestbox2_run(info), tar2_run(info), xz2_run(info)], 'xz')


@y.options()
def tool_test2(info):
    return tool_test0(info, [bestbox1_run(info), tar1_run(info), xz1_run(info), curl1_run(info)], 'xz')
