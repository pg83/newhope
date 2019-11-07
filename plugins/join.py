def join_funcs(my_name, my_num, args, channel=y.write_channel('new functions', 'join')):
    if not args:
        return args

    if len(args) == 1:
        return args

    def wrapper(info):
        deps = [arg(info) for arg in args]
        nodes = [y.restore_node_node(x) for x in deps]

        if my_num > 3:
            extra = [
                'export PKG_CONFIG=$(CUR_DIR)/bin/pkg-config',
                'export PKG_CONFIG_PATH=$(CUR_DIR)/lib/pkgconfig:$PKG_CONFIG_PATH',
            ]
        else:
            extra = []

        res = {
            'node': {
                'build': ['cp -R $(MNGR_{N}_DIR)/* $IDIR/'.format(N=x['name'].upper()) for x in nodes],
                'name': my_name + str(my_num),
                'version': '3.1315',
                'prepare': extra + [
                    'export CFLAGS="-I$(CUR_DIR)/include $CFLAGS"',
                    'export LDFLAGS="-L$(CUR_DIR)/lib $LDFLAGS"',
                ] + sum([x.get('prepare', []) for f in nodes], []),
                'constraint': info['info'],
            },
            'deps': deps,
        }

        return res

    wrapper.__name__ = my_name + str(my_num)

    channel({'kind': [], 'func': wrapper, 'args': [str(x) for x in args]})

    return [y.options()(wrapper)]
